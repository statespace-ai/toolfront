import logging
from typing import Any

from pydantic import Field

from toolfront.config import (
    MAX_DATA_ROWS,
    NUM_TABLE_SEARCH_ITEMS,
)
from toolfront.models.actions.query import Query
from toolfront.models.atomics.table import Table
from toolfront.models.datasources.database import Database
from toolfront.types import SearchMode
from toolfront.utils import serialize_response

logger = logging.getLogger("toolfront")


__all__ = [
    "db_inspect_table",
    "db_query",
    "db_sample_table",
    "db_search_tables",
]


async def db_inspect_table(
    table: Table = Field(..., description="Database table to inspect."),
) -> dict[str, Any]:
    """
    Inspect the structure of database table.

    ALWAYS INSPECT TABLES BEFORE WRITING QUERIES TO PREVENT ERRORS.
    ENSURE THE TABLE EXISTS BEFORE ATTEMPTING TO INSPECT IT.

    Inspect Instructions:
    1. Use this tool to understand table structure like column names, data types, and constraints
    2. Inspecting tables helps understand the structure of the data
    3. Always inspect tables before writing queries to understand their structure and prevent errors
    """
    try:
        logger.debug(f"Inspecting table: {table.database_url} {table.path}")
        database = Database.load_from_sanitized_url(table.database_url)
        result = await database.inspect_table(table.path)
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to inspect table: {e}", exc_info=True)
        raise RuntimeError(f"Failed to inspect table {table.path} in {table.database_url} - {str(e)}") from e


async def db_sample_table(
    table: Table = Field(..., description="Database table to sample."),
    n: int = Field(5, description="Number of rows to sample", ge=1, le=MAX_DATA_ROWS),
) -> dict[str, Any]:
    """
    Get a sample of data from a database table.

    ALWAYS SAMPLE TABLES BEFORE WRITING QUERIES TO PREVENT ERRORS. NEVER SAMPLE MORE ROWS THAN NECESSARY.
    ENSURE THE DATA SOURCE EXISTS BEFORE ATTEMPTING TO SAMPLE TABLES.

    Sample Instructions:
    1. Use this tool to preview actual data values and content.
    2. Sampling tables helps validate your assumptions about the data.
    3. Always sample tables before writing queries to understand their structure and prevent errors.
    """
    try:
        logger.debug(f"Sampling table: {table.database_url} {table.path}")
        database = Database.load_from_sanitized_url(table.database_url)
        result = await database.sample_table(table.path, n=n)
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to sample table: {e}", exc_info=True)
        raise RuntimeError(f"Failed to sample table {table.path} in {table.database_url} - {str(e)}") from e


async def db_query(
    query: Query = Field(..., description="Read-only SQL query to execute."),
) -> dict[str, Any]:
    """
    This tool allows you to run read-only SQL queries against a database.

    ALWAYS ENCLOSE IDENTIFIERS (TABLE NAMES, COLUMN NAMES) IN QUOTES TO PRESERVE CASE SENSITIVITY AND AVOID RESERVED WORD CONFLICTS AND SYNTAX ERRORS.

    Query Database Instructions:
        1. Only query tables that have been explicitly discovered, searched for, or referenced in the conversation.
        2. Always use the correct dialect for the database.
        3. Before writing queries, inspect and/or sample the underlying tables to understand their structure and prevent errors.
        4. When a query fails or returns unexpected results, examine the underlying tables to diagnose the issue and then retry.
    """

    try:
        logger.debug(f"Querying database: {query.database_url} {query.code}")
        database = Database.load_from_sanitized_url(query.database_url)
        result = await database.query(**query.model_dump(exclude={"database_url", "description"}))
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to query database: {e}", exc_info=True)
        raise RuntimeError(f"Failed to query database in {query.database_url} - {str(e)}") from e


async def db_search_tables(
    database_url: str = Field(..., description="Database URL to search."),
    pattern: str = Field(..., description="Pattern to search for."),
    mode: SearchMode = Field(default=SearchMode.BM25, description="Search mode to use."),
) -> dict[str, Any]:
    """
    Find and return fully qualified table names that match the given pattern.

    NEVER CALL THIS TOOL MORE THAN NECESSARY. DO NOT ADJUST THE LIMIT PARAMETER UNLESS REQUIRED.

    Table Search Instructions:
    1. This tool searches for fully qualified table names in dot notation format (e.g., schema.table_name or database.schema.table_name).
    2. Determine the best search mode to use:
        - regex:
            * Returns tables matching a regular expression pattern
            * Pattern must be a valid regex expression
            * Use when you need precise table name matching
        - bm25:
            * Returns tables using case-insensitive BM25 (Best Match 25) ranking algorithm
            * Pattern must be a sentence, phrase, or space-separated words
            * Use when searching tables names with descriptive keywords
        - jaro_winkler:
            * Returns tables using case-insensitive Jaro-Winkler similarity algorithm
            * Pattern must be an existing table name.
            * Use to search for similar table names.
    3. Begin with approximate search modes like BM25 and Jaro-Winkler, and only use regex to precisely search for a specific table name.
    """

    try:
        logger.debug(f"Searching tables: {database_url} {pattern} {mode}")
        database = Database.load_from_sanitized_url(database_url)
        result = await database.search_tables(pattern=pattern, limit=NUM_TABLE_SEARCH_ITEMS, mode=mode)
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to search tables: {e}", exc_info=True)
        raise RuntimeError(f"Failed to search tables in {database_url} - {str(e)}") from e
