"""Unit tests for configuration constants and validation."""

from toolfront.config import ALRU_CACHE_TTL, API_KEY_HEADER, BACKEND_URL, MAX_DATA_ROWS


class TestConfigConstants:
    """Test configuration constants are properly defined."""

    def test_max_data_rows_is_positive_integer(self):
        """Test that MAX_DATA_ROWS is a positive integer."""
        assert isinstance(MAX_DATA_ROWS, int)
        assert MAX_DATA_ROWS > 0
        # Reasonable limit for data export
        assert MAX_DATA_ROWS <= 10000

    def test_backend_url_is_string(self):
        """Test that BACKEND_URL is a string."""
        assert isinstance(BACKEND_URL, str)
        assert len(BACKEND_URL) > 0
        # Should look like a URL
        assert "://" in BACKEND_URL

    def test_api_key_header_is_string(self):
        """Test that API_KEY_HEADER is a string."""
        assert isinstance(API_KEY_HEADER, str)
        assert len(API_KEY_HEADER) > 0

    def test_alru_cache_ttl_is_positive_integer(self):
        """Test that ALRU_CACHE_TTL is a positive integer."""
        assert isinstance(ALRU_CACHE_TTL, int)
        assert ALRU_CACHE_TTL > 0
        # Reasonable cache time (not too short, not too long)
        assert 60 <= ALRU_CACHE_TTL <= 86400  # 1 minute to 1 day


class TestConfigValues:
    """Test specific configuration values are reasonable."""

    def test_max_data_rows_default_value(self):
        """Test the default MAX_DATA_ROWS value."""
        # Should be reasonable for API responses
        assert MAX_DATA_ROWS == 100

    def test_cache_ttl_default_value(self):
        """Test the default ALRU_CACHE_TTL value."""
        # Should be 1 hour (3600 seconds)
        assert ALRU_CACHE_TTL == 3600

    def test_backend_url_format(self):
        """Test that BACKEND_URL has expected format."""
        # Should be production API URL
        assert BACKEND_URL.startswith("https://")
        assert "api.kruskal.ai" in BACKEND_URL
