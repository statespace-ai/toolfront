from enum import Enum


class HTTPMethod(str, Enum):
    """Valid HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

    @classmethod
    def get_supported_methods(cls) -> set[str]:
        """Get all supported HTTP methods."""
        return {method.value for method in cls}
