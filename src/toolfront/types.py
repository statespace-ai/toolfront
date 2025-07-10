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


class DocumentType(str, Enum):
    """Document type."""

    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    EXCEL = "excel"
    JSON = "json"
    TXT = "txt"
    XML = "xml"
    YAML = "yaml"
    RTF = "rtf"
    MD = "md"

class SearchMode(str, Enum):
    """Search mode."""

    REGEX = "regex"
    BM25 = "bm25"
    JARO_WINKLER = "jaro_winkler"


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
