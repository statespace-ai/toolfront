import re
from abc import ABC
from typing import Any

import pandas as pd
from pydantic import Field, PrivateAttr, model_validator
from sqlalchemy.engine.url import make_url

from toolfront.models.database_connections.base import DatabaseConnection
from toolfront.models.datasources.base import DataSource
from toolfront.types import SearchMode
from toolfront.utils import search_items


class Database(DataSource, ABC):
    """Abstract base class for all databases."""

    url: str = Field(description="Database URL.")

    _connection: DatabaseConnection | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def model_validator(self) -> "Database":
        self._connection = DatabaseConnection.from_url(self.url)
        return self

    def sanitized_url(self) -> str:
        return str(self._connection.url)

    @classmethod
    def create_from_url(cls, url: str) -> "Database":
        return cls(url=url)

    def __str__(self) -> str:
        return f"Database(url={self._connection.url})"

    def __repr__(self) -> str:
        return f"Database(url={self.url})"

    @property
    def dialect(self) -> str:
        return str(make_url(self.url).drivername)

    async def get_tables(self) -> list[str]:
        """Get all tables in the database."""
        return await self._connection.get_tables()

    async def search_tables(self, pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10) -> list[str]:
        """Search for table names using different algorithms."""
        table_names = await self.get_tables()
        if not table_names:
            return []

        try:
            return search_items(table_names, pattern, mode, limit)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

    async def inspect_table(self, table_path: str) -> Any:
        """Inspect the structure of a table at the given path."""
        return await self._connection.inspect_table(table_path)

    async def sample_table(self, table_path: str, n: int = 5) -> Any:
        """Sample data from the specified table."""
        return await self._connection.sample_table(table_path, n)

    async def query(self, code: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        return await self._connection.query(code)
