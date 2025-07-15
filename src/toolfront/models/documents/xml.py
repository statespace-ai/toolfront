import logging
import xml.etree.ElementTree as ET

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class XMLDocument(Document):
    """XML document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read XML document content.

        Args:
            pagination: Ignored for XML documents.

        Returns:
            Document content as string.
        """
        try:
            tree = ET.parse(self.path)
            root = tree.getroot()

            def element_to_string(elem, level=0):
                indent = "  " * level
                result = f"{indent}Element: {elem.tag}\n"
                if elem.attrib:
                    result += f"{indent}Attributes: {elem.attrib}\n"
                if elem.text and elem.text.strip():
                    result += f"{indent}Text: {elem.text.strip()}\n"
                for child in elem:
                    result += element_to_string(child, level + 1)
                return result

            return element_to_string(root)
        except Exception:
            # Fallback to plain text if parsing fails
            try:
                with self.path.open("r", encoding="utf-8") as file:
                    return file.read()
            except Exception as e:
                logger.error(f"Error reading XML file {self.url}: {e}")
                raise DocumentError(f"Error reading XML file: {str(e)}")
