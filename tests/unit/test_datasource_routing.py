"""Unit tests for DataSource.from_url() routing logic."""

import pytest

from toolfront.models.base import DataSource


class TestDataSourceRouting:
    """Test the URL routing logic in DataSource.from_url()."""

    def test_routing_logic(self):
        """Test that different URL patterns route correctly."""
        # Each URL will fail to instantiate, but we can check which class it tried to create
        # by looking at the error message

        test_cases = [
            # HTTP URLs should try to create API
            ("http://api.example.com", ["errno", "connect", "getaddrinfo"]),  # API tries to fetch URL
            ("https://secure.api.com", ["errno", "connect", "getaddrinfo"]),
            # File URLs with API extensions should try to create API
            ("file:///path/to/spec.json", ["spec", "does not exist", "no such file"]),
            ("file:///path/to/spec.yaml", ["spec", "does not exist", "no such file"]),
            ("file:///path/to/spec.yml", ["spec", "does not exist", "no such file"]),
            # File URLs without API extensions should try to create Library
            ("file:///path/to/documents", ["path", "does not exist", "no such file"]),
            ("file:///path/to/library.pdf", ["path", "does not exist", "no such file"]),
            # Database URLs should try to create Database (will fail on missing drivers)
            ("postgresql://localhost/db", ["postgres", "backend", "import"]),
            ("mysql://localhost/db", ["mysql", "backend", "import"]),
            ("sqlite:///path/to/db.sqlite", ["sqlite", "backend", "import", "does not exist"]),
            # Case sensitivity checks
            ("HTTP://EXAMPLE.COM", ["connect", "database", "validation error"]),  # Uppercase HTTP -> Database
            ("file:///path/to/spec.JSON", ["path", "does not exist"]),  # Uppercase extension -> Library
        ]

        for url, expected_error_keywords in test_cases:
            with pytest.raises(Exception) as exc_info:
                DataSource.from_url(url)

            error_msg = str(exc_info.value).lower()
            assert any(keyword in error_msg for keyword in expected_error_keywords), (
                f"URL {url} error '{exc_info.value}' doesn't contain any of {expected_error_keywords}"
            )
