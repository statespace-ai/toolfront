from pathlib import Path
from typing import Any

from markitdown import MarkItDown
from pydantic import Field, model_validator

from toolfront.config import CHUNK_SIZE, MARKITDOWN_TYPES, TEXT_TYPES
from toolfront.models.base import DataSource


class Document(DataSource):
    """Abstract base class for document libraries."""

    filepath: str | None = Field(
        default=None,
        description="Document path content. If None, the document content is provided directly. Mutually exclusive with text.",
    )
    text: str = Field(
        description="Document content. If None, the document path is provided directly. Mutually exclusive with filepath.",
        exclude=True,
    )

    def __init__(self, filepath: str | None = None, text: str | None = None, **kwargs: Any) -> None:
        super().__init__(filepath=filepath, text=text, **kwargs)

    @model_validator(mode="before")
    def validate_model(cls, v: Any) -> Any:
        filepath_value = v.get("filepath")
        text_value = v.get("text")

        # Validate mutual exclusivity
        if filepath_value is not None and text_value is not None:
            raise ValueError("filepath and text cannot be provided together.")

        if filepath_value is None and text_value is None:
            raise ValueError("Either filepath or text must be provided.")

        # If text is provided, we're done
        if filepath_value is None:
            return v

        # Process filepath
        filepath = Path(filepath_value)
        if not filepath.exists():
            raise ValueError(f"Document path does not exist: {filepath}")

        # Extract file extension (without the dot)
        document_type = filepath.suffix[1:].lower() if filepath.suffix else ""

        # Read document based on type
        document_content = cls._read_document_content(filepath, document_type)
        v["text"] = document_content

        return v

    @classmethod
    def _read_document_content(cls, filepath: Path, document_type: str) -> str:
        """Read document content based on file type."""
        if document_type in MARKITDOWN_TYPES:
            md = MarkItDown()
            result = md.convert(filepath)
            return result.markdown
        elif document_type in TEXT_TYPES:
            return filepath.read_text(encoding="utf-8")
        else:
            raise ValueError(f"Unsupported document type: {document_type}")

    def tools(self) -> list[callable]:
        return [self.read_document]

    async def read_document(
        self,
        pagination: int | float = Field(
            ..., description="Section navigation: 0.0-0.99 for percentile, >=1 for section number."
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
        5. NEVER continue reading through the rest of the document unnecessarily once you have found the answer.
        """
        # Use the text content for chunking
        document_content = self.text

        # Calculate chunking parameters
        total_sections = (len(document_content) + CHUNK_SIZE - 1) // CHUNK_SIZE

        if total_sections == 0:
            return document_content

        # Determine section index and label based on pagination type
        if pagination < 1:
            # Percentile-based: convert to section index
            section_index = min(int(pagination * total_sections), total_sections - 1)
        else:
            section_index = min(int(pagination), total_sections) - 1

        start_idx = section_index * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(document_content))
        return f"Section {section_index + 1} of {total_sections}:\n\n{document_content[start_idx:end_idx]}"
