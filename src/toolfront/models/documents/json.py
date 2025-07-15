import json
import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class JSONDocument(Document):
    """JSON document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read JSON document content.

        Args:
            pagination: Ignored for JSON documents.

        Returns:
            Document content as string.
        """
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file {self.url}: {e}")
            raise DocumentError(f"Error parsing JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Error reading JSON file {self.url}: {e}")
            raise DocumentError(f"Error reading JSON file: {str(e)}")
