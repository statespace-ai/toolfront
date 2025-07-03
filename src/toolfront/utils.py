import logging
import re
from datetime import datetime
from typing import Any

import pandas as pd
from jellyfish import jaro_winkler_similarity
from rank_bm25 import BM25Okapi

from toolfront.config import MAX_DATA_ROWS
from toolfront.types import SearchMode

logger = logging.getLogger("toolfront")
logger.setLevel(logging.INFO)


def tokenize(text: str) -> list[str]:
    """Tokenize text into words."""
    return re.findall(r"\w+", text.lower())


def search_items_regex(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using regex."""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        return [name for name in item_names if regex.search(name)][:limit]
    except re.error:
        return []


def search_items_jaro_winkler(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using Jaro-Winkler similarity."""
    scores = [(name, jaro_winkler_similarity(pattern.lower(), name.lower())) for name in item_names]
    return [name for name, score in sorted(scores, key=lambda x: x[1], reverse=True) if score > 0.8][:limit]


def search_items_bm25(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using BM25."""
    # Tokenize all items
    tokenized_items = [tokenize(name) for name in item_names]

    # Create BM25 model
    bm25 = BM25Okapi(tokenized_items)

    # Tokenize query and get scores
    query_tokens = tokenize(pattern)
    if not query_tokens:
        return []

    # Get scores and sort
    scores = bm25.get_scores(query_tokens)
    scored_items = list(zip(item_names, scores, strict=False))
    return [name for name, score in sorted(scored_items, key=lambda x: x[1], reverse=True) if score > 0][:limit]


def search_items(
    item_names: list[str], pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10
) -> list[str]:
    """
    Search items using different algorithms.

    Args:
        item_names: List of item names to search
        pattern: Search pattern
        mode: Search mode (regex, bm25, jaro_winkler)
        limit: Maximum number of results to return

    Returns:
        List of matching item names
    """
    if mode == SearchMode.REGEX:
        return search_items_regex(item_names, pattern, limit)
    elif mode == SearchMode.BM25:
        return search_items_bm25(item_names, pattern, limit)
    elif mode == SearchMode.JARO_WINKLER:
        return search_items_jaro_winkler(item_names, pattern, limit)
    else:
        raise ValueError(f"Invalid search mode: {mode}")


def serialize_value(v: Any) -> Any:
    """Serialize a single value."""
    if pd.isna(v):
        return None
    elif isinstance(v, int | float | str | bool):
        return v
    elif isinstance(v, datetime):
        return v.isoformat()
    else:
        return str(v)


def serialize_dict(d: dict[str, Any]) -> dict[str, Any]:
    """
    Serialize a dictionary to JSON-compatible format.

    Args:
        d: Dictionary to serialize

    Returns:
        Serialized dictionary
    """
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = serialize_dict(v)
        elif isinstance(v, list | tuple):
            result[k] = [serialize_value(x) for x in v]
        else:
            result[k] = serialize_value(v)
    return result


def serialize_response(response: Any) -> dict[str, Any]:
    """
    Serialize a response to JSON-compatible format.

    Args:
        response: Response to serialize

    Returns:
        Serialized response
    """
    if isinstance(response, pd.DataFrame):
        return serialize_dataframe(response)
    elif isinstance(response, dict):
        return serialize_dict(response)
    elif isinstance(response, list | tuple):
        return [serialize_value(x) for x in response]
    else:
        return serialize_value(response)


def serialize_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """
    Serialize a DataFrame to JSON-compatible format.

    Args:
        df: DataFrame to serialize

    Returns:
        Serialized DataFrame with:
            - columns: List of column names
            - data: List of rows
            - truncated: Whether the data was truncated
    """
    # Get column names and types
    columns = [{"name": str(col), "type": str(dtype)} for col, dtype in df.dtypes.items()]

    # Convert to records
    truncated = False
    if len(df) > MAX_DATA_ROWS:
        df = df.head(MAX_DATA_ROWS)
        truncated = True

    # Convert to list of dicts
    data = df.to_dict("records")

    # Serialize each value
    data = [serialize_dict(row) for row in data]

    return {
        "columns": columns,
        "data": data,
        "truncated": truncated,
    }
