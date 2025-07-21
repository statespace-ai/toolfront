import json
import logging
import re
from typing import Any, get_args, get_origin

import pandas as pd
from platformdirs import user_cache_dir
from pydantic import TypeAdapter
from rank_bm25 import BM25Okapi
from yarl import URL

from toolfront.config import MAX_DATA_CHARS, MAX_DATA_ROWS

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)

cache_dir = user_cache_dir("toolfront")


def serialize_output(func):
    """
    Decorator that automatically serializes function outputs using serialize_response.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that serializes its output
    """
    import inspect

    # Get the original function signature
    sig = inspect.signature(func)

    # Create a wrapper function with the exact same signature
    def create_wrapper():
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return serialize_response(result)

        return wrapper

    wrapper = create_wrapper()

    # Preserve all function metadata for proper introspection
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = getattr(func, "__annotations__", {}).copy()
    wrapper.__signature__ = sig
    wrapper.__module__ = getattr(func, "__module__", None)
    wrapper.__qualname__ = getattr(func, "__qualname__", func.__name__)

    return wrapper


def tokenize(text: str) -> list[str]:
    """Tokenize text by splitting on common separators and filtering empty tokens."""
    return [token.lower() for token in re.split(r"[/._\s-]+", text) if token]


def search_items_regex(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using regex pattern."""
    regex = re.compile(pattern)
    return [name for name in item_names if regex.search(name)][:limit]


def search_items_bm25(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using BM25 ranking algorithm."""
    query_tokens = tokenize(pattern)
    if not query_tokens:
        return []

    valid_items = [(name, tokenize(name)) for name in item_names]
    valid_items = [(name, tokens) for name, tokens in valid_items if tokens]
    if not valid_items:
        return []

    # Create corpus of tokenized item names
    corpus = [tokens for _, tokens in valid_items]

    # Initialize BM25 with the corpus
    bm25 = BM25Okapi(corpus)

    # Get BM25 scores for the query
    scores = bm25.get_scores(query_tokens)

    return [
        name
        for name, score in sorted(
            zip([n for n, _ in valid_items], scores, strict=False), key=lambda x: x[1], reverse=True
        )
        if score > 0
    ][:limit]


def search_items(
    items: list[str],
    terms: list[str] | str | None = None,
    like: str | None = None,
    regex: str | None = None,
    limit: int = 10,
) -> list[str]:
    """
    Search for item names using different algorithms.

    Parameters
    ----------
    items : list[str]
        The list of items to search through.
    terms : list[str] | str | None, optional
        Terms for BM25 search. Can be either a list of strings or a single string
        with space-separated words. If provided, uses BM25 ranking algorithm.
        Default is None.
    like : str | None, optional
        Pattern for wildcard search. Converts to regex pattern with wildcards
        (e.g., "car" becomes ".*car.*"). Default is None.
    regex : str | None, optional
        Regular expression pattern for exact regex matching. Default is None.
    limit : int, optional
        Maximum number of items to return. Default is 10.

    Returns
    -------
    list[str]
        Filtered list of items matching the search criteria, limited to `limit` items.

    Raises
    ------
    ValueError
        If more than one of `terms`, `like`, or `regex` is provided, or if all
        three parameters are None.

    Notes
    -----
    The parameters `terms`, `like`, and `regex` are mutually exclusive. Only one
    can be provided at a time.

    Examples
    --------
    >>> items = ["user_table", "order_table", "product_catalog"]
    >>> search_items(items, terms=["user"], limit=5)
    ['user_table']

    >>> search_items(items, like="table")
    ['user_table', 'order_table']

    >>> search_items(items, regex=".*_table$")
    ['user_table', 'order_table']
    """
    if not items or not len(items):
        return []

    # Ensure mutually exclusive parameters
    provided_params = sum([terms is not None, like is not None, regex is not None])
    if provided_params > 1:
        raise ValueError("terms, like, and regex are mutually exclusive")

    if terms is not None:
        # Handle terms as either string or list
        pattern = terms if isinstance(terms, str) else " ".join(terms)
        return search_items_bm25(items, pattern, limit)
    elif regex is not None:
        # Use regex search
        return search_items_regex(items, regex, limit)
    elif like is not None:
        # Convert like pattern to regex (like "car" becomes ".*car.*")
        regex_pattern = f".*{re.escape(like)}.*"
        return search_items_regex(items, regex_pattern, limit)
    else:
        # All parameters are None - raise error
        raise ValueError("At least one of terms, like, or regex must be provided")


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
            truncated_list = tool_result[:10] + ['...']
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
