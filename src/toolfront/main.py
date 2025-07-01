import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Literal
from urllib.parse import parse_qs, urlparse, urlunparse

import click
import diskcache
import httpx
import jsonref
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from toolfront.config import API_KEY_HEADER, BACKEND_URL
from toolfront.models.connection import Connection
from toolfront.tools import (
    discover,
    inspect_endpoint,
    inspect_table,
    query_database,
    request_api,
    sample_table,
    search_endpoints,
    search_queries,
    search_tables,
)

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)

_cache = diskcache.Cache(".toolfront_cache")


def get_openapi_spec(url: str) -> dict | None:
    """Get OpenAPI spec with retries if cached result is None."""
    cache_key = url

    # Check if we have a cached result
    if cache_key in _cache:
        cached_result = _cache[cache_key]
        if cached_result is not None:
            logger.debug(f"Cache hit for {url}")
            return cached_result
        else:
            # Remove None from cache and retry
            logger.debug(f"Cached None for {url}, removing and retrying")
            del _cache[cache_key]

    # Download and cache if successful
    try:
        logger.debug(f"Downloading OpenAPI spec for {url}")
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            spec = response.json()

            parsed_spec = jsonref.replace_refs(spec)
            # Only cache non-None results
            _cache.set(cache_key, parsed_spec, expire=3600)  # 1 hour TTL
            logger.info(f"Successfully retrieved spec for {url}")
            return parsed_spec
    except Exception as e:
        logger.warning(f"Failed to retrieve spec from {url}: {e}")
        return None


@dataclass
class AppContext:
    http_session: httpx.AsyncClient | None = None
    url_map: dict = Field(default_factory=dict)


async def process_datasource(url: str) -> tuple[str, dict]:
    """Process datasource: parse, download spec, test connection"""

    parsed = urlparse(url)
    extra = {}

    if parsed.scheme in ("http", "https"):
        spec = get_openapi_spec(url)

        url = spec.get("servers", [{}])[0].get("url", None)

        # If no API URL is provided, use the parsed URL
        if url is None:
            url = parsed.netloc
        else:
            # If the API URL is a relative path, prepend the parsed URL
            if url.startswith("/"):
                url = f"https://{parsed.netloc}{url}"

        # Parse query parameters into a dictionary
        query_params = parse_qs(parsed.query)
        # Convert from lists to single values and exclude api_key
        extra = {"openapi_spec": spec, "query_params": query_params}

    else:
        netloc = parsed.netloc.replace(parsed.password, "***") if parsed.password else parsed.netloc
        url = urlunparse((parsed.scheme, netloc, parsed.path, "", "", ""))

    url_map = {url: {"parsed": parsed, "extra": extra}}

    result = await Connection.from_url(url).test_connection(url_map=url_map)
    if result.connected:
        logger.warning(f"Connection successful to {url}")
    else:
        logger.warning(f"Connection failed to {url}: {result.message}")

    return url_map


async def get_mcp(urls: tuple[str, ...], api_key: str | None = None) -> FastMCP:
    cleaned_urls = [url.lstrip("'").rstrip("'") for url in urls]

    # Process all datasources concurrently
    datasource_results = await asyncio.gather(*[process_datasource(url) for url in cleaned_urls])

    # Build url_map from results
    url_map = {k: v for d in datasource_results for k, v in d.items()}

    @asynccontextmanager
    async def app_lifespan(mcp_server: FastMCP) -> AsyncIterator[AppContext]:
        """Manage application lifecycle with type-safe context"""
        if api_key:
            headers = {API_KEY_HEADER: api_key}
            async with httpx.AsyncClient(headers=headers, base_url=BACKEND_URL) as http_client:
                yield AppContext(http_session=http_client, url_map=url_map)
        else:
            yield AppContext(url_map=url_map)

    mcp = FastMCP("ToolFront MCP server", lifespan=app_lifespan)

    mcp.add_tool(discover)
    mcp.add_tool(inspect_endpoint)
    mcp.add_tool(inspect_table)
    mcp.add_tool(query_database)
    mcp.add_tool(request_api)
    mcp.add_tool(sample_table)
    mcp.add_tool(search_endpoints)
    mcp.add_tool(search_tables)

    if api_key:
        mcp.add_tool(search_queries)

    return mcp


@click.command()
@click.option("--api-key", envvar="KRUSKAL_API_KEY", help="API key for authentication")
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="stdio", help="Transport mode for MCP server")
@click.argument("urls", nargs=-1)
def main(api_key: str | None = None, transport: Literal["stdio", "sse"] = "stdio", urls: tuple[str, ...] = ()) -> None:
    """ToolFront CLI - Run the MCP server"""
    logger.info("Starting MCP server with urls: %s", urls)
    mcp_instance = asyncio.run(get_mcp(urls, api_key))
    mcp_instance.run(transport=transport)


if __name__ == "__main__":
    main()
