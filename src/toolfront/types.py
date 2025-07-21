from dataclasses import dataclass
from enum import Enum


class HTTPMethod(str, Enum):
    """Valid HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

    @classmethod
    def get_supported_methods(cls) -> set[str]:
        """Get all supported HTTP methods."""
        return {method.value for method in cls}


class DocumentType(str, Enum):
    """Document type."""

    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    XLS = "xls"
    JSON = "json"
    TXT = "txt"
    XML = "xml"
    YAML = "yaml"
    YML = "yml"
    RTF = "rtf"
    MD = "md"

    @classmethod
    def from_file(cls, file_path: str) -> "DocumentType":
        try:
            return cls(file_path.split(".")[-1].lower())
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid file extension in path: {file_path}") from e

    @classmethod
    def get_supported_extensions(cls) -> set[str]:
        """Get all supported document extensions."""
        return {f".{doc_type.value}" for doc_type in cls}


@dataclass
class ConnectionResult:
    """Result of a database connection test."""

    connected: bool
    message: str


class DatasourceType(str, Enum):
    """Datasource type."""

    LIBRARY = "library"
    DATABASE = "database"
    API = "api"
