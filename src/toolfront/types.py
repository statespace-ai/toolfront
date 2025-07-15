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


class SearchMode(str, Enum):
    """Search mode."""

    REGEX = "regex"
    BM25 = "bm25"
    JARO_WINKLER = "jaro_winkler"


class DatabaseType(str, Enum):
    """Database type."""

    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    DUCKDB = "duckdb"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SNOWFLAKE = "snowflake"
    SQLITE = "sqlite"
    SQLSERVER = "sqlserver"

    @classmethod
    def from_drivername(cls, drivername: str) -> "DatabaseType":
        """Get DatabaseType from driver name."""
        driver_map = {
            "bigquery": cls.BIGQUERY,
            "databricks": cls.DATABRICKS,
            "duckdb": cls.DUCKDB,
            "mysql": cls.MYSQL,
            "postgresql": cls.POSTGRESQL,
            "postgres": cls.POSTGRESQL,  # alias
            "snowflake": cls.SNOWFLAKE,
            "sqlite": cls.SQLITE,
            "sqlserver": cls.SQLSERVER,
            "mssql": cls.SQLSERVER,  # alias
        }

        if drivername not in driver_map:
            raise ValueError(f"Unsupported database driver: {drivername}")

        return driver_map[drivername]

    def to_database_class(self):
        """Return the corresponding database class using lazy imports."""
        import importlib

        class_paths = {
            DatabaseType.BIGQUERY: "toolfront.models.databases.bigquery.BigQuery",
            DatabaseType.DATABRICKS: "toolfront.models.databases.databricks.Databricks",
            DatabaseType.DUCKDB: "toolfront.models.databases.duckdb.DuckDB",
            DatabaseType.MYSQL: "toolfront.models.databases.mysql.MySQL",
            DatabaseType.POSTGRESQL: "toolfront.models.databases.postgresql.PostgreSQL",
            DatabaseType.SNOWFLAKE: "toolfront.models.databases.snowflake.Snowflake",
            DatabaseType.SQLITE: "toolfront.models.databases.sqlite.SQLite",
            DatabaseType.SQLSERVER: "toolfront.models.databases.sqlserver.SQLServer",
        }

        if self not in class_paths:
            raise ValueError(f"Unsupported database type: {self}")

        import_path = class_paths[self]
        module_path, class_name = import_path.rsplit(".", 1)

        module = importlib.import_module(module_path)
        return getattr(module, class_name)


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
