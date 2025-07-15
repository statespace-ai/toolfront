import logging
from abc import ABC
from contextlib import asynccontextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Self
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel

from toolfront.types import DatasourceType

logger = logging.getLogger("toolfront")

# Context variable to store datasources for the current context
_context_datasources: ContextVar[dict[str, "DataSource"]] = ContextVar(
    "context_datasources", default={})


def _get_type(url: str) -> DatasourceType:
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme

    if scheme in ("http", "https"):
        return DatasourceType.API
    elif scheme == "file":
        path = Path(parsed_url.path)
        if path.exists():
            if path.is_file() and path.suffix.lower() in [".json", ".yaml", ".yml"]:
                return DatasourceType.API
            elif path.is_dir():
                return DatasourceType.LIBRARY
        raise ConnectionError(f"Path does not exist: {path}")
    else:
        return DatasourceType.DATABASE


@asynccontextmanager
async def connect_async(urls: list[str]):
    from toolfront.models.datasources.api import API
    from toolfront.models.datasources.database import Database
    from toolfront.models.datasources.library import Library
    from toolfront.tools import api_tools, database_tools, library_tools

    # Create a context-local datasource cache
    context_cache = {}

    # Process all URLs and collect datasources and tools
    datasources = []
    all_tools = set()
    context = {"datasources": {}}

    for url in urls:
        datasource_type = _get_type(url)
        match datasource_type:
            case DatasourceType.API:
                datasource_class = API
                tools = api_tools
            case DatasourceType.LIBRARY:
                datasource_class = Library
                tools = library_tools
            case DatasourceType.DATABASE:
                datasource_class = Database
                tools = database_tools
            case _:
                raise ValueError(f"Invalid datasource type: {datasource_type}")

        # Create datasource and add to context cache
        datasource = datasource_class.create_from_url(url)
        datasources.append(datasource)

        # Store in context cache using original URL as key
        context_cache[datasource.sanitized_url()] = datasource

        # Add tools to set
        all_tools.update(tools)

        # Group URLs by datasource type
        type_str = str(datasource_type.value)
        if type_str not in context["datasources"]:
            context["datasources"][type_str] = []
        context["datasources"][type_str].append(datasource.sanitized_url())

    # Set the context variable
    token = _context_datasources.set(context_cache)

    try:
        yield yaml.dump(context), list(all_tools)
    finally:
        # Reset the context variable
        _context_datasources.reset(token)


class DataSource(BaseModel, ABC):
    """Abstract base class for all datasources."""

    def sanitized_url(self) -> str:
        raise NotImplementedError("Subclasses must implement sanitized_url")

    @classmethod
    def create_from_url(cls, url: str) -> "DataSource":
        raise NotImplementedError("Subclasses must implement create_from_url")

    @classmethod
    def load_from_sanitized_url(cls, sanitized_url: str) -> Self:
        context_cache = _context_datasources.get({})
        if sanitized_url not in context_cache:
            raise ValueError(f"Datasource {sanitized_url} not found")

        obj = context_cache[sanitized_url]
        if not isinstance(obj, cls):
            raise ValueError(
                f"Datasource {sanitized_url} is not a {cls.__name__}")
        return obj


def get_datasource_cache() -> dict[str, DataSource]:
    return _context_datasources.get({})
