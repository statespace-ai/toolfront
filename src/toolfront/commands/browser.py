import click
from mcp.server.fastmcp import FastMCP

from toolfront.environment import Environment


@click.group()
def browser():
    """Browser commands for MCP server functionality."""
    pass


@browser.command()
@click.argument("url", type=click.STRING, required=True)
@click.option(
    "--params",
    "-p",
    multiple=True,
    default=None,
    help="Authentication parameters for the filesystem protocol: KEY=VALUE",
)
@click.option("--host", type=click.STRING, default="127.0.0.1", help="Host to run the server on")
@click.option("--port", type=click.INT, default=8000, help="Port to run the server on")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable-http", "sse"]),
    default="stdio",
    help="Transport mode for MCP server",
)
@click.option("--env", type=click.STRING, default=None, help="Environment variables to pass to the server")
def serve(url, params, host, port, transport, env) -> None:
    """Start an MCP server with a browsing environment.

    Usage: `browser serve URL [OPTIONS]`

    Parameters
    ----------
    url : str
        Starting URL or file path for the environment
    params : tuple[str, ...]
        Authentication parameters for the filesystem protocol: KEY=VALUE
    host : str
        Host to run the server on
    port : int
        Port to run the server on
    transport : str
        Transport mode for MCP server
    env : str
        Environment variables to pass to the server: KEY=VALUE


    Example
    -------
    Start the browser MCP server with stdio transport pointing to a local directory:
    ```bash
    uvx toolfront browser serve file:///path/to/mysite --transport stdio
    ```


    Example
    -------
    Start the browser MCP server with streamable-http transport pointing to a S3 bucket:
    ```bash
    uvx toolfront browser serve s3:///path/to/mysite --transport streamable-http --params AWS_ACCESS_KEY_ID=1234567890 --params AWS_SECRET_ACCESS_KEY=1234567890
    ```

    Example
    -------
    Start the browser MCP server with sse transport pointing to a git repository:
    ```bash
    uvx toolfront browser serve git://path/to/mysite --transport sse --params GIT_TOKEN=1234567890
    ```
    """
    click.echo("Starting MCP server")

    environment = Environment(url=url, params=params, env=env)

    mcp = FastMCP("ToolFront MCP server", host=host, port=port)

    mcp.add_tool(environment.run_command)
    mcp.add_tool(environment.read_file)
    mcp.add_tool(environment.glob)

    # Only add search tool if index page exists
    if environment.index_page:
        mcp.add_tool(environment.search)

    click.echo("MCP server started successfully")
    mcp.run(transport=transport)
