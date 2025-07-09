import logging
from typing import Any

from pydantic import Field

from toolfront.config import (
    NUM_DOCUMENT_SEARCH_ITEMS,
)
from toolfront.models.atomics.document import Document
from toolfront.models.connections.library import LibraryConnection
from toolfront.types import SearchMode
from toolfront.utils import serialize_response

logger = logging.getLogger("toolfront")


__all__ = [
    "sample_document",
    "search_documents",
    "read_document",
]


async def sample_document(
    document: Document = Field(..., description="Document to sample."),
) -> dict[str, Any]:
    """
    Get a content sample from a document.

    ALWAYS SAMPLE DOCUMENTS BEFORE WRITING QUERIES TO PREVENT ERRORS. NEVER SAMPLE MORE ROWS THAN NECESSARY.
    ENSURE THE DATA SOURCE EXISTS BEFORE ATTEMPTING TO SAMPLE DOCUMENTS.

    Library Sample Instructions:
    1. Use this tool to preview documents.
    2. Sampling documents helps validate your assumptions about their content.
    3. Always sample documents before reading them to understand whether they are relevant to the task and prevent redundant calls.
    """
    try:
        logger.debug(f"Sampling document: {document.connection.url} {document.path}")
        library = await document.connection.connect()
        return serialize_response(await library.sample_document(**document.model_dump(exclude={"connection"})))
    except Exception as e:
        logger.error(f"Failed to sample document: {e}", exc_info=True)
        raise ConnectionError(
            f"Failed to sample document in {document.connection.url} document {document.path}: {str(e)}"
        )


async def search_documents(
    connection: LibraryConnection = Field(..., description="Library connection to search."),
    pattern: str = Field(..., description="Pattern to search for."),
    mode: SearchMode = Field(default=SearchMode.REGEX, description="Search mode to use."),
) -> dict[str, Any]:
    """
    Find and return documents that match the given pattern.

    NEVER CALL THIS TOOL MORE THAN NECESSARY. DO NOT ADJUST THE LIMIT PARAMETER UNLESS REQUIRED.

    Library Search Instructions:
    1. This tool searches for document names in "file://path" format (e.g., "file:///Users/path/to/dir").
    2. Determine the best search mode to use:
        - regex:
            * Returns documents matching a regular expression pattern
            * Pattern must be a valid regex expression
            * Use when you need precise document matching
        - bm25:
            * Returns documents using case-insensitive BM25 (Best Match 25) ranking algorithm
            * Pattern must be a sentence, phrase, or space-separated words
            * Use when searching document names with descriptive keywords
        - jaro_winkler:
            * Returns documents using case-insensitive Jaro-Winkler similarity algorithm
            * Pattern must be an existing document name.
            * Use to search for similar document names.
    3. Begin with approximate search modes like BM25 and Jaro-Winkler, and only use regex to precisely search for a specific document name.
    """
    try:
        logger.debug(f"Searching documents: {connection.url} {pattern} {mode}")
        library = await connection.connect()
        result = await library.search_documents(pattern=pattern, mode=mode, limit=NUM_DOCUMENT_SEARCH_ITEMS)
        return {"documents": result}
    except Exception as e:
        logger.error(f"Failed to search documents: {e}", exc_info=True)
        raise ConnectionError(f"Failed to search documents in {connection.url} - {str(e)}")


async def read_document(
    document: Document = Field(..., description="Document to read."),
) -> dict[str, Any]:
    """
    Read the contents of a library's document.

    ALWAYS READ STORAGES BEFORE USING THEM TO PREVENT ERRORS.
    ENSURE THE STORAGE EXISTS BEFORE ATTEMPTING TO READ IT.

    Library Read Instructions:
    1. Use this tool to read the entire contents of a library's document.
    """
    try:
        logger.debug(f"Reading document: {document.connection.url} {document.path}")
        library = await document.connection.connect()
        return serialize_response(await library.read_document(**document.model_dump(exclude={"connection"})))
    except Exception as e:
        logger.error(f"Failed to read library: {e}", exc_info=True)
        raise ConnectionError(f"Failed to read library in {document.connection.url} - {str(e)}")
