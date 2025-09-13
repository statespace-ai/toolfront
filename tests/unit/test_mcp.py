"""Unit tests for MCP functionality."""

import os
import tempfile
from pathlib import Path

from toolfront.mcp import load_env_file, process_database_url


class TestLoadEnvFile:
    """Test cases for load_env_file function."""

    def test_load_env_file_basic(self):
        """Test loading basic env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("DATABASE_URL=postgresql://localhost/test\n")
            f.write("DATABASE_PASSWORD=secret123\n")
            f.write("# This is a comment\n")
            f.write("\n")  # Empty line
            f.write("API_KEY=abc123\n")
            env_file = Path(f.name)

        try:
            # Clear any existing env vars
            old_values = {}
            for key in ["DATABASE_URL", "DATABASE_PASSWORD", "API_KEY"]:
                old_values[key] = os.environ.pop(key, None)

            load_env_file(env_file)

            assert os.environ["DATABASE_URL"] == "postgresql://localhost/test"
            assert os.environ["DATABASE_PASSWORD"] == "secret123"
            assert os.environ["API_KEY"] == "abc123"

        finally:
            # Cleanup
            for key, value in old_values.items():
                if value is not None:
                    os.environ[key] = value
                else:
                    os.environ.pop(key, None)
            env_file.unlink()

    def test_load_env_file_nonexistent(self):
        """Test that loading nonexistent file doesn't crash."""
        load_env_file(Path("nonexistent.env"))
        # Should not raise any exception


class TestProcessDatabaseUrl:
    """Test cases for process_database_url function."""

    def test_process_url_with_password_substitution(self):
        """Test URL processing with password substitution."""
        # Set up environment
        old_password = os.environ.get("DATABASE_PASSWORD")
        os.environ["DATABASE_PASSWORD"] = "foo*&%^#bar"

        try:
            url = "mssql://user:{password}@host"
            result = process_database_url(url)
            expected = "mssql://user:foo%2A%26%25%5E%23bar@host"
            assert result == expected

        finally:
            # Cleanup
            if old_password is not None:
                os.environ["DATABASE_PASSWORD"] = old_password
            else:
                os.environ.pop("DATABASE_PASSWORD", None)

    def test_process_url_without_placeholder(self):
        """Test URL processing without password placeholder."""
        url = "mssql://user:password@host"
        result = process_database_url(url)
        assert result == url

    def test_process_url_placeholder_no_env_var(self):
        """Test URL with placeholder but no env var."""
        # Ensure env var is not set
        old_password = os.environ.get("DATABASE_PASSWORD")
        os.environ.pop("DATABASE_PASSWORD", None)

        try:
            url = "mssql://user:{password}@host"
            result = process_database_url(url)
            # Should return URL with placeholder unchanged
            assert result == "mssql://user:{password}@host"

        finally:
            # Cleanup
            if old_password is not None:
                os.environ["DATABASE_PASSWORD"] = old_password

    def test_process_url_special_characters_encoding(self):
        """Test that special characters in password are properly URL encoded."""
        old_password = os.environ.get("DATABASE_PASSWORD")
        test_cases = [
            ("simple", "simple"),
            ("p@ssword", "p%40ssword"),
            ("pass#123", "pass%23123"),
            ("user$pwd!", "user%24pwd%21"),
            ("complex@#$%^&*()", "complex%40%23%24%25%5E%26%2A%28%29"),
        ]

        try:
            for password, expected_encoded in test_cases:
                os.environ["DATABASE_PASSWORD"] = password
                url = "postgresql://user:{password}@host/db"
                result = process_database_url(url)
                expected = f"postgresql://user:{expected_encoded}@host/db"
                assert result == expected

        finally:
            # Cleanup
            if old_password is not None:
                os.environ["DATABASE_PASSWORD"] = old_password
            else:
                os.environ.pop("DATABASE_PASSWORD", None)
