import asyncio
import logging
import os
from pathlib import Path
from typing import Literal
from urllib.parse import quote

import click
from mcp.server.fastmcp import FastMCP

from toolfront.models.base import DataSource

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)


def load_env_file(env_file: Path = Path(".env")) -> None:
    """Load environment variables from .env file."""
    if not env_file.exists():
        return

    logger.info(f"Loading environment variables from {env_file}")
    with env_file.open() as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def process_database_url(url: str) -> str:
    """Process database URL with password substitution and encoding."""
    if "{password}" in url:
        password = os.getenv("DATABASE_PASSWORD")
        if password:
            encoded_password = quote(password, safe="")
            url = url.format(password=encoded_password)
            logger.info("Substituted and encoded DATABASE_PASSWORD into URL")
        else:
            logger.warning("URL contains {password} placeholder but DATABASE_PASSWORD env var not found")

    return url


async def get_mcp(url: str) -> FastMCP:
    processed_url = process_database_url(url)
    datasource = DataSource.from_url(processed_url)

    async def context() -> dict:
        """
        ALWAYS CALL THIS FIRST TO RETRIEVE THE CONTEXT FOR THE TASK.
        THEN, FOLLOW THE INSTRUCTIONS IN THE CONTEXT TO COMPLETE THE TASK.
        """
        return datasource.context()

    mcp = FastMCP("ToolFront MCP server")

    mcp.add_tool(context)

    for tool in datasource.tools():
        mcp.add_tool(tool, description=tool.__doc__)

    logger.info("Started ToolFront MCP server")

    return mcp


@click.command()
@click.argument("url", type=click.STRING, required=False)
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="stdio", help="Transport mode for MCP server")
@click.option("--env-file", type=click.Path(path_type=Path), default=".env", help="Path to .env file")
def main(url: str | None = None, transport: Literal["stdio", "sse"] = "stdio", env_file: Path = Path(".env")) -> None:
    logger.info("Starting MCP server")

    load_env_file(env_file)

    if not url:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise click.ClickException(
                "No database URL provided. Either:\n"
                "  1. Pass URL as argument: uvx toolfront 'mssql://user:{password}@host'\n"
                "  2. Set DATABASE_URL in .env file"
            )

    mcp_instance = asyncio.run(get_mcp(url))
    mcp_instance.run(transport=transport)


if __name__ == "__main__":
    main()
