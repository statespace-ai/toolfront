from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    TXT = "txt"
    JSON = "json"
    YAML = "yaml"
    XML = "xml"
    RTF = "rtf"


document_map = {
    "pdf": (DocumentType.PDF, "PDF"),
    "docx": (DocumentType.DOCX, "DocX"),
    "pptx": (DocumentType.PPTX, "PowerPoint"),
    "txt": (DocumentType.TXT, "TXT"),
    "json": (DocumentType.JSON, "JSON"),
    "yaml": (DocumentType.YAML, "YAML"),
    "xml": (DocumentType.XML, "XML"),
    "rtf": (DocumentType.RTF, "RTF"),
}

__all__ = ["DocumentType"]
