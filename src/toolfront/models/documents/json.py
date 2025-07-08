import json
from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class JSON(Document):
    """JSON file."""

    async def sample(self) -> str:
        with Path(self.path).open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                # Pretty print with limited depth for sampling
                return json.dumps(data, indent=2, ensure_ascii=False)[:MAX_SAMPLE_CHARS]
            except json.JSONDecodeError as e:
                return f"Error parsing JSON: {str(e)}"

    async def read(self) -> str:
        with Path(self.path).open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return json.dumps(data, indent=2, ensure_ascii=False)
            except json.JSONDecodeError as e:
                return f"Error parsing JSON: {str(e)}"
