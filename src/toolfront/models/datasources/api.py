import json
from abc import ABC
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import yaml
from pydantic import Field, model_validator

from toolfront.config import TIMEOUT_SECONDS
from toolfront.models.datasources.base import DataSource
from toolfront.types import HTTPMethod


class API(DataSource, ABC):
    """Abstract base class for OpenAPI/Swagger-based APIs."""

    spec_url: str | None = Field(None, description="API specification URL. Mutually exclusive with spec.")
    spec_config: dict | None = Field(None, description="API specification config. Mutually exclusive with spec_url.")
    headers: dict[str, str] | None = Field(None, description="Additional headers to include in requests.")
    params: dict[str, str] | None = Field(None, description="Query parameters to include in requests.")

    @model_validator(mode="after")
    def validate_model(self) -> "API":
        if self.spec_url is not None and self.spec_config is not None:
            raise ValueError("Either spec_url or spec_config must be provided")

        if self.spec_url is not None:
            match self.spec_scheme:
                case "file":
                    path = self.spec_path
                    if not path.exists():
                        raise ConnectionError(f"OpenAPI spec file not found: {path}")
                    with path.open() as f:
                        self.spec_config = (
                            yaml.safe_load(f) if path.suffix.lower() in [".yaml", ".yml"] else json.load(f)
                        )
                case "http" | "https":
                    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
                        response = client.get(self.spec_url)
                        response.raise_for_status()
                        self.spec_config = response.json()
                case _:
                    raise ValueError("Invalid url")
                
        return self

    def sanitized_url(self) -> str:
        return str(self.api_url)

    @classmethod
    def create_from_url(cls, url: str) -> "API":
        parsed_url = urlparse(url)

        if parsed_url.query:
            try:
                query_params = dict(pair.split("=") for pair in parsed_url.query.split("&") if pair)
            except Exception as e:
                raise ValueError(f"Failed to parse query parameters: {e}") from e
        else:
            query_params = None

        return cls(spec_url=url, params=query_params)

    def __str__(self) -> str:
        return f"API(url={self.api_url})"

    def __repr__(self) -> str:
        return f"API(url={self.api_url}, headers={self.headers}, params={self.params})"

    @property
    def spec_scheme(self) -> str:
        parsed_url = urlparse(self.spec_url)
        return parsed_url.scheme

    @property
    def spec_path(self) -> Path:
        parsed_url = urlparse(self.spec_url)
        return Path(parsed_url.path)

    @property
    def api_url(self) -> str:
        """Get the API URL."""
        url = self.spec_config.get("servers", [{}])[0].get("url")
        if not url:
            raise RuntimeError("No API URL found in OpenAPI spec")
        return url

    async def get_endpoints(self) -> list[str]:
        """Get the available endpoints from the OpenAPI/Swagger specification."""
        paths = self.spec_config.get("paths", {})

        if not paths:
            raise RuntimeError("No endpoints found in OpenAPI spec")

        endpoints = []
        for path, methods in paths.items():
            for method in methods:
                if method.upper() in [http_method.value.upper() for http_method in HTTPMethod]:
                    endpoints.append(f"{method.upper()} {path}")
        return endpoints

    async def inspect_endpoint(self, method: str, path: str) -> dict[str, Any]:
        """Inspect the details of a specific endpoint."""
        inspect = self.spec_config.get("paths", {}).get(path, {}).get(method.lower(), {})
        if not inspect:
            raise RuntimeError(f"Endpoint not found: {method} {path}")
        return inspect

    async def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Any:
        """Make a request to the API endpoint."""

        all_params = {**(params or {}), **(self.params or {})}
        all_headers = {**(headers or {}), **(self.headers or {})}

        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.request(
                method=method.upper(),
                url=f"{self.api_url}{path}",
                json=body,
                params=all_params,
                headers=all_headers,
            )
            response.raise_for_status()
            return response.json()
