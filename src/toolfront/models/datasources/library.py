from abc import ABC
from pathlib import Path
from urllib.parse import urlparse

from pydantic import Field, model_validator

from toolfront.models.datasources.base import DataSource
from toolfront.models.datasources.database import SearchMode
from toolfront.types import DocumentType
from toolfront.utils import search_items


class Library(DataSource, ABC):
    """Abstract base class for library."""

    url: str = Field(..., description="Library URL.")

    @model_validator(mode="after")
    def validate_model(self) -> "Library":
        if not self.scheme == "file":
            raise ValueError("Only file:// URLs are supported for libraries.")

        path = self.path
        if not path.exists():
            raise ValueError(f"Library path does not exist: {path}")

        return self

    def sanitized_url(self) -> str:
        return str(self.url)

    @classmethod
    def create_from_url(cls, url: str) -> "Library":
        return cls(url=url)

    def __str__(self) -> str:
        return f"Library(url={self.url})"

    __repr__ = __str__

    @property
    def scheme(self) -> str:
        parsed_url = urlparse(self.url)
        return parsed_url.scheme

    @property
    def path(self) -> Path:
        parsed_url = urlparse(self.url)
        return Path(parsed_url.path)

    async def get_documents(self) -> list[str]:
        """Get all documents in the library recursively."""

        path = self.path
        if not path.exists():
            return []

        try:
            supported_extensions = DocumentType.get_supported_extensions()
            return [str(p.relative_to(path)) for p in path.rglob("*.*") if p.suffix.lower() in supported_extensions]
        except (PermissionError, OSError) as e:
            raise RuntimeError(f"Error accessing {path}: {e}") from e

    async def search_documents(self, pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10) -> list[str]:
        """Search for documents in the library."""
        files = await self.get_documents()
        return search_items(files, pattern, mode, limit)

    async def read_document(self, document_path: str, pagination: int | float = 0) -> str:
        """Read the file using appropriate method based on file extension.

        Args:
            document_type: Type of the document to read.
            document_path: Path to the document.
            pagination: Page/section number (1+ int) or percentile (0-1 exclusive float) to read.
                        Only used for paginated documents (PDF, PPTX, XLSX). Ignored for others.
        """

        document_url = str(Path(self.path) / document_path)

        document_type = DocumentType.from_file(document_url)

        try:
            match document_type:
                case DocumentType.DOCX:
                    from toolfront.models.documents.docx import DOCXDocument

                    document = DOCXDocument(url=document_url)
                case DocumentType.XLSX | DocumentType.XLS:
                    from toolfront.models.documents.excel import ExcelDocument

                    document = ExcelDocument(url=document_url)
                case DocumentType.JSON:
                    from toolfront.models.documents.json import JSONDocument

                    document = JSONDocument(url=document_url)
                case DocumentType.MD:
                    from toolfront.models.documents.markdown import MarkdownDocument

                    document = MarkdownDocument(url=document_url)
                case DocumentType.PDF:
                    from toolfront.models.documents.pdf import PDFDocument

                    document = PDFDocument(url=document_url)
                case DocumentType.PPTX:
                    from toolfront.models.documents.powerpoint import PowerPointDocument

                    document = PowerPointDocument(url=document_url)
                case DocumentType.RTF:
                    from toolfront.models.documents.rtf import RTFDocument

                    document = RTFDocument(url=document_url)
                case DocumentType.TXT:
                    from toolfront.models.documents.txt import TXTDocument

                    document = TXTDocument(url=document_url)
                case DocumentType.XML:
                    from toolfront.models.documents.xml import XMLDocument

                    document = XMLDocument(url=document_url)
                case DocumentType.YAML | DocumentType.YML:
                    from toolfront.models.documents.yaml import YAMLDocument

                    document = YAMLDocument(url=document_url)
                case _:
                    raise ValueError(f"Unsupported document type: {document_type}")

        except ImportError as e:
            raise ImportError(f"Import error: {e}. Please install 'toolfront[all]' or toolfront[doc]") from e
        except Exception as e:
            raise RuntimeError(f"Error reading document {document_path}: {e}") from e

        return await document.read(pagination)
