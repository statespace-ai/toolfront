import logging
from abc import ABC

from pydantic import BaseModel, Field

from toolfront.models.connections.library import LibraryConnection

logger = logging.getLogger("toolfront")


class DocumentError(Exception):
    """Exception for document-related errors."""

    pass


class Document(BaseModel, ABC):
    """Abstract base class for documents."""

    connection: LibraryConnection = Field(..., description="Library connection.")

    path: str = Field(
        ...,
        description="Absolute document path in slash notation e.g. '/Users/path/to/dir/file.pdf''",
    )
