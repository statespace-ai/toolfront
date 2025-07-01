import logging
from abc import ABC
from typing import Any
from urllib.parse import ParseResult, urlparse

import httpx
from pydantic import BaseModel, Field, field_validator

from toolfront.utils import ConnectionResult, SearchMode, search_items

logger = logging.getLogger("toolfront")


class APIError(Exception):
    """Exception for API-related errors."""

    pass


class API(BaseModel, ABC):
    """Abstract base class for OpenAPI-based APIs."""

    url: ParseResult = Field(description="URL of the API")
    openapi_spec: dict[str, Any] = Field(default_factory=dict, description="OpenAPI specification.")
    query_params: dict[str, Any] | None = Field(None, description="Additional request parameters.")

    @field_validator("url", mode="before")
    def validate_url(cls, v: Any) -> ParseResult:
        if isinstance(v, str):
            v = urlparse(v)

        return v  # type: ignore[no-any-return]

    async def test_connection(self) -> ConnectionResult:
        """Test the connection to the API."""
        if self.openapi_spec is not None:
            return ConnectionResult(connected=True, message="API connection successful")
        else:
            return ConnectionResult(connected=False, message="API connection failed")

    async def get_endpoints(self) -> list[str]:
        """Get the available endpoints from the OpenAPI specification."""
        endpoints = []
        for path, methods in self.openapi_spec.get("paths", {}).items():
            for method in methods:
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
                    endpoints.append(f"{method.upper()} {path}")

        return endpoints

    async def inspect_endpoint(self, method: str, path: str) -> dict[str, Any]:
        """Inspect the details of a specific endpoint."""

        method = method.lower()

        endpoint_spec = self.openapi_spec.get("paths", {}).get(path, {}).get(method, {})
        if not endpoint_spec:
            raise APIError(f"Endpoint not found: {method} {path}")

        # Add some additional useful information
        return endpoint_spec

    async def search_endpoints(self, pattern: str, mode: SearchMode = SearchMode.REGEX, limit: int = 10) -> list[str]:
        """Search for endpoints using different algorithms."""
        endpoints = await self.get_endpoints()
        try:
            return search_items(endpoints, pattern, mode, limit)
        except Exception as e:
            logger.error(f"Endpoint search failed: {e}")
            raise APIError(f"Endpoint search failed: {e}") from e

    async def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        """
        Make a request to the API endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            path: The API endpoint path (e.g., "/users")
            body: Request body (for POST, PUT, etc.)
            headers: Additional headers to include

        Returns:
            Response data (typically JSON)

        Raises:
            APIError: If an invalid HTTP method is provided
        """

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method.upper(),
                url=f"{self.url.geturl()}{path}",
                json=body,
                params=(params or {}) | self.query_params,
                headers=headers,
            )
            return response.json()
