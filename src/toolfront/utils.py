import functools
import inspect
import json
import logging
from collections.abc import Callable
from typing import Any, get_args, get_origin

import pandas as pd
from pydantic import TypeAdapter
from pydantic_ai import ModelRetry
from yarl import URL

from toolfront.config import MAX_DATA_CHARS, MAX_DATA_ROWS

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)


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
            result = await func(*args, **kwargs)
            return serialize_response(result)
        except Exception as e:
            logger.error(f"Tool {func.__name__} failed: {e}", exc_info=True)
            raise ModelRetry(f"Tool {func.__name__} failed: {str(e)}") from e

    wrapper.__signature__ = sig

    return wrapper


def serialize_response(response: Any) -> Any:
    """
    Serialize any response to JSON-compatible format with proper truncation.
    Uses pydantic TypeAdapter for robust serialization of any object type.

    Args:
        response: Response to serialize (can be any type)

    Returns:
        Serialized response with optional truncation message
    """

    if isinstance(response, pd.DataFrame):
        # Truncate by rows if needed
        if len(response) > MAX_DATA_ROWS:
            truncated_df = response.head(MAX_DATA_ROWS)
            json_str = truncated_df.to_csv(index=False)
            return {
                "data": json_str,
                "truncation_message": f"Showing {MAX_DATA_ROWS:,} rows of {len(response):,} total rows",
            }

        # Convert to JSON string
        return response.to_csv(index=False)

    # For all other types, use pydantic TypeAdapter
    adapter = TypeAdapter(Any)
    serialized = adapter.dump_python(response)

    # Convert to JSON string to check character count
    json_str = json.dumps(serialized)

    # Handle truncation
    if len(json_str) > MAX_DATA_CHARS:
        truncated_str = json_str[: MAX_DATA_CHARS - 3] + "..."
        return {
            "data": truncated_str,
            "truncation_message": f"Showing {len(truncated_str):,} characters of {len(json_str):,} total characters",
        }

    return serialized


def deserialize_response(tool_result: Any) -> str:
    """Format tool result with proper type handling and truncation."""
    # Handle dict/object results - recursively process each key-value pair
    if isinstance(tool_result, dict):
        if not tool_result:
            return "```json\n{}\n```"

        parts = []
        for k, v in tool_result.items():
            formatted_value = deserialize_response(v)
            parts.append(f"**{k}:**\n{formatted_value}")

        return "\n\n".join(parts)

    # Handle string results - try CSV first, then raw string
    elif isinstance(tool_result, str):
        # Try parsing as CSV first
        try:
            from io import StringIO

            df = pd.read_csv(StringIO(tool_result))
            return f"\n{df.head(10).to_markdown()}\n"
        except Exception:
            # Fallback: treat as raw string and truncate if too long
            if len(tool_result) > 10000:
                tool_result = tool_result[:10000] + "...\n(truncated)"
            return f"\n{tool_result}\n"

    # Handle pandas DataFrame
    elif hasattr(tool_result, "to_markdown"):
        try:
            return f"```markdown\n{tool_result.head(10).to_markdown()}\n```"
        except Exception:
            pass

    # Handle lists
    elif isinstance(tool_result, list):
        if len(tool_result) > 10:
            truncated_list = tool_result[:10] + ["..."]
            result = json.dumps(truncated_list, indent=2)
            return f"```json\n{result}\n```\n\n(showing first 10 of {len(tool_result)} items)"
        else:
            result = json.dumps(tool_result, indent=2)
            return f"```json\n{result}\n```"

    # Handle other types
    else:
        tool_result_str = str(tool_result)
        if len(tool_result_str) > 10000:
            tool_result_str = tool_result_str[:10000] + "...\n(truncated)"
        return f"```\n{tool_result_str}\n```"


def sanitize_url(url: str) -> str:
    """Sanitize the url by removing the password."""
    url = URL(url)
    if url.password:
        url = url.with_password("***")
    return str(url)


def type_allows_none(type_hint: Any) -> bool:
    """
    Check if a type hint allows None values.

    Handles:
    - type(None) / NoneType
    - Optional[T] (which is Union[T, None])
    - T | None (Python 3.10+ union syntax)
    - Union[T, None]
    """
    if type_hint is type(None):
        return True

    # Handle Union types (including Optional)
    origin = get_origin(type_hint)
    if origin is not None:
        # For Union types, check if None is in the args
        args = get_args(type_hint)
        return type(None) in args

    return False
