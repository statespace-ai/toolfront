from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class TXT(Document):
    """Plain text file."""

    async def sample(self) -> str:
        with Path(self.path).open("r", encoding="utf-8") as file:
            return file.read()[:MAX_SAMPLE_CHARS]

    async def read(self) -> str:
        with Path(self.path).open("r", encoding="utf-8") as file:
            return file.read()
