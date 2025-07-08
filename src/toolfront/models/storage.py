import importlib
import logging
from abc import ABC
from pathlib import Path
from typing import Any
from urllib.parse import ParseResult, urlparse

from pydantic import BaseModel, Field, field_validator

from toolfront.models.database import SearchMode
from toolfront.models.documents import document_map
from toolfront.types import ConnectionResult
from toolfront.utils import search_items

valid_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx',
                    '.md', '.txt', '.rtf', '.json', '.yaml',
                    '.yml', '.xml'}

logger = logging.getLogger("toolfront")


class StorageError(Exception):
    """Exception for storage-related errors."""

    pass


class Storage(BaseModel, ABC):
    """Abstract base class for storage."""

    url: ParseResult = Field(description="URL of the storage")

    @field_validator("url", mode="before")
    def validate_url(cls, v: Any) -> ParseResult:
        if isinstance(v, str):
            v = urlparse(v)
        return v

    @classmethod
    def extension(cls) -> str:
        return cls.url.path.split(".")[-1]

    async def test_connection(self) -> ConnectionResult:
        """Test the connection to the storage."""
        return ConnectionResult(connected=True, message="Storage connection successful")

    async def get_documents(self) -> list[str]:
        """Get all documents in the storage recursively."""
        path = Path(self.url.path)
        if not path.exists():
            return []

        try:
            return [str(p) for p in path.rglob("*.*")
                    if p.suffix.lower() in valid_extensions]
        except (PermissionError, OSError) as e:
            logger.warning(f"Error accessing {path}: {e}")
            return []

    async def search_documents(self, pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10) -> list[str]:
        """Search for documents in the storage."""
        files = await self.get_documents()
        return search_items(files, pattern, mode, limit)

    async def inspect_document(self, file_path: str) -> dict[str, list[str] | dict[str, Any]]:
        """
        Inspect the file structure and return sections, sheet names, etc.

        Args:
            file_path: Path to the file to inspect

        Returns:
            Dictionary containing file structure information:
            - 'file_type': Type of file (pdf, xlsx, docx, etc.)
            - 'sections': List of hierarchical sections/headings
            - 'sheets': List of sheet names (for spreadsheets)
            - 'metadata': Additional file metadata
        """
        document_type, document_class_name = document_map[self.extension]
        module = importlib.import_module(
            f"toolfront.models.documents.{document_type.value}")
        document_class = getattr(module, document_class_name)
        return document_class(path=file_path)

    async def sample_document(self, file_path: str) -> str:
        """Sample the file."""
        document_type, document_class_name = document_map[self.extension]
        module = importlib.import_module(
            f"toolfront.models.documents.{document_type.value}")
        document_class = getattr(module, document_class_name)
        return document_class(path=file_path)

    async def read_document(self, file_path: str) -> str:
        """Read the file."""
        document_type, document_class_name = document_map[self.extension]
        module = importlib.import_module(
            f"toolfront.models.documents.{document_type.value}")
        document_class = getattr(module, document_class_name)
        return document_class(path=file_path)
