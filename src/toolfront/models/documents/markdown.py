from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class Markdown(Document):
    """Markdown document."""

    async def sample(self) -> str:
        with Path(self.path).open() as file:
            text = file.read()[:MAX_SAMPLE_CHARS]
        return text[:MAX_SAMPLE_CHARS]

    async def read(self) -> str:
        with Path(self.path).open() as file:
            return file.read()
