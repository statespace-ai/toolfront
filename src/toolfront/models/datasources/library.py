
from abc import ABC
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import Field, model_validator

from toolfront.models.actions.read import Read
from toolfront.models.datasources.base import DataSource
from toolfront.types import DocumentType


class Library(DataSource, ABC):
    """Abstract base class for document libraries."""

    url: str = Field(..., description="Library URL.")
    # documents: list[str] = Field(..., description="List of documents in the library.")

    @model_validator(mode="before")
    def validate_model(cls, v: Any) -> Any:
        parsed_url = urlparse(v.get("url"))
        if parsed_url.scheme != "file":
            raise ValueError("Only file:// URLs are supported for libraries.")

        path = Path(parsed_url.path)
        if not path.exists():
            raise ValueError(f"Library path does not exist: {path}")

        return v

    def tools(self) -> list[callable]:
        return [self.glob_search_documents, self.read_document]

    @property
    def path(self) -> Path:
        parsed_url = urlparse(self.url)
        return Path(parsed_url.path) if parsed_url.scheme == "file" else Path(self.url)

    async def glob_search_documents(self, pattern: str = Field(..., description="Glob pattern to search for.")) -> list[str]:
        """
        Return document paths in the library matching the glob pattern (e.g. "*.pdf", "docs/*.txt").

        1. Use educated guesses for initial glob patterns based on document type and target content.
        2. If your search fails, retry with a different glob pattern.
        3. Returns up to 100 results.
        """
        parsed_url = urlparse(self.url)
        root_path = Path(parsed_url.path) if parsed_url.scheme == "file" else Path(self.url)

        documents = []
        for file_path in root_path.rglob(pattern):
            if file_path.is_file():
                documents.append(str(file_path.relative_to(root_path)))
                if len(documents) >= 100:
                    break

        return documents

    async def read_document(self, document_path: str = Field(..., description="Document path to read."),
                            pagination: int | float = Field(0.0, description="Pagination parameter.")) -> str:
        """
        Read the contents of a library's document.

        Library Read Instructions:
        1. For non-paginated documents (JSON, MD, TXT, XML, YAML, RTF), this tool reads the entire document contents.
        2. For paginated documents (PDF, DOCX, PPTX, Excel), this tool reads only specific pages/sections. Use pagination parameter strategically to target relevant content.
        3. Use pagination parameter as between 0.0 (inclusive) and 1.0 (exclusive) for percentile-based navigation or int (1+) for specific page numbers.
        4. When searching for specific information in large paginated documents, use a "soft" binary search approach:
        - Start with an educated percentile guess based on document type and target content (e.g., 0.8 for conclusions in academic papers, 0.3 for methodology)
        - Use the context from your initial read to refine your search. If you find related but not target content, adjust percentile accordingly
        - Iterate between percentile and page number paginations to pinpoint information as you narrow down the location
        - If initial pages show the document is irrelevant, abandon it quickly rather than exhaustively searching it.
        5. Use educated guesses for initial page positions based on document structure (e.g., table of contents near start, conclusions near end, etc.).
        6. Avoid over-paginating: don't read every page sequentially unless absolutely necessary for comprehensive understanding.
        """
        document_url = str(self.path / document_path)

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
                    from toolfront.models.documents.generic import GenericDocument

                    document = GenericDocument(url=document_url)

        except ImportError as e:
            raise ImportError(f"Import error: {e}. Please install 'toolfront[all]' or toolfront[doc]") from e
        except Exception as e:
            raise RuntimeError(f"Error reading document {document_path}: {e}") from e

        return await document.read(pagination)

    def _retrieve_class(self) -> type:
        return Read

    def _retrieve_function(self) -> Any:
        return self.read_document
