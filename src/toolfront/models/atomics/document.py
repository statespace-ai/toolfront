import logging
from abc import ABC

from pydantic import BaseModel, Field

from toolfront.models.connections.library import LibraryConnection
from toolfront.types import DocumentType

logger = logging.getLogger("toolfront")


class DocumentError(Exception):
    """Exception for document-related errors."""

    pass


class Document(BaseModel, ABC):
    """Abstract base class for documents."""

    connection: LibraryConnection = Field(..., description="Library connection.")

    document_type: DocumentType = Field(..., description="Document type.")

    document_path: str = Field(
        ...,
        description="Absolute document path in slash notation e.g. '/Users/path/to/dir/file.pdf''",
    )
