from pydantic import BaseModel, Field


class Read(BaseModel):
    """Storage library."""

    library_url: str = Field(..., description="Library URL.")

    document_path: str = Field(..., description="Document path.")

    pagination: int | float = Field(
        ...,
        description="Document pagination number or percentile. If 0 <= pagination < 1, it's a percentile. If pagination >= 1, it's a page number.",
    )
