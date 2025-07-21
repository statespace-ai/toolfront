import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class GenericDocument(Document):
    """Generic document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read TXT document content.

        Args:
            pagination: Ignored for TXT documents.

        Returns:
            Document content as string.
        """
        try:
            with self.path.open("r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading file {self.url}: {e}")
            raise DocumentError(f"Error reading file: {str(e)}")
