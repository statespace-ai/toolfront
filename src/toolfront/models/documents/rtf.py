import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class RTFDocument(Document):
    """RTF document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read RTF document content.

        Args:
            pagination: Ignored for RTF documents.

        Returns:
            Document content as string.
        """
        try:
            from striprtf.striprtf import rtf_to_text

            with self.path.open("r", encoding="utf-8") as file:
                rtf_content = file.read()
                text = rtf_to_text(rtf_content)
                return text
        except ImportError:
            # Fallback to raw RTF if striprtf not available
            try:
                with self.path.open("r", encoding="utf-8") as file:
                    return f"RTF content (requires striprtf library for text extraction):\n{file.read()}"
            except Exception as e:
                logger.error(f"Error reading RTF file {self.url}: {e}")
                raise DocumentError(f"Error reading RTF file: {str(e)}")
        except Exception as e:
            logger.error(f"Error reading RTF file {self.url}: {e}")
            raise DocumentError(f"Error reading RTF file: {str(e)}")
