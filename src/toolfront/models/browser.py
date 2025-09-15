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
import sqlparse
from pydantic import BaseModel, Field, PrivateAttr, model_validator

from toolfront.config import TIMEOUT_SECONDS
from toolfront.models.base import DataSource
from toolfront.utils import (
    change_dir,
    parse_markdown_with_frontmatter,
    url_to_path,
)

logger = logging.getLogger("toolfront")

DEFAULT_CACHE_DIR = Path("toolfront_cache")
DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class ToolPage(BaseModel):
    url: str = Field(..., description="URL of the page.")
    markdown: str | None = Field(None, description="Markdown content of the page.")
    config: dict[str, Any] | None = Field(None, description="Config of the page.")
    headers: dict[str, str] | None = Field(None, description="HTTP headers for the page.", exclude=True)
    params: dict[str, str] | None = Field(None, description="Query parameters for the page.", exclude=True)
    variables: dict[str, str] | None = Field(None, description="Variables for the page.", exclude=True)
    
    model_config = {"arbitrary_types_allowed": True}
    
    _connection: duckdb.DuckDBPyConnection | None = None
    _path_cache: Path | None = None
    
    @model_validator(mode="before")
    @classmethod
    def validate_model_before(cls, data: Any) -> Any:
        """Process raw data before model creation."""
        if isinstance(data, dict) and "url" in data:
            url = data["url"]
            
            # Validate URL format
            parsed = parse.urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid URL: {url}. Must include scheme and netloc.")
            
            data["url"] = data["url"].rstrip("/") + "/"
            
            if "markdown" not in data or "config" not in data:
                with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
                    response = client.get(data["url"], params=data.get("params", {}), headers=data.get("headers", {}))
                    response.raise_for_status()
                    data["markdown"], data["config"] = parse_markdown_with_frontmatter(response.text)
        
        return data
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize DuckDB connection and cache files."""
        self._path_cache = DEFAULT_CACHE_DIR / url_to_path(self.url)
        self._path_cache.mkdir(parents=True, exist_ok=True)
        
        # Cache files if needed
        if len(self.config.get("import", [])):
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
    
    @property
    def title(self) -> str:
        """Return the title of the page."""
        return self.config.get("title", "")
    
    @property
    def content(self) -> str:
        """Return the content of the page."""
        return f"<{self.title}>\n{self.markdown}\n{self.dynamic_content}\n</{self.title}>"
    
    @cached_property
    def dynamic_content(self) -> list[dict]:
        """Return a dynamic context for the page."""
        
        queries = []
        content = ""
        
        with change_dir(self._path_cache):
            self._connection = duckdb.connect(":memory:")
            
            if self.variables:
                for k, v in self.variables.items():
                    self._connection.execute(f"SET VARIABLE {k} = {f"'{v}'" if isinstance(v, str) else v};")
            
            for import_path in self.config.get("import", []):
                if (
                        Path(import_path).exists()
                        and str(import_path).endswith(".sql")
                        and (query_content := Path(import_path).read_bytes())
                ):
                    queries.append(query_content.decode("utf-8"))
            
            if queries:
                content += "\n## SQL\n"
                for query in queries:
                    query_content = ""
                    for sub_query in sqlparse.split(query):
                        if df_data := self._connection.query(sub_query):
                            query_content += f"\n{df_data.df().to_markdown()}\n"
                    
                    content += f"### Query:\n```sql\n{query}\n```\n"
                    if query_content:
                        content += f"### Result:\n{query_content}\n"
        return content
    
    def query(self, sql: str) -> Any:
        """Execute a DuckDB query from the cached queries."""
        with change_dir(self._path_cache):
            result = self._connection.sql(sql)
            if result:
                result = result.df().to_markdown()
            return result
    
    async def _cache_files(self, parsed_url: parse.ParseResult) -> None:
        """Pre-fetch and cache all query and data files asynchronously and in parallel."""
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            tasks = []
            
            # Add tasks for all files
            for import_path in self.config.get("import", []):
                if import_path.startswith("/"):
                    import_url = parsed_url._replace(path=import_path)
                else:
                    import_url = parsed_url._replace(path=parsed_url.path.lstrip("/") + import_path)
                
                tasks.append(asyncio.create_task(self._fetch_and_cache_file_async(import_url, client)))
            
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
    setup_sql: str | None, optional
        Path or content of SQL to execute when loading a page.
    headers : dict[str, str], optional
        HTTP headers for authentication.
    params : dict[str, str], optional
        Query parameters for all requests.
    """
    
    url: str = Field(..., description="Starting URL.")
    headers: dict[str, str] | None = Field(None, description="Additional headers to include in requests.", exclude=True)
    params: dict[str, str] | None = Field(None, description="Query parameters to include in requests.", exclude=True)
    variables: dict[str, str] | None = Field()
    _page: ToolPage | None = PrivateAttr(None)
    
    def __init__(
            self,
            url: str,
            headers: dict[str, str] | None = None,
            params: dict[str, str] | None = None,
            variables: dict[str, str] | None = None,
            **kwargs: Any,
    ) -> None:
        if variables is None and kwargs is not None:
            variables = kwargs
        super().__init__(url=url, headers=headers, params=params, variables=variables)
    
    @model_validator(mode="after")
    def validate_browser(self) -> Any:
        """Validate the page."""
        self.navigate(self.url)
        return self
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url='{self._page.url}')"
    
    def instructions(self, context: str | None = None) -> str:
        parent_instructions = super().instructions(context=context)
        return f"{parent_instructions}\n\n{self._page.content}"
    
    def tools(self) -> list[callable]:
        """Available tool methods for browser operations."""
        return [
            self.execute_macro,
            self.navigate,
        ]
    
    def execute_macro(
            self, name: str, args: list[Any] | None = None, kwargs: dict[str, Any] | None = None
    ) -> Any:
        """Execute a DuckDB macro.

        ONLY EXECUTE MACROS FOUND IN THE CURRENT PAGE CONTENT.
        FAILURE TO PROPERLY IDENTIFY AND PASS POSITIONAL AND NAMED ARGUMENTS WILL CAUSE ERRORS.
        ALWAYS FOLLOW THE MACRO'S INSTRUCTION COMMENTS.

        Instructions:
        1. Examine macro definition to understand its purpose and parameters.
        2. Parameters WITHOUT := are REQUIRED and go to `args` list in exact definition order.
        3. Parameters WITH := are OPTIONAL with default values and go to `kwargs` dict using exact names.
        4. If all parameters have := pass everything via kwargs.
        5. When execution fails examine macro definition and adjust parameters accordingly.

        Examples:
        macro add(a, b) → args=[1, 2], kwargs=None
        macro sum(a, b := 5) → args=[1], kwargs={"b": 2}
        macro user_activity(limit_k := 10, interval_days := 7) → args=None, kwargs={"interval_days": 7}
        """
        arg_parts = []
        
        # Handle positional arguments
        if args:
            arg_parts.extend([f"'{v}'" if isinstance(v, str) else str(v) for v in args])
        
        # Handle keyword arguments
        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, str):
                    arg_parts.append(f"{k} := '{v}'")
                else:
                    arg_parts.append(f"{k} := {v}")
        
        arg_str = ", ".join(arg_parts)
        macro_call = f"SELECT * FROM {name}({arg_str})"
        
        try:
            return self._page.query(macro_call)
        except Exception as e:
            raise e
    
    def navigate(
            self,
            url: str,
    ) -> Any:
        """Navigate to a page.

        ONLY NAVIGATE TO COMPLETE URLS WITH PROTOCOL AND DOMAIN.
        RELATIVE URLS OR RESOURCE PATHS WILL CAUSE ERRORS.

        Instructions:
        1. Use only URLs discovered in current page content or conversation.
        2. Ensure URL includes protocol (http/https) and full domain name.
        3. Verify URL format matches discovered links before navigation.
        4. After successful navigation examine returned content for available macros and links.
        5. When navigation fails check URL syntax and retry with corrected format.
        """
        
        self._page = ToolPage(url=url, headers=self.headers, params=self.params, variables=self.variables)
        return self._page.content
