import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

import click

# from fake_database import Database  # Replace with your actual DB type
from mcp.server.fastmcp import FastMCP

from toolfront.models.datasources.base import connect

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)

logger.info("Starting ToolFront MCP server")


async def get_mcp(urls: tuple[str, ...]) -> FastMCP:
    @asynccontextmanager
    async def app_lifespan(server: FastMCP) -> AsyncIterator[None]:
        """Manage application lifecycle with type-safe context"""
        with connect(list(urls)) as (context, tools):
            # import pdb; pdb.set_trace()

            async def discover() -> dict:
                """
                ALWAYS CALL THIS FIRST TO DISCOVER THE AVAILABLE DATASOURCES
                """
                return context

            # Always include discover tool
            tools.append(discover)

            for tool in tools:
                server.add_tool(tool)

            logger.info(f"Started MCP with {len(urls)} datasources and {len(tools)} tools")

            try:
                yield
            finally:
                pass

    mcp = FastMCP("ToolFront MCP server", lifespan=app_lifespan)

    return mcp


@click.command()
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="stdio", help="Transport mode for MCP server")
@click.argument("urls", nargs=-1)
def main(transport: Literal["stdio", "sse"] = "stdio", urls: tuple[str, ...] = ()) -> None:
    logger.info("Starting MCP server")
    mcp_instance = asyncio.run(get_mcp(urls))
    mcp_instance.run(transport=transport)


if __name__ == "__main__":
    main()
