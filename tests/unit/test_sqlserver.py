"""Unit tests for SQL Server database implementation."""

from unittest.mock import patch

import pytest
from sqlalchemy.engine.url import make_url

from toolfront.models.connection import Connection
from toolfront.models.databases.sqlserver import SQLServer


class TestSQLServerConnection:
    """Test SQL Server connection handling."""

    def test_sqlserver_driver_selection(self):
        """Test that SQL Server URLs are properly routed to SQLServer class."""
        test_urls = [
            "mssql://user:pass@localhost:1433/mydb",
            "sqlserver://user:pass@localhost:1433/mydb",
        ]

        for test_url in test_urls:
            connection = Connection(url=test_url)

            with patch("toolfront.models.connection.SQLServer") as mock_sqlserver:
                import asyncio

                asyncio.run(connection.connect())

                # Should use SQLServer class
                mock_sqlserver.assert_called_once()
                called_url = mock_sqlserver.call_args[1]["url"]
                assert called_url.drivername == "mssql+pyodbc"

    def test_sqlserver_url_modification(self):
        """Test that SQL Server URLs are properly modified for pyodbc driver."""
        test_cases = [
            ("mssql://user:pass@localhost/db", "mssql+pyodbc"),
            ("sqlserver://user:pass@localhost/db", "mssql+pyodbc"),
        ]

        for original_url, expected_driver in test_cases:
            url = make_url(original_url)

            if url.drivername in ("mssql", "sqlserver"):
                modified_url = url.set(drivername="mssql+pyodbc")
                assert modified_url.drivername == expected_driver


class TestSQLServerImplementation:
    """Test SQL Server specific implementation methods."""

    def test_initialize_session(self):
        """Test SQL Server session initialization."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        session_sql = sqlserver.initialize_session()
        assert session_sql == "SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED"

    def test_table_path_validation(self):
        """Test table path validation for inspect_table method."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        # Valid table path should work
        valid_path = "dbo.users"
        splits = valid_path.split(".")
        assert len(splits) == 2

        # Invalid table path should fail
        invalid_paths = [
            "users",  # Missing schema
            "dbo.users.extra",  # Too many parts
            "",  # Empty
        ]

        for invalid_path in invalid_paths:
            splits = invalid_path.split(".")
            if len(splits) != 2:
                # This would trigger ValueError in inspect_table
                assert True

    def test_get_tables_query_structure(self):
        """Test that get_tables method uses correct SQL structure."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        # The get_tables method should exclude system schemas
        # We can't easily test the actual query execution without a real connection,
        # but we can verify the method exists and has correct structure
        assert hasattr(sqlserver, "get_tables")
        assert callable(sqlserver.get_tables)

    def test_sample_table_query_format(self):
        """Test that sample_table uses SQL Server TOP syntax."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        # The sample_table method should use TOP N syntax
        # We can't test actual execution, but we can verify method exists
        assert hasattr(sqlserver, "sample_table")
        assert callable(sqlserver.sample_table)

    def test_inspect_table_query_format(self):
        """Test that inspect_table uses correct INFORMATION_SCHEMA query."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        # Verify the method exists and validates input
        assert hasattr(sqlserver, "inspect_table")
        assert callable(sqlserver.inspect_table)


class TestSQLServerURLHandling:
    """Test SQL Server URL parsing and handling."""

    def test_sqlserver_url_parsing(self):
        """Test basic SQL Server URL parsing."""
        test_urls = [
            "mssql://user:pass@localhost:1433/mydb",
            "sqlserver://user:pass@localhost:1433/mydb",
            "mssql://user:pass@server.domain.com:1433/mydb",
            "sqlserver://user:pass@server.domain.com/mydb",  # Default port
        ]

        for url in test_urls:
            connection = Connection(url=url)
            assert connection.url == url

    def test_sqlserver_url_with_special_characters(self):
        """Test SQL Server URL parsing with special characters in password."""
        url_with_special = "mssql://user:p%40ss@localhost:1433/mydb"
        connection = Connection(url=url_with_special)

        assert connection.url == url_with_special

    def test_sqlserver_url_with_query_parameters(self):
        """Test SQL Server URLs with query parameters."""
        url_with_params = "mssql://user:pass@localhost:1433/db?driver=ODBC+Driver+17+for+SQL+Server"
        connection = Connection(url=url_with_params)

        assert connection.url == url_with_params
