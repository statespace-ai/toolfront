from pydantic import BaseModel, Field


class Read(BaseModel):
    """Storage library."""

    document_path: str = Field(..., description="Full document path.")

    pagination: int | float = Field(
        ...,
        description="Document pagination number or percentile. If 0 <= pagination < 1, it's a percentile. If pagination >= 1, it's a page number.",
    )
