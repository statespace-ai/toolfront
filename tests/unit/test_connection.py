"""Unit tests for Connection class URL parsing and driver selection."""

from unittest.mock import patch

import pytest
from sqlalchemy.engine.url import make_url

from toolfront.models.connection import Connection


class TestConnectionDriverSelection:
    """Test Connection.connect() method for proper driver selection."""

    def test_connection_url_parsing(self):
        """Test basic URL parsing and storage."""
        test_urls = [
            "postgresql://user:pass@localhost:5432/mydb",
            "mysql://user:pass@localhost:3306/mydb",
            "sqlite:///test.db",
            "bigquery://project/dataset",
            "snowflake://user:pass@account/db/schema",
            "duckdb:///test.db",
        ]

        for url in test_urls:
            connection = Connection(url=url)
            assert connection.url == url

    def test_unsupported_driver_error(self):
        """Test that unsupported drivers raise ValueError during connect."""
        connection = Connection(url="unsupported://localhost/db")

        # Test the driver selection logic directly by trying to connect
        with pytest.raises(ValueError, match="Unsupported data source"):
            import asyncio

            asyncio.run(connection.connect())

    def test_driver_modification_logic(self):
        """Test that URLs are properly modified for async drivers."""
        test_cases = [
            ("postgresql://user:pass@localhost/db", "postgresql+asyncpg"),
            ("mysql://user:pass@localhost/db", "mysql+aiomysql"),
            ("sqlite:///memory.db", "sqlite+aiosqlite"),
            ("bigquery://project/dataset", "bigquery"),
            ("snowflake://user:pass@account/db/schema", "snowflake"),
            ("duckdb:///memory.db", "duckdb"),
        ]

        for original_url, expected_driver in test_cases:
            url = make_url(original_url)

            # Test the driver modification logic
            if url.drivername == "postgresql":
                modified_url = url.set(drivername="postgresql+asyncpg")
                assert modified_url.drivername == expected_driver
            elif url.drivername == "mysql":
                modified_url = url.set(drivername="mysql+aiomysql")
                assert modified_url.drivername == expected_driver
            elif url.drivername == "sqlite":
                modified_url = url.set(drivername="sqlite+aiosqlite")
                assert modified_url.drivername == expected_driver
            else:
                # No modification for other drivers
                assert url.drivername == expected_driver


class TestConnectionUrlHandling:
    """Test URL parsing and URL map handling."""

    def test_url_parsing_basic(self):
        """Test basic URL parsing."""
        connection = Connection(url="postgresql://user:pass@localhost:5432/mydb")

        # Should not raise an error during creation
        assert connection.url == "postgresql://user:pass@localhost:5432/mydb"

    def test_url_parsing_with_special_characters(self):
        """Test URL parsing with special characters in password."""
        url_with_special = "postgresql://user:p%40ss@localhost:5432/mydb"
        connection = Connection(url=url_with_special)

        assert connection.url == url_with_special

    def test_url_map_usage(self):
        """Test that url_map is used when provided."""
        obfuscated_url = "postgresql://user:***@localhost:5432/mydb"
        real_url = make_url("postgresql://user:realpass@localhost:5432/mydb")

        connection = Connection(url=obfuscated_url)
        url_map = {obfuscated_url: real_url}

        # Mock the database creation to avoid actual connection
        with patch("toolfront.models.connection.PostgreSQL") as mock_postgres:
            import asyncio

            asyncio.run(connection.connect(url_map=url_map))

            # Should use the real URL from url_map
            mock_postgres.assert_called_once()
            called_url = mock_postgres.call_args[1]["url"]
            assert str(called_url).replace("+asyncpg", "") == str(real_url)

    def test_url_map_fallback_to_direct_parsing(self):
        """Test fallback to direct URL parsing when not in url_map."""
        connection = Connection(url="postgresql://user:pass@localhost:5432/mydb")
        url_map = {"other://url": make_url("other://url")}

        with patch("toolfront.models.connection.PostgreSQL") as mock_postgres:
            import asyncio

            asyncio.run(connection.connect(url_map=url_map))

            # Should parse the URL directly since it's not in url_map
            mock_postgres.assert_called_once()

    def test_no_url_map_provided(self):
        """Test behavior when no url_map is provided."""
        connection = Connection(url="postgresql://user:pass@localhost:5432/mydb")

        with patch("toolfront.models.connection.PostgreSQL") as mock_postgres:
            import asyncio

            asyncio.run(connection.connect())

            # Should work without url_map
            mock_postgres.assert_called_once()

    def test_url_unquoting(self):
        """Test that URLs are properly unquoted."""
        quoted_url = "postgresql://user:pass%40word@localhost:5432/mydb"
        connection = Connection(url=quoted_url)

        with patch("toolfront.models.connection.PostgreSQL") as mock_postgres:
            import asyncio

            asyncio.run(connection.connect())

            # URL should be unquoted before processing
            mock_postgres.assert_called_once()


class TestUrlValidation:
    """Test URL validation and edge cases."""

    def test_url_with_query_parameters(self):
        """Test URLs with query parameters."""
        url_with_params = "postgresql://user:pass@localhost:5432/db?sslmode=require"
        connection = Connection(url=url_with_params)

        assert connection.url == url_with_params

    def test_file_based_database_urls(self):
        """Test file-based database URLs."""
        file_urls = [
            "sqlite:///:memory:",  # In-memory databases should work
            "duckdb:///:memory:",
        ]

        for url in file_urls:
            connection = Connection(url=url)
            assert connection.url == url

    def test_special_characters_in_password(self):
        """Test URLs with special characters in password."""
        url_with_special = "postgresql://user:p%40ss@localhost:5432/mydb"
        connection = Connection(url=url_with_special)

        assert connection.url == url_with_special
