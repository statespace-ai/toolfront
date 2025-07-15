import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class YAMLDocument(Document):
    """YAML document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read YAML document content.

        Args:
            pagination: Ignored for YAML documents.

        Returns:
            Document content as string.
        """
        try:
            import yaml

            with self.path.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return yaml.dump(data, indent=2, default_flow_style=False)
        except ImportError:
            # Fallback to plain text if PyYAML not available
            try:
                with self.path.open("r", encoding="utf-8") as file:
                    return file.read()
            except Exception as e:
                logger.error(f"Error reading YAML file {self.url}: {e}")
                raise DocumentError(f"Error reading YAML file: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing YAML file {self.url}: {e}")
            raise DocumentError(f"Error parsing YAML: {str(e)}")
