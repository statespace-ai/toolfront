import logging
import re
import warnings
from abc import ABC
from contextlib import closing
from typing import Any

import ibis
import pandas as pd
from ibis import BaseBackend
from pydantic import BaseModel, Field, PrivateAttr, computed_field, field_serializer, model_validator

from toolfront.models.base import DataSource
from toolfront.utils import sanitize_url, serialize_response

logger = logging.getLogger("toolfront")


class Table(BaseModel):
    path: str = Field(
        ...,
        description="Full table path in dot notation e.g. 'schema.table' or 'database.schema.table'.",
    )


class Query(BaseModel):
    code: str = Field(..., description="SQL query string to execute. Must match the SQL dialect of the database.")

    def is_read_only_query(self) -> bool:
        """Check if SQL contains only read operations"""
        # Remove comments and normalize whitespace
        clean_sql = re.sub(r"--.*?$|/\*.*?\*/", "", self.code, flags=re.MULTILINE | re.DOTALL)
        clean_sql = re.sub(r"\s+", " ", clean_sql).strip().upper()

        # Split on semicolons to handle multiple statements
        statements = [s.strip() for s in clean_sql.split(";") if s.strip()]

        read_only_patterns = [r"^SELECT\b", r"^WITH\b", r"^SHOW\b", r"^DESCRIBE\b", r"^DESC\b", r"^EXPLAIN\b"]

        return all(any(re.match(pattern, stmt) for pattern in read_only_patterns) for stmt in statements)


class Database(DataSource, ABC):
    """Abstract base class for all databases.

    Parameters
    ----------
    url : str
        Database URL for connection.
    match : str, optional
        Regex pattern to match tables. If None, all tables will be used.

    Attributes
    ----------
    _connection : BaseBackend or None
        Ibis backend connection to the database.
    _connection_kwargs : dict[str, Any]
        Additional keyword arguments for database connection.
    """

    url: str = Field(description="Database URL.")

    match: str | None = Field(
        description="Regex pattern to filter tables. If None, all tables will be used.",
        exclude=True,
    )

    _tables: list[str] = PrivateAttr(default_factory=list)
    _connection: BaseBackend | None = PrivateAttr(default=None)
    _connection_kwargs: dict[str, Any] = PrivateAttr(default_factory=dict)

    def __init__(self, url: str, match: str | None = None, **kwargs: Any) -> None:
        self._connection_kwargs = kwargs
        super().__init__(url=url, match=match)

    def __getitem__(self, name: str) -> "ibis.Table":
        parts = name.split(".")
        if not 1 <= len(parts) <= 3:
            raise ValueError(f"Invalid table name: {name}")
        return self._connection.table(parts[-1], database=tuple(parts[:-1]) if len(parts) > 1 else None)

    def __repr__(self) -> str:
        dump = self.model_dump(exclude={"tables"})
        args = ", ".join(f"{k}={repr(v)}" for k, v in dump.items())
        return f"{self.__class__.__name__}({args})"

    @model_validator(mode="after")
    def model_validator(self) -> "Database":
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Unable to create Ibis UDFs", UserWarning)
            self._connection = ibis.connect(self.url, **self._connection_kwargs)

        # Handle tables parameter: None (all), string (regex), or list (exact names)
        if self.match:
            if not isinstance(self.match, str):
                raise ValueError(f"Match must be a string, got {type(self.match)}")

            try:
                re.compile(self.match)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern for tables: {self.match} - {str(e)}")

        # Discover all available tables in the database
        catalog = self._connection.current_catalog
        databases = self._connection.list_databases(catalog=catalog)

        all_tables = []
        for db in databases:
            tables = self._connection.list_tables(like=self.match, database=(catalog, db))
            prefix = f"{catalog}." if catalog else ""
            all_tables.extend([f"{prefix}{db}.{table}" for table in tables])

        if not len(all_tables):
            raise ValueError("No tables found in the database")

        self._tables = all_tables

        return self

    @field_serializer("url")
    def serialize_url(self, value: str) -> str:
        """Serialize URL field by sanitizing sensitive information.

        Parameters
        ----------
        value : str
            Original database URL.

        Returns
        -------
        str
            Sanitized URL with sensitive information removed.
        """
        return sanitize_url(value)

    @computed_field
    @property
    def tables(self) -> list[str]:
        return self._tables

    def tools(self) -> list[callable]:
        """Return list of available tool methods.

        Returns
        -------
        list[callable]
            List containing inspect_table and query methods.
        """
        return [self.inspect_table, self.query]

    async def inspect_table(
        self,
        table: Table = Field(..., description="Database table to inspect."),
    ) -> dict[str, Any]:
        """Inspect the schema of database table and get sample data.

        1. Use this tool to understand table structure like column names, data types, and constraints
        2. Inspecting tables helps understand the structure of the data
        3. ALWAYS inspect unfamiliar tables first to learn their columns and data types before querying
        """
        try:
            logger.debug(f"Inspecting table: {self.url} {table.path}")
            table = self[table.path]
            return {
                "schema": serialize_response(table.info().to_pandas()),
                "samples": serialize_response(table.head(5).to_pandas()),
            }
        except Exception as e:
            logger.error(f"Failed to inspect table: {e}", exc_info=True)
            raise RuntimeError(f"Failed to inspect table {table.path} in {self.url} - {str(e)}") from e

    async def query(
        self,
        query: Query = Field(..., description="Read-only SQL query to execute."),
    ) -> dict[str, Any]:
        """
        This tool allows you to run read-only SQL queries against a database.

        ALWAYS ENCLOSE IDENTIFIERS (TABLE NAMES, COLUMN NAMES) IN QUOTES TO PRESERVE CASE SENSITIVITY AND AVOID RESERVED WORD CONFLICTS AND SYNTAX ERRORS.

        1. ONLY write read-only queries for tables that have been explicitly discovered or referenced.
        2. Before writing queries, make sure you understand the schema of the tables you are querying.
        3. ALWAYS use the correct dialect for the database.
        4. NEVER use aliases in queries unless strictly necessary.
        5. When a query fails or returns unexpected results, try to diagnose the issue and then retry.
        """
        logger.debug(f"Querying database: {self.url} {query.code}")
        if not query.is_read_only_query():
            raise ValueError("Only read-only queries are allowed")

        if not hasattr(self._connection, "raw_sql"):
            raise ValueError("Database does not support raw sql queries")

        with closing(self._connection.raw_sql(query.code)) as cursor:
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(cursor.fetchall(), columns=columns)

    def _preprocess(self, var_type: Any) -> Any:
        return Query if isinstance(var_type, pd.DataFrame) else var_type

    def _postprocess(self, result: Any) -> Any:
        return self.query(result) if isinstance(result, Query) else result
