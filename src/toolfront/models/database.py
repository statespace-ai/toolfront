import logging
import warnings
from abc import ABC
from contextlib import closing
from typing import Any

import ibis
import pandas as pd
import sqlparse
from ibis import BaseBackend
from pydantic import BaseModel, Field, PrivateAttr, model_validator

from toolfront.models.base import DataSource
from toolfront.utils import serialize_response

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
        parsed = sqlparse.parse(self.code)

        for statement in parsed:
            stmt_type = statement.get_type()
            if stmt_type not in ["SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN"]:
                return False

        return True


class Database(DataSource, ABC):
    """Abstract base class for all databases."""

    url: str = Field(description="Database URL.")

    tables: list[str] | str | None = Field(
        description="List of tables in the database, or a regex pattern to match tables. If None, all tables will be used."
    )

    _connection: BaseBackend | None = PrivateAttr(default=None)

    def __init__(self, url: str, tables: list[str] | str | None = None, **kwargs: Any) -> None:
        super().__init__(url=url, tables=tables, **kwargs)

    def __getitem__(self, name: str) -> "ibis.Table":
        parts = name.split(".")
        if not 1 <= len(parts) <= 3:
            raise ValueError(f"Invalid table name: {name}")
        return self._connection.table(parts[-1], database=tuple(parts[:-1]) if len(parts) > 1 else None)

    @model_validator(mode="after")
    def model_validator(self) -> "Database":
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", "Unable to create Ibis UDFs", UserWarning)
            self._connection = ibis.connect(self.url)

        like = None
        if isinstance(self.tables, str):
            like = self.tables


        catalog = self._connection.current_catalog
        databases = self._connection.list_databases(catalog=catalog)

        all_tables = []
        for db in databases:
            tables = self._connection.list_tables(
                like=like, database=(catalog, db))
            prefix = f"{catalog}." if catalog else ""
            all_tables.extend([f"{prefix}{db}.{table}" for table in tables])

        if isinstance(self.tables, list):
            self.tables = [t for t in all_tables if t in self.tables]
            if not self.tables:
                raise ValueError(f"None of the specified tables found: {self.tables}")
        else:
            self.tables = all_tables

        return self

    def tools(self) -> list[callable]:
        return [self.inspect_table, self.query]

    async def inspect_table(
        self,
        table: Table = Field(..., description="Database table to inspect."),
    ) -> dict[str, Any]:
        """
        Inspect the schema of database table and get the first 5 samples from it.

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


    def _retrieve_class(self):
        return Query

    def _retrieve_function(self) -> Any:
        return self.query
