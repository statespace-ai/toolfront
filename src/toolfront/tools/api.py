import logging
from typing import Any

from pydantic import Field

from toolfront.models.actions.request import Request
from toolfront.models.atomics.endpoint import Endpoint
from toolfront.models.datasources.api import API
from toolfront.utils import serialize_response

logger = logging.getLogger("toolfront")


__all__ = [
    "api_inspect_endpoint",
    "api_request",
    "api_get_endpoints",
]


async def api_get_endpoints(
    api_url: str = Field(..., description="API URL to search."),
) -> dict[str, Any]:
    """
    Get all endpoints from an API.

    Get Endpoints Instructions:
    1. This tool returns all endpoints in "METHOD /path" format (e.g., "GET /users", "POST /orders/{id}").
    2. Use this tool to get all endpoints from an API before inspecting them and making requests.
    """

    try:
        logger.debug(f"Getting endpoints: {api_url}")
        api = API.load_from_sanitized_url(api_url)
        result = await api.get_endpoints()
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to search endpoints: {e}", exc_info=True)
        raise RuntimeError(f"Failed to search endpoints in {api_url} - {str(e)}") from e


async def api_inspect_endpoint(
    endpoint: Endpoint = Field(..., description="API endpoint to inspect."),
) -> dict[str, Any]:
    """
    Inspect the structure of an API endpoint.

    ALWAYS INSPECT ENDPOINTS BEFORE MAKING REQUESTS TO PREVENT ERRORS.
    ENSURE THE ENDPOINT EXISTS BEFORE ATTEMPTING TO INSPECT IT.

    Inspect Instructions:
    1. Use this tool to understand endpoint structure like request parameters, response schema, and authentication requirements
    2. Inspecting endpoints helps understand the structure of the data
    3. Always inspect endpoints before writing queries to understand their structure and prevent errors
    """
    try:
        logger.debug(f"Inspecting endpoint: {endpoint.api_url} {endpoint.path}")
        api = API.load_from_sanitized_url(endpoint.api_url)
        result = await api.inspect_endpoint(**endpoint.model_dump(exclude={"api_url"}))
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to inspect endpoint: {e}", exc_info=True)
        raise RuntimeError(f"Failed to inspect endpoint {endpoint.path} in {endpoint.api_url} - {str(e)}") from e


async def api_request(
    request: Request = Field(..., description="The request to make."),
) -> dict[str, Any]:
    """
    Request an API endpoint.

    NEVER PASS API KEYS OR SECRETS TO THIS TOOL. SECRETS AND API KEYS WILL BE AUTOMATICALLY INJECTED INTO THE REQUEST.

    Request API Instructions:
        1. Only make requests to endpoints that have been explicitly discovered, searched for, or referenced in the conversation.
        2. Before making requests, inspect the underlying endpoints to understand their config and prevent errors.
        3. When a request fails or returns unexpected results, examine the endpoint to diagnose the issue and then retry.
    """
    try:
        logger.debug(f"Requesting API: {request.api_url} {request.path}")
        api = API.load_from_sanitized_url(request.api_url)
        result = await api.request(**request.model_dump(exclude={"api_url", "description"}))
        return serialize_response(result)
    except Exception as e:
        logger.error(f"Failed to request API: {e}", exc_info=True)
        raise RuntimeError(f"Failed to request API in {request.api_url} - {str(e)}") from e
