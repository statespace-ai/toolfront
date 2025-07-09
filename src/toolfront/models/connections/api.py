import logging
from urllib.parse import ParseResult, parse_qs, urlparse

from pydantic import Field

from toolfront.models.api import API
from toolfront.models.connection import Connection

logger = logging.getLogger("toolfront")


class APIConnection(Connection):
    """API connection."""

    url: str = Field(..., description="Full API URL.")

    async def connect(self) -> API:
        from toolfront.cache import load_openapi_spec_from_clean_url, load_spec_url_from_clean_url

        # Get the clean URL (this is what we'll use for the API connection)
        clean_url = str(self.url)

        # Load OpenAPI spec from clean URL
        openapi_spec = load_openapi_spec_from_clean_url(clean_url)

        # Get the original spec URL that contains auth parameters
        original_spec_url = load_spec_url_from_clean_url(clean_url)
        if not original_spec_url:
            raise ConnectionError(f"No spec URL found for URL: {clean_url}")

        # Parse the original spec URL to extract auth parameters
        url: ParseResult = urlparse(original_spec_url)
        query_params = parse_qs(url.query)
        # Convert from lists to single values
        query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        # Initialize auth containers
        auth_headers = {}
        auth_query_params = {}

        # Common auth parameter names
        auth_param_names = ["apikey", "api_key", "token", "access_token", "bearer", "key", "auth"]

        # Check OpenAPI spec for security schemes
        if openapi_spec and "components" in openapi_spec and "securitySchemes" in openapi_spec["components"]:
            for _scheme_name, scheme in openapi_spec["components"]["securitySchemes"].items():
                if scheme.get("type") == "apiKey":
                    param_name = scheme.get("name")
                    param_location = scheme.get("in", "query")

                    # Find matching parameter in query params (case-insensitive)
                    for qp_name, qp_value in list(query_params.items()):
                        if qp_name.lower() == param_name.lower():
                            if param_location == "header":
                                auth_headers[param_name] = qp_value
                                del query_params[qp_name]
                            elif param_location == "query":
                                auth_query_params[qp_name] = qp_value
                                del query_params[qp_name]
                            break
                elif scheme.get("type") == "http" and scheme.get("scheme") == "bearer":
                    # Look for bearer/token in query params
                    for qp_name, qp_value in list(query_params.items()):
                        if qp_name.lower() in ["bearer", "token", "access_token"]:
                            auth_headers["Authorization"] = f"Bearer {qp_value}"
                            del query_params[qp_name]
                            break
        else:
            # No spec or security schemes - use heuristics
            for qp_name, qp_value in list(query_params.items()):
                if qp_name.lower() in auth_param_names:
                    if qp_name.lower() in ["bearer", "token", "access_token"]:
                        auth_headers["Authorization"] = f"Bearer {qp_value}"
                        del query_params[qp_name]
                    else:
                        # Default to keeping in query params (like Polygon)
                        auth_query_params[qp_name] = qp_value
                        del query_params[qp_name]

        return API(
            url=clean_url, auth_headers=auth_headers, auth_query_params=auth_query_params, openapi_spec=openapi_spec
        )
