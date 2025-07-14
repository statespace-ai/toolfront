import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class PDFDocument(Document):
    """PDF document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read PDF document content.

        Args:
            pagination: Page number (1+ int) or percentile (0-1 exclusive float) to read.

        Returns:
            Document content as string.
        """
        try:
            from pypdf import PdfReader

            reader = PdfReader(self.path)
            total_pages = len(reader.pages)

            target_page_idx = self._get_target_page(pagination, total_pages) - 1

            text = f"Page {target_page_idx + 1} of {total_pages}:\n\n"
            text += reader.pages[target_page_idx].extract_text()

            return text
        except ImportError:
            error_msg = "PDF support requires pypdf library"
            logger.error(f"Missing dependency for PDF reading: {error_msg}")
            raise DocumentError(error_msg)
        except Exception as e:
            logger.error(f"Error reading PDF file {self.uri}: {e}")
            raise DocumentError(f"Error reading PDF file: {str(e)}")
