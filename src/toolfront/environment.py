import logging
import re
import subprocess
import tomllib
from enum import Enum
from typing import Any
from urllib.parse import parse_qsl, urlparse, urlunparse

import yaml
from fsspec import filesystem
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator, model_validator

from toolfront.utils import clean_url

logger = logging.getLogger("toolfront")


def get_frontmatter(markdown: str) -> dict[str, Any]:
    """Parse frontmatter from markdown content.

    Supports both YAML (--- ... ---) and TOML (+++ ... +++) frontmatter formats.

    Parameters
    ----------
    markdown : str
        Raw markdown content with optional frontmatter

    Returns
    -------
    dict[str, Any]
        Parsed frontmatter as dict (empty dict if no frontmatter found)
    """
    # Try YAML frontmatter (--- ... ---)
    yaml_pattern = r"^\n*---\s*\n(.*?)\n---\s*\n(.*)"
    if match := re.match(yaml_pattern, markdown, re.DOTALL):
        try:
            return yaml.safe_load(match.group(1))
        except Exception as e:
            logger.warning(f"Failed to parse YAML frontmatter: {e}")
            return {}

    # Try TOML frontmatter (+++ ... +++)
    toml_pattern = r"^\n*\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)"
    if match := re.match(toml_pattern, markdown, re.DOTALL):
        try:
            return tomllib.loads(match.group(1))
        except Exception as e:
            logger.warning(f"Failed to parse TOML frontmatter: {e}")
            return {}

    return {}


class OutputMode(str, Enum):
    """Output modes for search."""

    CONTENT = "content"
    FILES_WITH_MATCHES = "files_with_matches"
    COUNT = "count"


class CommandOutput(BaseModel):
    """Output of a command."""

    stdout: str = Field(..., description="Standard output of the command.")
    stderr: str = Field(..., description="Standard error of the command.")


class GlobOutput(BaseModel):
    """Output for glob mode."""

    matches: list[str] = Field(..., description="Array of matching file paths")
    count: int = Field(..., description="Number of matches")
    url_pattern: str = Field(..., description="URL pattern used")


class ReadFileOutput(BaseModel):
    """File read operation output."""

    content: str = Field(..., description="File content with line numbers")
    total_lines: int = Field(..., description="Total number of lines in file")
    lines_returned: int = Field(..., description="Lines returned")


class SearchResult(BaseModel):
    """Single BM25 search result."""

    file: str = Field(..., description="File path containing the match")
    score: float = Field(..., description="BM25 relevance score")
    content: str = Field(..., description="Matching document content")


class SearchOutput(BaseModel):
    """BM25 search output."""

    results: list[SearchResult] = Field(..., description="Search results ranked by BM25 score")
    total_results: int = Field(..., description="Total number of results found")
    terms: str = Field(..., description="Search terms used")


class GrepMatch(BaseModel):
    """Single grep match result."""

    file: str = Field(..., description="File path containing the match")
    line_number: int | None = Field(None, description="Line number of the match")
    line: str = Field(..., description="Matching line content")
    before_context: list[str] | None = Field(None, description="Lines before the match")
    after_context: list[str] | None = Field(None, description="Lines after the match")


class GrepContentOutput(BaseModel):
    """Grep output for content mode with match details."""

    matches: list[GrepMatch] = Field(..., description="List of matches with content")
    total_matches: int = Field(..., description="Total number of matches found")


class GrepFilesOutput(BaseModel):
    """Grep output for files_with_matches mode."""

    files: list[str] = Field(..., description="Files containing matches")
    count: int = Field(..., description="Number of files with matches")


class GrepCountOutput(BaseModel):
    """Grep output for count mode."""

    total_matches: int = Field(..., description="Total number of matches across all files")


class Environment(BaseModel):
    """Environment for managing filesystem operations and document search.

    Attributes
    ----------
    url : str
        Root URL for the environment - all operations must be within this URL
    params : dict[str, str] | None
        Authentication parameters for filesystem protocols
    env : dict[str, str] | None
        Environment variables for command execution
    home_page : str | None
        Home page URL (file if URL is a file, else index.md in directory)
    """

    url: str = Field(..., description="Root URL for the environment")
    params: dict[str, str] | None = Field(
        default=None, description="Filesystem authentication parameters", exclude=True
    )
    env: dict[str, str] | None = Field(default=None, description="Environment variables for commands", exclude=True)
    home_page: str | None = Field(default=None, description="Home page for the environment")

    _fs: Any = PrivateAttr(None)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("params", mode="before")
    @classmethod
    def validate_params(cls, params: dict[str, str] | list[str] | tuple | None) -> dict[str, str] | None:
        """Convert list of KEY=VALUE strings to dict."""
        if isinstance(params, list | tuple):
            return dict(param.split("=", 1) for param in params)
        return params

    @field_validator("env", mode="before")
    @classmethod
    def validate_env(cls, env: dict[str, str] | list[str] | tuple | None) -> dict[str, str] | None:
        """Convert list of KEY=VALUE strings to dict."""
        if isinstance(env, list | tuple):
            return dict(env_var.split("=", 1) for env_var in env)
        return env

    @model_validator(mode="after")
    def _initialize_filesystem(self) -> "Environment":
        """Initialize filesystem and determine home/index pages."""
        url = clean_url(self.url)
        parsed = urlparse(url)

        # Setup filesystem with auth params
        kwargs = dict(parse_qsl(parsed.query, keep_blank_values=True))
        if self.params:
            kwargs.update(self.params)

        self._fs = filesystem(parsed.scheme, **kwargs)

        # Determine home page and normalize URL
        if self._fs.isfile(parsed.path):
            self.home_page = url
            parent_path = parsed.path.rsplit("/", 1)[0] if "/" in parsed.path else ""
            self.url = urlunparse((parsed.scheme, parsed.netloc, parent_path, "", "", ""))
        elif self._fs.isdir(parsed.path):
            self.url = url
            home_page = f"{parsed.path.rstrip('/')}/index.md"
            if self._fs.isfile(home_page):
                self.home_page = home_page
        else:
            raise ValueError(f"URL does not point to a valid file or directory: {url}")

        return self

    def _validate_url(self, url: str, require_type: str | None = None):
        """Validate URL is within environment root.

        Parameters
        ----------
        url : str
            URL to validate
        require_type : str | None
            Required type: 'file', 'directory', or None

        Returns
        -------
        ParseResult
            Parsed and validated URL

        Raises
        ------
        ValueError
            If URL is outside environment root or doesn't match required type
        FileNotFoundError
            If file is required but doesn't exist
        """
        url = clean_url(url)
        parsed = urlparse(url)
        root_parsed = urlparse(self.url)

        # Validate scheme and netloc match
        if parsed.scheme != root_parsed.scheme:
            raise ValueError(f"URL scheme must match environment root: {url} (expected {root_parsed.scheme}://)")

        if parsed.netloc != root_parsed.netloc:
            raise ValueError(
                f"URL domain must match environment root: {url} (expected {root_parsed.scheme}://{root_parsed.netloc})"
            )

        # Validate path is within root
        root_path = root_parsed.path.rstrip("/")
        url_path = parsed.path.rstrip("/")

        if not url_path.startswith(root_path):
            raise ValueError(f"URL must be within environment root: {url} (root: {self.url})")

        # Validate type if required
        if require_type == "file" and not self._fs.isfile(parsed.path):
            raise FileNotFoundError(f"File not found: {url}")
        elif require_type == "directory" and not self._fs.isdir(parsed.path):
            raise ValueError(f"URL must be a directory: {url}")

        return parsed

    async def run_command(self, command: list[str], page_url: str) -> CommandOutput:
        """Execute a command from a markdown page's frontmatter.

        Instructions:
        1. First read the markdown page to see available commands in its frontmatter
        2. Commands must exactly match those listed in the page's frontmatter
        3. If you don't know what a command does or what arguments it accepts, run it with --help flag first (e.g., ['command', '--help'])
        4. Use the help output to understand the command's usage before running it with actual arguments
        5. page_url MUST be an absolute file URL within the environment root (e.g., 'file:///path/to/page.md', 's3://bucket/path/page.md', 'https://example.com/docs/page.md')

        Parameters
        ----------
        command : list[str]
            Command and its arguments as a list (e.g., ['python', 'script.py', '--arg', 'value'])
        page_url : str
            Absolute file URL to the markdown (.md) page containing the command in its frontmatter

        Returns
        -------
        CommandOutput
            Object with stdout and stderr

        Raises
        ------
        RuntimeError
            If command is not listed in the page's frontmatter or execution fails
        """
        parsed = self._validate_url(page_url, require_type="file")

        if not parsed.path.endswith(".md"):
            raise ValueError(f"page_url must point to a markdown (.md) file: {urlunparse(parsed)}")

        # Parse frontmatter and validate command
        frontmatter = get_frontmatter(self._fs.read_text(parsed.path))
        if not frontmatter:
            raise RuntimeError(f"No frontmatter found in: {urlunparse(parsed)}")

        tools = frontmatter.get("tools", {})
        if not tools:
            raise RuntimeError(f"No tools found in frontmatter of: {urlunparse(parsed)}")

        if not any(command[: len(t)] == t for t in tools):
            raise RuntimeError(f"Invalid command: {command}. Must be one of: {tools}")

        # Execute in page directory for file:// URLs
        cwd = None
        if parsed.scheme == "file":
            cwd = parsed.path.rsplit("/", 1)[0] if "/" in parsed.path else ""

        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)

        return CommandOutput(stdout=result.stdout, stderr=result.stderr)

    async def read(self, file_url: str, offset: int | None = None, length: int | None = None) -> ReadFileOutput:
        """Read a file from the filesystem.

        Instructions:
        1. file_url MUST be an absolute file URL within the environment root
        2. Use glob to find files first if you don't know the exact path
        3. Offset and length are line-based (0-indexed)

        Parameters
        ----------
        file_url : str
            Absolute file URL (e.g., 'file:///path/to/file.txt', 's3://bucket/file.py')
        offset : int | None
            Starting line number (0-indexed, default: 0)
        length : int | None
            Number of lines to read (default: read to end)

        Returns
        -------
        ReadFileOutput
            Object with content, total lines, and lines returned

        Raises
        ------
        FileNotFoundError
            If the file doesn't exist
        """
        parsed = self._validate_url(file_url, require_type="file")

        all_lines = self._fs.read_text(parsed.path).splitlines()
        total_lines = len(all_lines)
        start = offset if offset is not None else 0
        end = (start + length) if length is not None else total_lines

        selected_lines = all_lines[start:end]
        content = "\n".join(f"{start + i + 1:6d}\t{line}" for i, line in enumerate(selected_lines))

        return ReadFileOutput(content=content, total_lines=total_lines, lines_returned=len(selected_lines))

    async def tree(
        self,
        path_url: str,
        recursion_limit: int = 2,
        max_display: int = 25,
    ) -> str:
        """Get directory tree structure.

        Instructions:
        1. path_url MUST be an absolute directory URL within the environment root
        2. Returns a visual tree representation of the directory structure
        3. Use recursion_limit to control depth (default: 2 levels)
        4. Use max_display to limit items shown per directory (default: 25)

        Parameters
        ----------
        path_url : str
            Absolute directory URL (e.g., 'file:///path/to/dir', 's3://bucket/path')
        recursion_limit : int
            Maximum depth of directory traversal (default: 2)
        max_display : int
            Maximum number of items to display per directory (default: 25)

        Returns
        -------
        str
            Visual tree representation of the directory structure

        Raises
        ------
        ValueError
            If path_url is not a directory
        """
        parsed = self._validate_url(path_url, require_type="directory")

        return self._fs.tree(
            path=parsed.path,
            recursion_limit=recursion_limit,
            max_display=max_display,
        )

    async def glob(self, path_url: str, pattern: str) -> GlobOutput:
        """Find files matching a glob pattern.

        Instructions:
        1. path_url MUST be an absolute directory URL within the environment root (e.g., 'file:///path/to/dir', 's3://bucket/path', 'https://example.com/files')
        2. All URLs must be within the environment's root URL
        3. pattern is the glob pattern to match (e.g., '**/*.py', '*.md', 'src/**/*.txt')
        4. Use ** for recursive directory matching
        5. Pattern is combined with the directory URL

        Examples:
        - Find Python files locally: path_url='file:///path/to/project', pattern='**/*.py'
        - Find markdown in remote bucket: path_url='s3://bucket/docs', pattern='**/*.md'
        - Find text files via HTTP: path_url='https://example.com/files', pattern='*.txt'

        Parameters
        ----------
        path_url : str
            Absolute directory URL (e.g., 'file:///path/to/dir', 's3://bucket/path', 'https://example.com/files')
        pattern : str
            Glob pattern to match (e.g., '**/*.py', '*.md')

        Returns
        -------
        GlobOutput
            Object with matches, count, and url pattern

        Raises
        ------
        ValueError
            If path_url is not a directory or pattern is malformed
        """
        parsed = self._validate_url(path_url, require_type="directory")

        search_path = parsed.path.rstrip("/") + "/" + pattern
        matches = self._fs.glob(search_path)
        url_pattern = f"{urlunparse(parsed)}/{pattern}"

        return GlobOutput(matches=matches, count=len(matches), url_pattern=url_pattern)

    async def grep(
        self,
        pattern: str,
        path_url: str,
        filename_pattern: str | None = None,
        output_mode: OutputMode = OutputMode.CONTENT,
        case_insensitive: bool = False,
        show_line_numbers: bool = True,
        lines_before: int | None = None,
        lines_after: int | None = None,
        lines_context: int | None = None,
        limit: int | None = None,
    ) -> GrepContentOutput | GrepFilesOutput | GrepCountOutput:
        """Search documents using regex pattern matching via grep subprocess.

        Instructions:
        1. pattern is a regular expression (not literal string)
        2. Set case_insensitive=True for case-insensitive matching
        3. Use output_mode to control results:
           - 'content': matching lines with optional context
           - 'files_with_matches': list of files containing matches
           - 'count': total number of matches
        4. For content mode, use lines_before/lines_after/lines_context for context
        5. Use filename_pattern to filter by filename glob (e.g., '*.py')
        6. path_url MUST be an absolute URL within the environment root
        7. For local filesystems (file://), uses native grep subprocess for performance

        Parameters
        ----------
        pattern : str
            Regular expression pattern
        path_url : str
            Absolute URL to search
        filename_pattern : str | None
            Glob pattern to filter filenames (e.g., '*.py', '*.md')
        output_mode : OutputMode
            Output mode (default: content)
        case_insensitive : bool
            Case insensitive (default: False)
        show_line_numbers : bool
            Show line numbers in content mode (default: True)
        lines_before : int | None
            Lines before match (content mode)
        lines_after : int | None
            Lines after match (content mode)
        lines_context : int | None
            Lines before and after (overrides lines_before/after)
        limit : int | None
            Max results (None for unlimited)

        Returns
        -------
        GrepContentOutput | GrepFilesOutput | GrepCountOutput
            Output depends on output_mode

        Raises
        ------
        RuntimeError
            If grep command fails
        """
        parsed = self._validate_url(path_url, require_type="directory")

        # For local filesystems, use native grep
        if parsed.scheme == "file":
            grep_args = ["grep", "-r"]

            # Add flags
            if case_insensitive:
                grep_args.append("-i")
            if show_line_numbers and output_mode == OutputMode.CONTENT:
                grep_args.append("-n")

            # Handle output mode
            if output_mode == OutputMode.FILES_WITH_MATCHES:
                grep_args.append("-l")
            elif output_mode == OutputMode.COUNT:
                grep_args.append("-c")

            # Handle context
            if output_mode == OutputMode.CONTENT:
                if lines_context is not None:
                    grep_args.append(f"-C{lines_context}")
                else:
                    if lines_before:
                        grep_args.append(f"-B{lines_before}")
                    if lines_after:
                        grep_args.append(f"-A{lines_after}")

            # Add filename filter
            if filename_pattern:
                grep_args.extend(["--include", filename_pattern])

            # Add pattern and path
            grep_args.append(pattern)
            grep_args.append(parsed.path)

            result = subprocess.run(grep_args, capture_output=True, text=True)

            # Parse output based on mode
            if output_mode == OutputMode.FILES_WITH_MATCHES:
                files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
                return GrepFilesOutput(files=files, count=len(files))

            elif output_mode == OutputMode.COUNT:
                total = 0
                for line in result.stdout.splitlines():
                    if ":" in line:
                        try:
                            count = int(line.split(":")[-1])
                            total += count
                        except ValueError:
                            continue
                return GrepCountOutput(total_matches=total)

            else:  # CONTENT mode
                matches = []
                lines = result.stdout.splitlines()
                i = 0
                while i < len(lines):
                    line = lines[i]
                    if not line:
                        i += 1
                        continue

                    # Parse grep output: filename:line_number:content
                    if ":" in line:
                        parts = line.split(":", 2)
                        if len(parts) >= 3:
                            filename = parts[0]
                            try:
                                line_num = int(parts[1]) if show_line_numbers else None
                                content = parts[2]

                                # Collect context (simplistic - grep handles this)
                                match = GrepMatch(
                                    file=filename,
                                    line_number=line_num,
                                    line=content,
                                    before_context=None,
                                    after_context=None,
                                )
                                matches.append(match)

                                if limit and len(matches) >= limit:
                                    break
                            except ValueError:
                                pass
                    i += 1

                return GrepContentOutput(matches=matches, total_matches=len(matches))

        else:
            raise NotImplementedError("Grep for remote filesystems is not yet implemented.")

    async def search(
        self,
        terms: str,
        path_url: str,
        limit: int = 10,
    ) -> SearchOutput:
        """Search documents using BM25 full-text search.

        Instructions:
        1. Craft queries with actual terms/keywords you've seen in documents
        2. Include synonyms and variations (e.g., "authenticate login session")
        3. Mix general concepts with specific names (classes, functions, terms)
        4. Results ranked by relevance score (higher = more relevant)
        5. Searches entire document content (whole files)
        6. path_url MUST be an absolute URL within the environment root

        Parameters
        ----------
        terms : str
            Search query (natural language keywords)
        path_url : str
            Absolute URL to search
        limit : int
            Max results (default: 10)

        Returns
        -------
        SearchOutput
            Search results ranked by BM25 score

        Raises
        ------
        RuntimeError
            If no search index exists
        """
        raise NotImplementedError("Search is not implemented yet")
