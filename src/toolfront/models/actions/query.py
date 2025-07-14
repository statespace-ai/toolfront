from pydantic import BaseModel, Field


class Query(BaseModel):
    """Query model for both database queries and file queries."""

    database_url: str = Field(..., description="Database URL.")

    code: str = Field(..., description="SQL query string to execute. Must match the SQL dialect of the database.")
