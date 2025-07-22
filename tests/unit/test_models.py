"""Unit tests for model validation logic in toolfront.models."""

import pytest
from pydantic import ValidationError

from toolfront.models.api import Endpoint, HTTPMethod, Request
from toolfront.models.database import Table
from toolfront.models.library import Read


class TestHTTPMethod:
    """Test cases for HTTPMethod enum."""

    def test_valid_methods(self):
        """Test all valid HTTP methods."""
        assert HTTPMethod.GET.value == "GET"
        assert HTTPMethod.POST.value == "POST"
        assert HTTPMethod.PUT.value == "PUT"
        assert HTTPMethod.DELETE.value == "DELETE"
        assert HTTPMethod.PATCH.value == "PATCH"
        assert HTTPMethod.HEAD.value == "HEAD"
        assert HTTPMethod.OPTIONS.value == "OPTIONS"

    def test_get_supported_methods(self):
        """Test getting all supported methods."""
        supported = HTTPMethod.get_supported_methods()
        assert isinstance(supported, set)
        assert "GET" in supported
        assert "POST" in supported
        assert len(supported) == 7


class TestEndpoint:
    """Test cases for Endpoint model."""

    def test_valid_endpoint(self):
        """Test creating valid endpoints."""
        endpoint = Endpoint(method=HTTPMethod.GET, path="/users")
        assert endpoint.method == HTTPMethod.GET
        assert endpoint.path == "/users"

    def test_endpoint_with_path_params(self):
        """Test endpoint with path parameters."""
        endpoint = Endpoint(method=HTTPMethod.GET, path="/users/{id}")
        assert endpoint.path == "/users/{id}"

    def test_endpoint_with_multiple_params(self):
        """Test endpoint with multiple path parameters."""
        endpoint = Endpoint(method=HTTPMethod.PUT, path="/users/{userId}/posts/{postId}")
        assert endpoint.path == "/users/{userId}/posts/{postId}"

    def test_invalid_method(self):
        """Test that invalid HTTP method raises error."""
        with pytest.raises(ValidationError):
            Endpoint(method="INVALID", path="/users")


class TestRequest:
    """Test cases for Request model."""

    def test_minimal_request(self):
        """Test creating request with only required fields."""
        endpoint = Endpoint(method=HTTPMethod.GET, path="/users")
        request = Request(endpoint=endpoint)
        assert request.endpoint == endpoint
        assert request.path_params is None
        assert request.body is None
        assert request.headers is None
        assert request.params is None

    def test_request_with_all_fields(self):
        """Test creating request with all optional fields."""
        endpoint = Endpoint(method=HTTPMethod.POST, path="/users/{id}")
        request = Request(
            endpoint=endpoint,
            path_params={"id": "123"},
            body={"name": "John", "email": "john@example.com"},
            headers={"Authorization": "Bearer token"},
            params={"include": "profile"}
        )
        assert request.path_params == {"id": "123"}
        assert request.body == {"name": "John", "email": "john@example.com"}
        assert request.headers == {"Authorization": "Bearer token"}
        assert request.params == {"include": "profile"}

    def test_request_field_descriptions(self):
        """Test that field descriptions are set correctly."""
        fields = Request.model_fields
        assert "endpoint" in fields
        assert "path_params" in fields
        assert "Optional path parameters" in fields["path_params"].description
        assert "Optional request body" in fields["body"].description


class TestTable:
    """Test cases for Table model."""

    def test_simple_table_name(self):
        """Test creating table with simple name."""
        table = Table(path="users")
        assert table.path == "users"

    def test_schema_qualified_table(self):
        """Test creating table with schema."""
        table = Table(path="public.users")
        assert table.path == "public.users"

    def test_fully_qualified_table(self):
        """Test creating table with database.schema.table format."""
        table = Table(path="mydb.public.users")
        assert table.path == "mydb.public.users"

    def test_table_field_description(self):
        """Test that field description is set correctly."""
        field = Table.model_fields["path"]
        assert "Full table path in dot notation" in field.description


class TestRead:
    """Test cases for Read model."""

    def test_read_with_section_number(self):
        """Test creating read request with section number."""
        read = Read(document_path="docs/manual.pdf", pagination=1)
        assert read.document_path == "docs/manual.pdf"
        assert read.pagination == 1

    def test_read_with_percentile(self):
        """Test creating read request with percentile."""
        read = Read(document_path="report.docx", pagination=0.5)
        assert read.document_path == "report.docx"
        assert read.pagination == 0.5

    def test_read_edge_percentiles(self):
        """Test edge cases for percentile values."""
        # Start of document
        read = Read(document_path="doc.txt", pagination=0.0)
        assert read.pagination == 0.0

        # Near end of document
        read = Read(document_path="doc.txt", pagination=0.99)
        assert read.pagination == 0.99

    def test_read_field_descriptions(self):
        """Test that field descriptions are set correctly."""
        fields = Read.model_fields
        assert "document_path" in fields
        assert "pagination" in fields
        assert "Section navigation" in fields["pagination"].description


class TestLibraryPaginationLogic:
    """Test cases for library pagination calculations."""

    def test_pagination_percentile_calculation(self):
        """Test percentile to section index conversion."""
        # Test data
        total_sections = 10
        
        # 0% should be first section (index 0)
        section_index = min(int(0.0 * total_sections), total_sections - 1)
        assert section_index == 0
        
        # 50% should be middle section (index 5)
        section_index = min(int(0.5 * total_sections), total_sections - 1)
        assert section_index == 5
        
        # 99% should be last section (index 9)
        section_index = min(int(0.99 * total_sections), total_sections - 1)
        assert section_index == 9

    def test_pagination_section_number_calculation(self):
        """Test section number to index conversion."""
        total_sections = 10
        
        # Section 1 should be index 0
        section_index = min(int(1) - 1, total_sections - 1)
        assert section_index == 0
        
        # Section 10 should be index 9
        section_index = min(int(10) - 1, total_sections - 1)
        assert section_index == 9
        
        # Section 20 (out of bounds) should clamp to index 9
        section_index = min(int(20) - 1, total_sections - 1)
        assert section_index == 9

    def test_chunk_boundary_calculation(self):
        """Test chunk boundary calculations."""
        CHUNK_SIZE = 10000
        document_length = 25000  # 3 chunks
        
        # First chunk
        section_index = 0
        start_idx = section_index * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, document_length)
        assert start_idx == 0
        assert end_idx == 10000
        
        # Second chunk
        section_index = 1
        start_idx = section_index * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, document_length)
        assert start_idx == 10000
        assert end_idx == 20000
        
        # Third (partial) chunk
        section_index = 2
        start_idx = section_index * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, document_length)
        assert start_idx == 20000
        assert end_idx == 25000