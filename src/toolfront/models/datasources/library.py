from abc import ABC
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from markitdown import MarkItDown
from pydantic import Field, model_validator

from toolfront.models.actions.read import Read
from toolfront.models.datasources.base import DataSource

CHUNK_SIZE = 10000


class Library(DataSource, ABC):
    """Abstract base class for document libraries."""

    url: str = Field(..., description="Library URL.")

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

    async def glob_search_documents(
        self, pattern: str = Field(..., description="Glob pattern to search for.")
    ) -> list[str]:
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

    async def read_document(
        self,
        document_path: str = Field(..., description="Document path to read."),
        pagination: int | float = Field(
            0.0,
            description="Section navigation: 0.0-0.99 for percentile, >=1 for section number.",
        ),
    ) -> str:
        """
        Read the contents of a library's document with automatic chunking.

        All documents are automatically chunked into sections of 10,000 characters each for easier navigation.

        Library Read Instructions:
        1. Documents are split into 10k character chunks for all file types (PDF, DOCX, PPTX, Excel, JSON, MD, TXT, XML, YAML, RTF, HTML).
        2. Use pagination parameter to navigate through document sections:
           - 0.0 <= pagination < 1.0: Return section at that percentile (e.g., 0.5 = middle section)
           - pagination >= 1: Return specific section number (e.g., 1 = first section, 2 = second section)
        3. When searching for specific information in large documents, use a "soft" binary search approach:
           - Start with an educated percentile guess based on document type and target content (e.g., 0.8 for conclusions in academic papers, 0.3 for methodology)
           - Use the context from your initial read to refine your search. If you find related but not target content, adjust percentile accordingly
           - Iterate between percentile and section number paginations to pinpoint information as you narrow down the location
        4. Use educated guesses for initial positions based on document structure (e.g., table of contents near start, conclusions near end, etc.).
        5. Each returned section includes metadata showing "Section X of Y" for context.
        """

        document_type = document_path.split(".")[-1]

        if document_type in {"pptx", "docx", "xlsx", "xls", "pdf"}:
            md = MarkItDown()
            result = md.convert(self.path / document_path)
            document = result.markdown
        elif document_type in {"md", "txt", "json", "xml", "yaml", "yml", "rtf", "html"}:
            with (self.path / document_path).open("r", encoding="utf-8") as f:
                document = f.read()
        else:
            raise ValueError(f"Unsupported document type: {document_type}")

            # Calculate chunking parameters
        total_sections = (len(document) + CHUNK_SIZE - 1) // CHUNK_SIZE

        if total_sections == 0:
            return document

        # Determine section index and label based on pagination type
        if pagination < 1:
            # Percentile-based: convert to section index
            section_index = min(int(pagination * total_sections), total_sections - 1)
        else:
            section_index = min(int(pagination), total_sections - 1)

        start_idx = section_index * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(document))
        return f"Section {section_index + 1} of {total_sections}:\n\n{document[start_idx:end_idx]}"

    def _retrieve_class(self) -> type:
        return Read

    def _retrieve_function(self) -> Any:
        return self.read_document
