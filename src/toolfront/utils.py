"""
Data serialization utilities for converting DataFrames and other data structures.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from urllib.parse import parse_qs

import pandas as pd
from jellyfish import jaro_winkler_similarity
from rank_bm25 import BM25Okapi

from toolfront.config import MAX_DATA_ROWS


class HTTPMethod(str, Enum):
    """Valid HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class SearchMode(str, Enum):
    """Search mode for searching items."""

    REGEX = "regex"
    BM25 = "bm25"
    JARO_WINKLER = "jaro_winkler"


@dataclass
class ConnectionResult:
    """Result of a database connection test."""

    connected: bool
    message: str


def tokenize(text: str) -> list[str]:
    """Tokenize text by splitting on common separators and filtering empty tokens."""
    return [token.lower() for token in re.split(r"[/._\s-]+", text) if token]


def search_items_regex(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using regex pattern."""
    regex = re.compile(pattern)
    return [name for name in item_names if regex.search(name)][:limit]


def search_items_jaro_winkler(item_names: list[str], pattern: str, limit: int) -> list[str]:
    """Search items using Jaro-Winkler similarity."""
    tokenized_pattern = " ".join(tokenize(pattern))
    similarities = [(name, jaro_winkler_similarity(" ".join(tokenize(name)), tokenized_pattern)) for name in item_names]
    return [name for name, _ in sorted(similarities, key=lambda x: x[1], reverse=True)][:limit]


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
        for name, _ in sorted(zip([n for n, _ in valid_items], scores, strict=False), key=lambda x: x[1], reverse=True)
    ][:limit]


def search_items(
    item_names: list[str], pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10
) -> list[str]:
    """Search for item names using different algorithms."""
    if not item_names:
        return []

    if mode == SearchMode.REGEX:
        return search_items_regex(item_names, pattern, limit)
    elif mode == SearchMode.JARO_WINKLER:
        return search_items_jaro_winkler(item_names, pattern, limit)
    elif mode == SearchMode.BM25:
        return search_items_bm25(item_names, pattern, limit)
    else:
        raise ValueError(f"Unknown search mode: {mode}")


def parse_query_string(query_string: str) -> dict[str, Any]:
    """
    Parse a query string into a dictionary.

    Args:
        query_string (str): The query string to parse, can start with 'query=' or just be the query parameters

    Returns:
        Dict[str, Any]: Dictionary containing the parsed query parameters

    Example:
        >>> parse_query_string("query='apiKey=abc123'")
        {'apiKey': 'abc123'}
        >>> parse_query_string("apiKey=abc123&param=value")
        {'apiKey': 'abc123', 'param': 'value'}
    """
    # Remove 'query=' prefix if present
    if query_string.startswith("query="):
        query_string = query_string[6:]

    # Remove surrounding quotes if present
    query_string = query_string.strip("'\"")

    # Parse the query string
    parsed = parse_qs(query_string)

    # Convert lists to single values where possible
    return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}


def serialize_response(response: Any) -> Any:
    """Serialize a response object to a JSON-compatible format."""
    if hasattr(response, "model_dump"):
        return response.model_dump()
    return response


def serialize_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """
    Convert a pandas DataFrame to a JSON-serializable response format with pagination.

    Serializes DataFrame data including datetime objects and handles automatic truncation
    when the dataset exceeds MAX_DATA_ROWS.

    Args:
        df: The pandas DataFrame to convert and format

    Returns:
        Dictionary with 'data' (table structure), 'row_count' (total rows), and
        optional 'message' (truncation notice when data is truncated)
    """

    def serialize_value(v: Any) -> Any:
        """Serialize individual values, handling special types like datetime and NaN."""
        # Convert pandas and Python datetime objects to ISO format, handle NaT/NaN
        if pd.isna(v):
            return None
        if isinstance(v, datetime | pd.Timestamp):
            return v.isoformat()
        if isinstance(v, pd.Period):
            return v.asfreq("D").to_timestamp().isoformat()
        elif not hasattr(v, "__dict__"):
            return str(v)
        return v

    # Build rows including index, serializing each cell
    rows_with_indices = []
    for idx, row in df.iterrows():
        serialized_row = [serialize_value(idx)]
        for v in row.tolist():
            serialized_row.append(serialize_value(v))
        rows_with_indices.append(serialized_row)

    columns_with_index = ["index"] + df.columns.tolist()

    # Get total row count
    total_rows = len(rows_with_indices)

    # Handle truncation if needed
    is_truncated = total_rows > MAX_DATA_ROWS
    if is_truncated:
        rows_with_indices = rows_with_indices[:MAX_DATA_ROWS]

    table_data = {
        "type": "table",
        "columns": columns_with_index,
        "rows": rows_with_indices,
    }

    result = {"data": table_data, "row_count": total_rows}

    if is_truncated:
        result["message"] = (
            f"Results truncated to {MAX_DATA_ROWS} rows (showing {MAX_DATA_ROWS} of {total_rows} total rows)"
        )

    return result
