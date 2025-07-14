import logging
from abc import ABC, abstractmethod
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger("toolfront")


class DocumentError(Exception):
    """Exception for document-related errors."""

    pass


class Document(BaseModel, ABC):
    """Abstract base class for documents."""

    uri: str = Field(..., description="Document URI.")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(uri={self.uri})"

    __repr__ = __str__

    @property
    def path(self) -> Path:
        """Get the Path object from the URI."""
        return Path(self.uri)

    def _get_target_page(self, pagination: int | float, total_pages: int) -> int:
        """Get the target page number, defaulting to page 1 if no pagination specified."""
        if 0 <= pagination < 1:
            return max(1, min(total_pages, int(pagination * total_pages) + 1))
        elif pagination >= 1:
            return max(1, min(total_pages, int(pagination)))
        else:
            return 1  # Always default to page 1

    @abstractmethod
    async def read(self, pagination: int | float = 0) -> str:
        """Read the document content.

        Args:
            pagination: Page/section number (1+ int) or percentile (0-1 exclusive float) to read.
                       Only used for paginated documents (PDF, PPTX, XLSX). Ignored for others.

        Returns:
            Document content as string.
        """
        pass
