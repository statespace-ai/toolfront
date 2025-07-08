from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class YAML(Document):
    """YAML file."""

    async def sample(self) -> str:
        try:
            import yaml

            with Path(self.path).open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                # Pretty print YAML with limited output
                return yaml.dump(data, indent=2, default_flow_style=False)[:MAX_SAMPLE_CHARS]
        except ImportError:
            # Fallback to plain text if PyYAML not available
            with Path(self.path).open("r", encoding="utf-8") as file:
                return file.read()[:MAX_SAMPLE_CHARS]
        except Exception as e:
            return f"Error parsing YAML: {str(e)}"

    async def read(self) -> str:
        try:
            import yaml

            with Path(self.path).open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return yaml.dump(data, indent=2, default_flow_style=False)
        except ImportError:
            # Fallback to plain text if PyYAML not available
            with Path(self.path).open("r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error parsing YAML: {str(e)}"
