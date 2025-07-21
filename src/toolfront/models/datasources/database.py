import asyncio
import logging
import re
import warnings
from abc import ABC
from contextlib import closing
from itertools import chain
from typing import Any

import ibis
import pandas as pd
from ibis import BaseBackend
from pydantic import Field, PrivateAttr, model_validator
from pydantic_ai import ModelRetry

from toolfront.models.actions.query import Query
from toolfront.models.atomics.table import Table
from toolfront.models.datasources.base import DataSource
from toolfront.utils import serialize_response

logger = logging.getLogger("toolfront")


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

        if isinstance(self.tables, str):
            tables = self._get_tables(like=self.tables)
            if not tables:
                raise ValueError(f"No tables found matching the regex pattern: {tables}")
        elif isinstance(self.tables, list):
            tables = [table for table in self.tables if table in set(self._get_tables())]
            if not tables:
                raise ValueError(f"No tables found matching the list: {tables}")

        if not self.tables:
            self.tables = self._get_tables()

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
        3. Always inspect tables before writing queries to understand their structure and prevent errors
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

    def _query(self, query: Query) -> dict[str, Any]:
        """
        Query the database.
        """
        logger.debug(f"Querying database: {self.url} {query.code}")
        if not query.is_read_only_query():
            raise ValueError("Only read-only queries are allowed")

        if not hasattr(self._connection, "raw_sql"):
            raise ValueError("Database does not support raw sql queries")

        with closing(self._connection.raw_sql(query.code)) as cursor:
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(cursor.fetchall(), columns=columns)

    async def query(
        self,
        query: Query = Field(..., description="Read-only SQL query to execute."),
    ) -> dict[str, Any]:
        """
        This tool allows you to run read-only SQL queries against a database.

        ALWAYS ENCLOSE IDENTIFIERS (TABLE NAMES, COLUMN NAMES) IN QUOTES TO PRESERVE CASE SENSITIVITY AND AVOID RESERVED WORD CONFLICTS AND SYNTAX ERRORS.

        1. Only write read-only queries for against tables that have been explicitly discovered or referenced.
        2. Before writing queries, make sure you understand the schema of the tables you are querying.
        3. Always use the correct dialect for the database.
        4. Do not use aliases in queries unless strictly necessary.
        5. When a query fails or returns unexpected results, try to diagnose the issue and then retry.
        """
        try:
            return serialize_response(self._query(query))
        except Exception as e:
            logger.error(f"Failed to query database: {e}", exc_info=True)
            raise ModelRetry(f"Failed to query database in {self.url} - {str(e)}") from e

    def _get_tables(self, like: str | None = None) -> list[str]:
        """List all tables in the database."""
        return asyncio.run(self._get_tables_async(like))

    async def _get_tables_async(self, like: str | None = None) -> list[str]:
        """List all tables in the database asynchronously."""

        catalog = self._connection.current_catalog
        databases = self._connection.list_databases(catalog=catalog)

        async def get_filtered_tables(db: str) -> list[str]:
            tables = await asyncio.to_thread(self._connection.list_tables, like=like, database=(catalog, db))
            prefix = f"{catalog}." if catalog else ""
            return [f"{prefix}{db}.{table}" for table in tables if not like or re.match(like, table)]

        results = await asyncio.gather(*[get_filtered_tables(db) for db in databases])
        return list(chain.from_iterable(results))

    def _retrieve_class(self):
        return Query

    def _retrieve_function(self) -> Any:
        return self._query
