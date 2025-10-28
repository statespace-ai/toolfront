import os
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any

import click
import uvicorn
import yaml
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, field_validator


class ActionRequest(BaseModel):
    """Request body for action endpoint."""

    command: list[str]
    args: dict[str, str] | None = None
    env: dict[str, str] | None = None

    @field_validator("args", mode="before")
    @classmethod
    def validate_args(cls, args: dict[str, str] | None) -> dict[str, str]:
        if args is None:
            return {}
        return args


def get_frontmatter(markdown: str) -> dict[str, Any]:
    """Parse frontmatter from markdown content.

    Supports both YAML (--- ... ---) and TOML (+++ ... +++) frontmatter formats.
    """
    # Try YAML frontmatter (--- ... ---)
    yaml_pattern = r"^\n*---\s*\n(.*?)\n---\s*\n(.*)"
    if match := re.match(yaml_pattern, markdown, re.DOTALL):
        try:
            return yaml.safe_load(match.group(1))
        except Exception:
            return {}

    # Try TOML frontmatter (+++ ... +++)
    toml_pattern = r"^\n*\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)"
    if match := re.match(toml_pattern, markdown, re.DOTALL):
        try:
            return tomllib.loads(match.group(1))
        except Exception:
            return {}

    return {}


def resolve_file_path(directory: Path, file_path: str) -> str:
    """Resolve and validate a file path.

    Simple resolution logic:
    - If path ends with .md: use as-is
    - Otherwise: try path/README.md
    """
    full_path = (directory / file_path).resolve()

    # Security check
    if not full_path.is_relative_to(directory):
        raise HTTPException(status_code=403, detail="Access denied: path outside served directory")

    # If path ends with .md, use it directly
    if file_path.endswith(".md"):
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        if not full_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        return str(full_path)

    # Otherwise, try path/README.md
    readme_path = full_path / "README.md"
    if readme_path.exists() and readme_path.is_file():
        return str(readme_path)

    raise HTTPException(status_code=404, detail="File not found (tried README.md)")


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--host", default="127.0.0.1", help="Host to bind the server to")
@click.option("--port", default=8000, type=int, help="Port to bind the server to")
def serve(directory, host, port):
    """Serve files from a directory via HTTP"""
    directory = Path(directory).resolve()

    # check if README.md exists in the directory
    if not (directory / "README.md").exists():
        raise HTTPException(status_code=400, detail="README.md not found in directory")

    app = FastAPI(title="ToolFront Application")

    @app.get("/{file_path:path}")
    async def read_file(file_path: str):
        """Read a file from the served directory"""
        full_path = resolve_file_path(directory, file_path)
        return FileResponse(full_path)

    @app.post("/{file_path:path}")
    async def action(file_path: str, action: ActionRequest = Body(...)):
        """Execute a command defined in a file's frontmatter"""
        command = action.command
        args = action.args

        # Resolve file path
        full_path = resolve_file_path(directory, file_path)
        path = Path(full_path)

        # Parse frontmatter and validate command
        frontmatter = get_frontmatter(path.read_text())
        if not frontmatter:
            raise HTTPException(status_code=400, detail=f"No frontmatter found in: {path}")

        tools = frontmatter.get("tools", {})
        if not tools:
            raise HTTPException(status_code=400, detail=f"No tools found in frontmatter of: {path}")

        if not any(command[: len(t)] == t for t in tools):
            raise HTTPException(status_code=400, detail=f"Invalid command: {command}. Must be one of: {tools}")

        # Expand placeholders in command and replace arguments with values
        expanded_command = [os.path.expandvars(c).format(**args) for c in command]

        result = subprocess.run(expanded_command, cwd=path.parent, env=action.env, capture_output=True, text=True)

        return JSONResponse(
            {"stdout": result.stdout or "N/A", "stderr": result.stderr or "N/A", "returncode": result.returncode}
        )

    click.echo(f"Starting ToolFront server on {host}:{port}")
    click.echo(f"Serving files from: {directory}")
    click.echo(f"GET  http://{host}:{port}/path/to/file.md - Read file")
    click.echo(f"POST http://{host}:{port}/path/to/file.md - Execute command")

    uvicorn.run(app, host=host, port=port)
