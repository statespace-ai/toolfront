import asyncio
import logging
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from functools import cached_property
from pathlib import Path
from typing import Any
from urllib import parse

import duckdb
import httpx
import yaml
from pydantic import BaseModel, Field, model_validator

from toolfront.config import TIMEOUT_SECONDS
from toolfront.models.base import DataSource
from toolfront.utils import (
    change_dir,
    parse_markdown_with_frontmatter,
    url_to_path,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("toolfront")

DEFAULT_CACHE_DIR = Path("toolfront_cache")
DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class ToolPage(BaseModel):
    url: str = Field(..., description="URL of the page.")
    markdown: str | None = Field(
        None, description="Markdown content of the page.")
    config: dict[str, Any] | None = Field(
        None, description="Config of the page.")

    headers: dict[str, str] | None = Field(
        None, description="HTTP headers for the page.")
    params: dict[str, str] | None = Field(
        None, description="Query parameters for the page.")

    model_config = {"arbitrary_types_allowed": True}

    _connection: duckdb.DuckDBPyConnection | None = None
    _path_cache: Path | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_model_before(cls, data: Any) -> Any:
        """Process raw data before model creation."""
        if isinstance(data, dict) and "url" in data:
            data["url"] = data["url"].rstrip("/") + "/"

            if "markdown" not in data or "config" not in data:
                with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
                    response = client.get(data["url"], params=data.get(
                        "params", {}), headers=data.get("headers", {}))
                    response.raise_for_status()
                    data["markdown"], data["config"] = parse_markdown_with_frontmatter(
                        response.text)

        return data

    def model_post_init(self, __context: Any) -> None:
        """Initialize DuckDB connection and cache files."""
        self._path_cache = DEFAULT_CACHE_DIR / url_to_path(self.url)
        self._path_cache.mkdir(parents=True, exist_ok=True)

        # Cache files if needed
        if self.query_paths or self.file_paths:
            with change_dir(DEFAULT_CACHE_DIR):
                parsed_url = parse.urlparse(self.url)

                try:
                    # Check if we're in an event loop
                    asyncio.get_running_loop()

                    def run_async_cache():
                        asyncio.run(self._cache_files(parsed_url))

                    with ThreadPoolExecutor() as executor:
                        executor.submit(run_async_cache).result()

                except RuntimeError:
                    # No event loop running, safe to use asyncio.run
                    asyncio.run(self._cache_files(parsed_url))

        with change_dir(self._path_cache):
            if self._connection is None:
                self._connection = duckdb.connect(":memory:")
                logger.debug("Created new DuckDB connection")
            else:
                logger.debug("Reusing existing DuckDB connection")

    @cached_property
    def title(self) -> str:
        """Return the title of the page."""
        return self.config.get("title", "")

    @cached_property
    def query_paths(self) -> list[str]:
        """Return the query paths of the page."""
        return self.config.get("queries", [])

    @cached_property
    def file_paths(self) -> list[str]:
        """Return the file paths of the page."""
        return self.config.get("files", [])

    @cached_property
    def content(self) -> str:
        """Return the content of the page."""
        static_content = self.static_content
        dynamic_content = self.dynamic_content
        content_dict = {
            "content": {
                "static": static_content,
                "dynamic": dynamic_content,
            },
            "queries": self.queries,
        }
        return yaml.dump(content_dict, sort_keys=False, default_flow_style=False)

    @cached_property
    def static_content(self) -> str:
        """Return a static context for the page."""
        return self.markdown

    @cached_property
    def dynamic_content(self) -> list[dict]:
        """Return a dynamic context for the page."""
        result = []
        queries = self.queries

        with change_dir(self._path_cache):
            for query in queries:
                try:
                    # Convert to dict and ensure it's JSON serializable
                    df_data = self._connection.sql(query).df().to_dict(orient="records")
                except Exception as e:
                    # Skip queries that fail (e.g., macro already exists)
                    if "already exists" in str(e):
                        logger.debug(f"Skipping query due to existing object: {e}")
                        continue
                    else:
                        logger.warning(f"Query failed: {e}")
                        continue
                # Clean the data to ensure it's serializable
                clean_data = []
                for record in df_data:
                    clean_record = {}
                    for k, v in record.items():
                        # Convert to basic Python types
                        if hasattr(v, 'item'):  # numpy types
                            clean_record[k] = v.item()
                        elif hasattr(v, 'isoformat'):  # datetime types
                            clean_record[k] = v.isoformat()
                        else:
                            clean_record[k] = v
                    clean_data.append(clean_record)
                result.append(clean_data)
        return result

    @cached_property
    def queries(self) -> list[str]:
        """Return the queries of the page."""
        result = []

        with change_dir(self._path_cache):
            for query_path in self.query_paths:
                if Path(query_path).exists() and (query_content := Path(query_path).read_bytes()):
                    query_sql = query_content.decode("utf-8")
                    result.append(query_sql)

        return result

    def query(self, sql: str) -> Any:
        """Execute a DuckDB query from the cached queries."""
        with change_dir(self._path_cache):
            try:
                return self._connection.sql(sql).fetchall()
            except Exception as e:
                if "already exists" in str(e):
                    logger.debug(f"Object already exists, continuing: {e}")
                    # Try to execute again if it was just a creation issue
                    return self._connection.sql(sql).fetchall()
                else:
                    raise

    async def _cache_files(self, parsed_url: parse.ParseResult) -> None:
        """Pre-fetch and cache all query and data files asynchronously and in parallel."""
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            tasks = []

            # Add tasks for all files
            for file_path in self.query_paths + self.file_paths:
                if file_path.startswith("/"):
                    file_url = parsed_url._replace(path=file_path)
                else:
                    file_url = parsed_url._replace(
                        path=parsed_url.path.lstrip("/") + file_path)

                tasks.append(asyncio.create_task(
                    self._fetch_and_cache_file_async(file_url, client)))

            # Execute all tasks in parallel
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _fetch_and_cache_file_async(self, file_url: parse.ParseResult, client: httpx.AsyncClient) -> bytes | None:
        """Fetch a file and cache it with original name and structure."""
        try:
            file_path = url_to_path(file_url.geturl())
            response = await client.get(file_url.geturl())
            response.raise_for_status()

            # Cache file with original name and directory structure
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(response.content)
        except Exception as e:
            logger.warning(f"Failed to fetch and cache file: {file_url}: {e}")
            return None


class Browser(DataSource, ABC):
    """Natural language interface for OpenAPI/Swagger APIs.

    Parameters
    ----------
    url : str
        Starting URL.
    headers : dict[str, str], optional
        HTTP headers for authentication.
    params : dict[str, str], optional
        Query parameters for all requests.
    """

    start_url: str = Field(..., description="Starting URL.")
    headers: dict[str, str] | None = Field(
        None, description="Additional headers to include in requests.", exclude=True)
    params: dict[str, str] | None = Field(
        None, description="Query parameters to include in requests.", exclude=True)

    _page: ToolPage | None

    def __init__(
        self,
        start_url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(start_url=start_url, headers=headers, params=params, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def tools(self) -> list[callable]:
        """Available tool methods for browser operations.

        Returns
        -------
        list[callable]
            Methods for macro execution and HTTP requests.
        """
        return [
            self.execute_macro,
            self.navigate,
        ]

    async def execute_macro(self, name: str, args: list[Any] | None = None, kwargs: dict[str, Any] | None = None) -> Any:
        """Execute a DuckDB macro from the cached queries.

        Instructions:
        1. Only execute macros that have been explicitly discovered or referenced in the latest URL.
        2. ALWAYS use positional arguments (args) for parameters without default values, in the order they are defined in the macro.
        3. ALWAYS use named arguments (kwargs) when the macro has default parameters defined with := syntax.
        4. When a macro execution fails or returns unexpected results, examine the macro definition and retry with correct parameters.
        """
        arg_parts = []

        # Handle positional arguments
        if args:
            arg_parts.extend([f"'{v}'" if isinstance(
                v, str) else str(v) for v in args])

        # Handle keyword arguments
        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, str):
                    arg_parts.append(f"{k} := '{v}'")
                else:
                    arg_parts.append(f"{k} := {v}")

        arg_str = ", ".join(arg_parts)
        macro_call = f"SELECT * FROM {name}({arg_str})"
        return self._page.query(macro_call)

    async def navigate(
        self,
        url: str,
    ) -> Any:
        """Navigate to a URL.

        Instructions:
        1. Only navigate to URLs that have been explicitly discovered, searched for, or referenced in the conversation.
        2. Before navigating, inspect the underlying URLs to understand their config and prevent errors.
        3. When a navigation fails or returns unexpected results, examine the URL to diagnose the issue and then retry.
        """
        self._page = ToolPage(url=url, headers=self.headers, params=self.params)
        return self._page.content
