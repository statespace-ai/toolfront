from abc import ABC

from pydantic import BaseModel, Field


class Document(BaseModel, ABC):
    """Abstract base class for documents."""

    library_url: str = Field(..., description="Library URL.")

    path: str = Field(
        ...,
        description="Document path in relative to the library url e.g. 'path/to/file.pdf'.",
    )
