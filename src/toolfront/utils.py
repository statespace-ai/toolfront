import ast
import functools
import inspect
import logging
import os
import re
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib import parse

import executing
import pandas as pd
import yaml
from pydantic_ai import ModelRetry
from pydantic_ai.messages import ModelMessage, ToolReturnPart
from yarl import URL

from toolfront.config import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_COHERE_MODEL,
    DEFAULT_GOOGLE_MODEL,
    DEFAULT_MISTRAL_MODEL,
    DEFAULT_OPENAI_MODEL,
)

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)


@contextmanager
def change_dir(destination):
    prev_dir = Path.cwd()  # save current directory
    os.chdir(destination)  # change to new directory
    try:
        yield
    finally:
        os.chdir(prev_dir)  # restore original directory


def prepare_tool_for_pydantic_ai(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that automatically serializes function outputs using serialize_response and handles errors.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that serializes its output
    """
    
    # Get the original function signature
    sig = inspect.signature(func)
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            
            if isinstance(result, pd.DataFrame):
                result = result.to_markdown()
            return result
        
        except Exception as e:
            logger.error(f"Tool {func.__name__} failed: {e}", exc_info=True)
            raise ModelRetry(f"Tool {func.__name__} failed: {str(e)}") from e
    
    wrapper.__signature__ = sig
    
    return wrapper


def sanitize_url(url: str) -> str:
    """Sanitize the url by removing the password."""
    url = URL(url)
    if url.password:
        url = url.with_password("***")
    return str(url)


def get_model_from_env() -> str:
    if model := os.getenv("TOOLFRONT_MODEL"):
        return model
    
    """Get the default model to use."""
    if os.getenv("OPENAI_API_KEY"):
        return DEFAULT_OPENAI_MODEL
    elif os.getenv("ANTHROPIC_API_KEY"):
        return DEFAULT_ANTHROPIC_MODEL
    elif os.getenv("GOOGLE_API_KEY"):
        return DEFAULT_GOOGLE_MODEL
    elif os.getenv("MISTRAL_API_KEY"):
        return DEFAULT_MISTRAL_MODEL
    elif os.getenv("COHERE_API_KEY"):
        return DEFAULT_COHERE_MODEL
    raise ValueError("Please specify an API key and model to use")


def get_output_type_hint() -> Any:
    """
    Get the caller's variable type annotation using the executing library.

    Returns:
        The type annotation or None if not found
    """
    
    def _contains_node(tree: ast.AST | None, target: ast.AST) -> bool:
        """Check if target node is anywhere in the tree."""
        if tree is None or tree is target:
            return tree is target
        return any(_contains_node(child, target) for child in ast.iter_child_nodes(tree))
    
    try:
        # Get caller's frame (2 levels up: this function -> ask() -> actual caller)
        frame = inspect.currentframe().f_back.f_back
        source = executing.Source.for_frame(frame)
        node = source.executing(frame).node
        
        if not node:
            return None
        
        parent = node.parent
        
        # Walk up the AST to find the assignment containing our call
        if (
                isinstance(parent, ast.AnnAssign)
                and _contains_node(parent.value, node)
                and isinstance(parent.target, ast.Name)
        ):
            # Found annotated assignment: var: Type = value
            try:
                return eval(ast.unparse(parent.annotation), frame.f_globals, frame.f_locals)
            except Exception:
                return ast.unparse(parent.annotation)
        
        return None
    
    except Exception as e:
        logger.debug(f"Could not get caller context: {e}")
        return None


def parse_markdown_with_frontmatter(markdown: str) -> tuple[str, dict[str, Any]]:
    """Parse frontmatter from markdown content and return both raw markdown and frontmatter.

    Args:
        markdown: Raw markdown content with optional frontmatter

    Returns:
        Tuple of (raw_markdown_without_frontmatter, frontmatter_config)
    """
    frontmatter_pattern = r"^\n*---\s*\n(.*?)\n---\s*\n(.*)"
    match = re.match(frontmatter_pattern, markdown, re.DOTALL)
    
    if not match:
        return markdown, {}
    
    try:
        frontmatter_yaml = match.group(1)
        content_without_frontmatter = match.group(2)
        config = yaml.safe_load(frontmatter_yaml) or {}
        return content_without_frontmatter, config
    except Exception as e:
        logger.warning(f"Failed to parse frontmatter YAML: {e}")
        return markdown, {}


def url_to_path(url: str) -> Path:
    parsed_url = parse.urlparse(url)
    return Path(parsed_url.netloc.rstrip("/")) / parsed_url.path.lstrip("/")


async def message_at_index_contains_tool_return_parts(messages: list[ModelMessage], index: int) -> bool:
    return any(isinstance(part, ToolReturnPart) for part in messages[index].parts)


def history_processor(context_window: int | None = None) -> callable:
    if not context_window:
        return None
    
    async def keep_recent_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
        number_of_messages = len(messages)
        if number_of_messages <= context_window:
            return messages
        if await message_at_index_contains_tool_return_parts(messages, number_of_messages - context_window):
            return messages
        return [messages[0]] + messages[-context_window:]
    
    return keep_recent_messages
