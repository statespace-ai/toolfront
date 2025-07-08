import logging
from abc import ABC

from pydantic import BaseModel, Field

from toolfront.models.connection import StorageConnection

logger = logging.getLogger("toolfront")


class DocumentError(Exception):
    """Exception for document-related errors."""

    pass


class Document(BaseModel, ABC):
    """Abstract base class for documents."""

    connection: StorageConnection = Field(..., description="Storage connection.")

    path: str = Field(
        ...,
        description="Full document path in slash notation e.g. '/Users/path/to/dir/file.pdf' or 'relative/path/to/dir/file.pdf'",
    )
