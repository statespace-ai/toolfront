import json

import click
from mcp.server.fastmcp import FastMCP

from toolfront.models import Browser


class JSONType(click.ParamType):
    name = "json"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON: {e}", param, ctx)


JSON = JSONType()


@click.group()
def browser():
    """Browser commands"""
    pass


@browser.command()
@click.argument("url", type=click.STRING, required=True)
@click.option("--setup-sql", type=click.STRING, default="", help="Path to SQL file to execute when loading a page")
@click.option("--headers", type=JSON, default=None, help="Headers to include in the request")
@click.option("--params", type=JSON, default=None, help="Query parameters to include in the request")
@click.option("--host", type=click.STRING, default="127.0.0.1", help="Host to run the server on")
@click.option("--port", type=click.INT, default=8000, help="Port to run the server on")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable-http", "sse"]),
    default="stdio",
    help="Transport mode for MCP server",
)
def serve(url, setup_sql, headers, params, host, port, transport) -> None:
    browser = Browser(url=url, setup_sql=setup_sql, headers=headers, params=params)

    mcp = FastMCP("ToolFront MCP server", instructions=browser.instructions(), host=host, port=port)

    for tool in browser.tools():
        mcp.add_tool(tool, description=tool.__doc__)

    return mcp.run(transport=transport)
