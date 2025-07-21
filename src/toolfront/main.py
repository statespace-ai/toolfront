import asyncio
import logging
from typing import Literal

import click
from mcp.server.fastmcp import FastMCP

from toolfront.models.base import DataSource

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)


async def get_mcp(url: str) -> FastMCP:
    import pdb; pdb.set_trace()
    datasource = DataSource.from_url(url)

    async def discover() -> dict:
        """
        ALWAYS CALL THIS FIRST TO DISCOVER THE AVAILABLE DATASOURCES
        """
        return datasource.context()

    mcp = FastMCP("ToolFront MCP server")


    mcp.add_tool(discover)

    for tool in datasource.tools():
        import pdb; pdb.set_trace()
        docs = tool.__doc__
        mcp.add_tool(tool)



    logger.info("Started ToolFront MCP server")

    return mcp


@click.command()
@click.argument("url", type=click.STRING, required=True)
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="stdio", help="Transport mode for MCP server")
def main(url: str, transport: Literal["stdio", "sse"] = "stdio") -> None:
    logger.info("Starting MCP server")
    mcp_instance = asyncio.run(get_mcp(url))
    mcp_instance.run(transport=transport)


if __name__ == "__main__":
    main()
