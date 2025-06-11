from urllib.parse import unquote

from pydantic import BaseModel, Field
from sqlalchemy.engine.url import make_url

from toolfront.models.connection import Connection

FILESYSTEM_DIALECT = "duckdb"


class Query(BaseModel):
    """Query model for both database queries and file queries."""

    connection: Connection = Field(..., description="Query data source.")

    code: str = Field(..., description="SQL query string to execute. Must match the SQL dialect of the data source.")

    description: str = Field(
        ...,
        description="A clear business-focused description of what the query does including tables and transformations used.",
    )

    @property
    def dialect(self) -> str:
        if self.connection.url.startswith("filesystem://"):
            return str(FILESYSTEM_DIALECT)
        else:
            # For database sources, parse the URL to get the driver name
            url = make_url(unquote(self.connection.url))
            return url.drivername
