import os
from importlib.resources import files
from pathlib import Path

import click
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/{full_path:path}")
async def serve_file(full_path: str):
    """
    Serve files from CONTENT_DIR.
    If path ends in / or file not found, serve index.md.
    Markdown files are rendered to HTML, SQL and others are plain text.
    """
    # Resolve requested path in content dir
    abs_path = Path(os.environ["CONTENT_DIR"]) / full_path
    
    # If it's a directory or doesn't exist, try index.md
    if abs_path.is_dir() or not abs_path.exists():
        abs_path = abs_path / "index.md"
    
    # Check file exists
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {full_path}")
    
    # Serve Markdown as HTML
    if str(abs_path).endswith(".md"):
        md_content = abs_path.read_text(encoding="utf-8")
        return PlainTextResponse(content=md_content)
    
    # Serve SQL or other files as plain text
    content = abs_path.read_text(encoding="utf-8")
    return PlainTextResponse(content=content)


@click.group()
def site():
    """Toolsite commands"""
    pass


@site.command()
@click.argument("path", type=click.Path(), required=True)
@click.option("--database", "-db", type=click.STRING, help="Database variable name")
@click.option("--api", type=click.STRING, help="API variable name")
@click.option("--documents", type=click.STRING, help="Documents variable name")
def create_page(path, database, api, documents):
    """Create a page from template (database, API, or documents)"""
    # Check mutual exclusivity
    options_provided = sum(bool(x) for x in [database, api, documents])
    if options_provided == 0:
        raise click.UsageError("You must provide exactly one of --database, --api, or --documents.")
    elif options_provided > 1:
        raise click.UsageError("Options --database, --api, and --documents are mutually exclusive.")
    
    # Determine target file path
    target_path = Path(path)
    
    # If path exists and is not a directory, error out
    if target_path.exists() and not target_path.is_dir():
        raise click.UsageError(f"Path {target_path} exists but is not a directory.")
    
    # If directory exists, ask for confirmation
    if target_path.exists() and target_path.is_dir():
        if not click.confirm(f"Directory {target_path} already exists. Continue and potentially overwrite files?"):
            click.echo("Operation cancelled.")
            return
    
    # Ensure target directory exists
    target_path.mkdir(parents=True, exist_ok=True)
    
    if database:
        # Handle database template
        md_template_file = files("cli") / "templates" / "markdown" / "database.md"
        sql_template_file = files("cli") / "templates" / "sql" / "database.sql"
        
        # Replace template variables
        processed_md = md_template_file.read_text().replace("<PLACEHOLDER>", database)
        processed_sql = sql_template_file.read_text().replace("<PLACEHOLDER>", database)
        
        # Write the processed templates to target files
        (target_path / "index.md").write_text(processed_md)
        (target_path / "index.sql").write_text(processed_sql)
        
        click.echo(f"Created SQL page: {target_path}")
        click.echo(f"Variable name: {database}")
        click.echo(f"Set your '{database}' variable before running queries.")
    
    elif api:
        # TODO: Handle API template
        click.echo(f"API template not implemented yet. Variable name: {api}")
        raise NotImplementedError("API template functionality not yet implemented")
    
    elif documents:
        # TODO: Handle documents template
        click.echo(f"Documents template not implemented yet. Variable name: {documents}")
        raise NotImplementedError("Documents template functionality not yet implemented")


@site.command()
@click.argument("path", type=click.Path(), default="./", required=False)
@click.option("--host", "-h", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", "-p", default=8000, help="Port to run the server on")
@click.option(
        "--autoreload/--no-autoreload",
        "-r",
        default=False,
        help="Reload the server on code changes",
)
def serve(path, host, port, autoreload):
    """Start a toolsite server in PATH"""
    os.environ["CONTENT_DIR"] = path
    uvicorn.run("cli.commands.site:app", host=host, port=port, reload=autoreload)
