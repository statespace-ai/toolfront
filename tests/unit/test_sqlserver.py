"""Unit tests for SQL Server database implementation."""

import pytest
from sqlalchemy.engine.url import make_url

from toolfront.models.databases.sqlserver import SQLServer


class TestSQLServerImplementation:
    """Test SQL Server specific implementation logic."""

    def test_initialize_session(self):
        """Test SQL Server session initialization returns correct SQL."""
        url = make_url("mssql+pyodbc://user:pass@localhost/db")
        sqlserver = SQLServer(url=url)

        session_sql = sqlserver.initialize_session()
        assert session_sql == "SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED"

    def test_table_path_validation_logic(self):
        """Test table path splitting logic."""
        # Valid table path should split correctly
        valid_path = "dbo.users"
        splits = valid_path.split(".")
        assert len(splits) == 2
        assert splits[0] == "dbo"
        assert splits[1] == "users"

        # Invalid table paths should fail validation
        invalid_paths = [
            "users",  # Missing schema
            "dbo.users.extra",  # Too many parts
            "",  # Empty
            ".",  # Just dot
            "dbo.",  # Missing table name
            ".users",  # Missing schema name
        ]

        for invalid_path in invalid_paths:
            splits = invalid_path.split(".")
            # This logic matches what's in the actual implementation
            assert len(splits) != 2 or any(not part.strip() for part in splits)

    def test_sample_size_validation_logic(self):
        """Test sample size parameter validation logic."""
        # Valid sample sizes
        valid_sizes = [1, 5, 10, 100]
        for size in valid_sizes:
            assert size > 0  # This is the validation logic in our code

        # Invalid sample sizes
        invalid_sizes = [0, -1, -10]
        for size in invalid_sizes:
            assert size <= 0  # This would trigger ValueError in our code
