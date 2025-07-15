import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class TXTDocument(Document):
    """TXT document reader."""

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
            logger.error(f"Error reading TXT file {self.url}: {e}")
            raise DocumentError(f"Error reading TXT file: {str(e)}")
