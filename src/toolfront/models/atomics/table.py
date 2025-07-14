from pydantic import BaseModel, Field


class Table(BaseModel):
    """Unified table identifier for both database tables and file tables."""

    database_url: str = Field(..., description="Database URL.")

    path: str = Field(
        ...,
        description="Full table path in dot notation e.g. 'schema.table' or 'database.schema.table'.",
    )
