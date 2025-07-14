import asyncio
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from toolfront.types import ConnectionResult

logger = logging.getLogger("toolfront")


class DatabaseConnection(BaseModel, ABC):
    """Abstract base class for all database connectors."""

    url: str | URL = Field(description="Database connection URL")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("url", mode="after")
    @classmethod
    def url_validator_before(cls, url: Any) -> URL:
        if isinstance(url, URL):
            return url
        elif isinstance(url, str):
            return make_url(url)

        raise ValueError(f"Invalid URL: {url}")

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.test_connection()

    @staticmethod
    def from_url(url: str) -> "DatabaseConnection":
        """Create a database connector from a URL."""
        match make_url(url).drivername:
            case "postgresql" | "postgres":
                from toolfront.models.database_connections.postgresql import PostgreSQLConnection

                return PostgreSQLConnection(url=url)
            case "mysql" | "mariadb":
                from toolfront.models.database_connections.mysql import MySQLConnection

                return MySQLConnection(url=url)
            case "sqlite":
                from toolfront.models.database_connections.sqlite import SQLiteConnection

                return SQLiteConnection(url=url)
            case "mssql" | "sqlserver":
                from toolfront.models.database_connections.sqlserver import SQLServerConnection

                return SQLServerConnection(url=url)
            case "bigquery":
                from toolfront.models.database_connections.bigquery import BigQueryConnection

                return BigQueryConnection(url=url)
            case "snowflake":
                from toolfront.models.database_connections.snowflake import SnowflakeConnection

                return SnowflakeConnection(url=url)
            case "databricks":
                from toolfront.models.database_connections.databricks import DatabricksConnection

                return DatabricksConnection(url=url)
            case _:
                raise ValueError(f"Unsupported database type: {url.drivername}")

    @abstractmethod
    def test_connection(self) -> ConnectionResult:
        """Test the connection to the database."""
        raise NotImplementedError("Subclasses must implement test_connection")

    @abstractmethod
    async def get_tables(self) -> list[str]:
        """Get the tables of the data source."""
        raise NotImplementedError("Subclasses must implement get_tables")

    @abstractmethod
    async def inspect_table(self, table_path: str) -> Any:
        """Inspect the structure of a table at the given path."""
        raise NotImplementedError("Subclasses must implement inspect_table")

    @abstractmethod
    async def sample_table(self, table_path: str, n: int = 5) -> Any:
        """Sample data from the specified table."""
        raise NotImplementedError("Subclasses must implement sample_table")

    @abstractmethod
    async def query(self, code: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        raise NotImplementedError("Subclasses must implement query")


class FileMixin:
    @field_validator("url")
    def check_file_exists(cls, url: str) -> str:
        url_obj = make_url(url)
        if url_obj.database and not Path(url_obj.database).is_file() and "memory:" not in url_obj.database:
            raise FileNotFoundError(f"File does not exist: {url_obj.database}")
        return url


class SyncSQLAlchemyMixin:
    def initialize_session(self) -> str | None:
        """Return SQL statement to execute for session initialization, or None if no initialization needed."""
        return None

    def test_connection(self) -> ConnectionResult:
        """Test the connection to the database."""
        try:
            self.query("SELECT 1")
            return ConnectionResult(connected=True, message="Connection successful")
        except Exception as e:
            return ConnectionResult(connected=False, message=f"Connection failed: {e}")

    def query(self, code: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        init_sql = self.initialize_session()

        # Try async first, fallback to sync for configuration errors
        engine = create_engine(self.url, echo=False)
        try:
            with engine.connect() as conn:
                conn = conn.execution_options(readonly=True)
                if init_sql:
                    conn.execute(text(init_sql))
                    conn.commit()
                result = conn.execute(text(code))
                data = result.fetchall()
                logger.debug(f"Sync query executed successfully: {code[:100]}...")
                return pd.DataFrame(data)
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {e}") from e
        finally:
            engine.dispose()


class AsyncSQLAlchemyMixin:
    @field_validator("url", mode="after")
    def url_validator(cls, url: str | URL) -> str | URL:
        if not isinstance(url, URL):
            url = make_url(url)

        match url.drivername:
            case "postgresql":
                return url.set(drivername="postgresql+psycopg2")
            case "mysql":
                return url.set(drivername="mysql+pymysql")
            case "sqlite":
                return url.set(drivername="sqlite+aiosqlite")
            case "mssql":
                return url.set(drivername="mssql+pyodbc")

        return url

    async def initialize_session(self) -> str | None:
        """Return SQL statement to execute for session initialization, or None if no initialization needed."""
        return None

    def test_connection(self) -> ConnectionResult:
        """Test the connection to the database."""
        try:
            asyncio.get_event_loop().run_until_complete(self.query("SELECT 1"))
            return ConnectionResult(connected=True, message="Connection successful")
        except Exception as e:
            return ConnectionResult(connected=False, message=f"Connection failed: {e}")

    async def query(self, code: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame."""
        init_sql = await self.initialize_session()

        # Try async first, fallback to sync for configuration errors
        engine = create_async_engine(self.url, echo=False)
        try:
            async with engine.connect() as conn:
                conn = await conn.execution_options(readonly=True)
                if init_sql:
                    await conn.execute(text(init_sql))
                result = await conn.execute(text(code))
                data = result.fetchall()
                logger.debug(f"Async query executed successfully: {code[:100]}...")
                return pd.DataFrame(data)
        finally:
            await engine.dispose()
