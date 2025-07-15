import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class MarkdownDocument(Document):
    """Markdown document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read Markdown document content.

        Args:
            pagination: Ignored for Markdown documents.

        Returns:
            Document content as string.
        """
        try:
            with self.path.open("r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading Markdown file {self.url}: {e}")
            raise DocumentError(f"Error reading Markdown file: {str(e)}")
