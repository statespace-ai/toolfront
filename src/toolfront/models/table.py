from pydantic import BaseModel, Field

from toolfront.models.connection import Connection


class Table(BaseModel):
    """Unified table identifier for both database tables and file tables."""

    connection: Connection = Field(..., description="Table connection.")

    path: str = Field(
        ...,
        description="Full path to the table in the data source. \n"
        "For database data sources: dot notation (e.g. 'schema.table' or 'database.schema.table'). \n"
        "For 'filesystem' data sources: absolute path (e.g. '/path/to/file.csv') or relative path from the source name (e.g. 'path/to/file.parquet').",
    )
