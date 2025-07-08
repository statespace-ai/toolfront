import xml.etree.ElementTree as ET
from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class XML(Document):
    """XML file."""

    async def sample(self) -> str:
        try:
            # Parse XML and pretty print
            tree = ET.parse(self.path)
            root = tree.getroot()

            # Create a structured representation
            result = f"Root element: {root.tag}\n"
            result += f"Root attributes: {root.attrib}\n\n"

            # Sample first few elements
            for i, child in enumerate(root):
                if i >= 5:  # Limit to first 5 elements
                    result += "... (truncated)\n"
                    break
                result += f"Element: {child.tag}\n"
                result += f"Attributes: {child.attrib}\n"
                if child.text and child.text.strip():
                    result += f"Text: {child.text.strip()}\n"
                result += "\n"

            return result[:MAX_SAMPLE_CHARS]
        except Exception as e:
            # Fallback to plain text if parsing fails
            with Path(self.path).open("r", encoding="utf-8") as file:
                return file.read()[:MAX_SAMPLE_CHARS]

    async def read(self) -> str:
        try:
            # Parse XML and create structured output
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
        except Exception as e:
            # Fallback to plain text if parsing fails
            with Path(self.path).open("r", encoding="utf-8") as file:
                return file.read()
