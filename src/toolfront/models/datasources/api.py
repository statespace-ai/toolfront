import json
from abc import ABC
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml
from pydantic import Field, model_validator

from toolfront.config import TIMEOUT_SECONDS
from toolfront.models.actions.request import Request
from toolfront.models.datasources.base import DataSource
from toolfront.types import HTTPMethod


class API(DataSource, ABC):
    """Abstract base class for OpenAPI/Swagger-based APIs."""

    url: str = Field(..., description="API URL.")
    endpoints: list[str] = Field(..., description="List of available endpoints.")
    spec: dict | str = Field(..., description="API specification config.", exclude=True)
    headers: dict[str, str] | None = Field(None, description="Additional headers to include in requests.", exclude=True)
    params: dict[str, str] | None = Field(None, description="Query parameters to include in requests.", exclude=True)

    def __init__(
        self,
        url: str | None = None,
        spec: dict | str | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(url=url, spec=spec, headers=headers, params=params, **kwargs)

    @model_validator(mode="before")
    def validate_model(cls, v: Any) -> Any:
        spec = v.get("spec")

        if isinstance(spec, str):
            parsed_url = urlparse(spec)
            match parsed_url.scheme:
                case "file":
                    path = Path(parsed_url.path)
                    if not path.exists():
                        raise ConnectionError(f"OpenAPI spec file not found: {path}")
                    with path.open() as f:
                        v["spec"] = yaml.safe_load(f) if path.suffix.lower() in [".yaml", ".yml"] else json.load(f)
                case "http" | "https":
                    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
                        response = client.get(parsed_url.geturl())
                        response.raise_for_status()
                        v["spec"] = response.json()
                case _:
                    raise ValueError("Invalid API spec URL")

            v["params"] = dict(pair.split("=") for pair in parsed_url.query.split("&") if pair) or None
        elif not isinstance(spec, dict):
            raise ValueError("Invalid API spec. Must be a URL string or a dictionary.")

        # Get the API URL from the spec
        v["url"] = v["spec"].get("servers", [{}])[0].get("url")

        # Get the endpoints from the spec
        paths = v["spec"].get("paths", {})

        if not paths:
            raise RuntimeError("No endpoints found in OpenAPI spec")

        endpoints = []
        for path, methods in paths.items():
            for method in methods:
                if method.upper() in [http_method.value.upper() for http_method in HTTPMethod]:
                    endpoints.append(f"{method.upper()} {path}")

        v["endpoints"] = endpoints

        return v

    def tools(self) -> list[callable]:
        return [self.inspect_endpoint, self.request]

    async def inspect_endpoint(self, method: HTTPMethod, path: str) -> dict[str, Any]:
        """
        Inspect the structure of an API endpoint.

        TO PREVENT ERRORS, ALWAYS ENSURE THE ENDPOINT EXISTS BEFORE INSPECTING IT.

        Inspect Instructions:
        1. Use this tool to understand endpoint structure like request parameters and response schema
        2. Inspecting endpoints helps understand the structure of the data
        3. Always inspect endpoints before writing queries to understand their structure and prevent errors
        """
        inspect = self.spec.get("paths", {}).get(path, {}).get(method.lower(), {})
        if not inspect:
            raise RuntimeError(f"Endpoint not found: {method} {path}")
        return inspect

    async def request(
        self,
        request: Request,
    ) -> Any:
        """
        Request an API endpoint.

            TO PREVENT ERRORS, ALWAYS ENSURE ENDPOINTS EXIST AND YOU ARE USING THE CORRECT METHOD, PATH, AND PARAMETERS.
        NEVER PASS API KEYS OR SECRETS TO THIS TOOL. SECRETS AND API KEYS WILL BE AUTOMATICALLY INJECTED INTO THE REQUEST.

        Request API Instructions:
            1. Only make requests to endpoints that have been explicitly discovered, searched for, or referenced in the conversation.
            2. Before making requests, inspect the underlying endpoints to understand their config and prevent errors.
            3. When a request fails or returns unexpected results, examine the endpoint to diagnose the issue and then retry.
        """

        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.request(
                method=request.method.upper(),
                url=f"{self.url}{request.path}",
                json=request.body,
                params={**(request.params or {}), **(self.params or {})},
                headers={**(request.headers or {}), **(self.headers or {})},
            )
            response.raise_for_status()
            return response.json()

    def _retrieve_class(self) -> type:
        return Request

    def _retrieve_function(self) -> Any:
        return self.request
