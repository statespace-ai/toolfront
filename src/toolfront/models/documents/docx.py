from docx import Document as DocxDocument

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class DocX(Document):
    """Microsoft Word document."""

    async def sample(self) -> str:
        doc = DocxDocument(self.path)
        text = ""
        for paragraph in doc.paragraphs[:10]:  # Sample first 10 paragraphs
            text += paragraph.text + "\n"
        return text[:MAX_SAMPLE_CHARS]

    async def read(self) -> str:
        doc = DocxDocument(self.path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
