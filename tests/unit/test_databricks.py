"""
Unit tests for Databricks integration
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import pandas as pd
from sqlalchemy.engine.url import make_url

from toolfront.models.databases.databricks import Databricks
from toolfront.models.database import MatchMode


def test_databricks_initialization():
    """Test that a Databricks instance can be created."""
    url = make_url("databricks://hostname:443/database?http_path=/path&token=token")
    db = Databricks(url=url)
    assert db.url.drivername == "databricks"
    assert db.url.host == "hostname"
    assert db.url.port == 443
    assert db.url.database == "database"
    assert db.url.query["http_path"] == "/path"
    assert db.url.query["token"] == "token"


@pytest.mark.asyncio
async def test_get_tables():
    """Test get_tables method."""
    # Create mock DataFrame that would be returned by query
    mock_df = pd.DataFrame({
        0: ["catalog1", "catalog1", "catalog2"],
        1: ["schema1", "schema2", "schema1"],
        2: ["table1", "table2", "table3"]
    })
    
    # Create Databricks instance
    url = make_url("databricks://hostname:443/database?http_path=/path&token=token")
    db = Databricks(url=url)
    
    # Mock the query method
    db.query = AsyncMock(return_value=mock_df)
    
    # Call get_tables
    tables = await db.get_tables()
    
    # Verify results
    assert len(tables) == 3
    assert "catalog1.schema1.table1" in tables
    assert "catalog1.schema2.table2" in tables
    assert "catalog2.schema1.table3" in tables
    
    # Verify query was called
    db.query.assert_called_once()
    # We don't check the exact query because it may vary based on Databricks version


@pytest.mark.asyncio
async def test_scan_tables():
    """Test scan_tables method."""
    # Create Databricks instance
    url = make_url("databricks://hostname:443/database?http_path=/path&token=token")
    db = Databricks(url=url)
    
    # Mock get_tables method
    mock_tables = ["catalog1.schema1.customer", "catalog1.schema1.order", "catalog2.schema1.product"]
    db.get_tables = AsyncMock(return_value=mock_tables)
    
    # Test regex mode
    result = await db.scan_tables(pattern="customer", mode=MatchMode.REGEX)
    assert len(result) == 1
    assert "catalog1.schema1.customer" in result
    
    # Test with different pattern
    result = await db.scan_tables(pattern="schema1", mode=MatchMode.REGEX)
    assert len(result) == 3  # All contain schema1
    
    # Test with non-existent pattern
    result = await db.scan_tables(pattern="nonexistent", mode=MatchMode.REGEX)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_inspect_table():
    """Test inspect_table method."""
    # Create mock DataFrame that would be returned by query
    mock_df = pd.DataFrame({
        "column_name": ["id", "name", "age"],
        "data_type": ["INT", "VARCHAR", "INT"],
        "is_nullable": ["NO", "YES", "YES"],
        "column_default": [None, None, None],
        "ordinal_position": [1, 2, 3]
    })
    
    # Create Databricks instance
    url = make_url("databricks://hostname:443/database?http_path=/path&token=token")
    db = Databricks(url=url)
    
    # Mock the query method
    db.query = AsyncMock(return_value=mock_df)
    
    # Call inspect_table
    result = await db.inspect_table("catalog1.schema1.customer")
    
    # Verify results
    assert len(result) == 3  # 3 rows
    assert list(result["column_name"]) == ["id", "name", "age"]
    
    # Verify query was called with correct SQL
    db.query.assert_called_once()
    call_args = db.query.call_args[0][0]
    assert "catalog1.information_schema.columns" in call_args
    assert "table_schema = 'schema1'" in call_args
    assert "table_name = 'customer'" in call_args
    
    # Test with invalid table path
    with pytest.raises(ValueError, match="Invalid table path"):
        await db.inspect_table("invalid_path")


@pytest.mark.asyncio
async def test_sample_table():
    """Test sample_table method."""
    # Create mock DataFrame that would be returned by query
    mock_df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    
    # Create Databricks instance
    url = make_url("databricks://hostname:443/database?http_path=/path&token=token")
    db = Databricks(url=url)
    
    # Mock the query method
    db.query = AsyncMock(return_value=mock_df)
    
    # Call sample_table
    result = await db.sample_table("catalog1.schema1.customer", n=3)
    
    # Verify results
    assert len(result) == 3  # 3 rows
    assert list(result["name"]) == ["Alice", "Bob", "Charlie"]
    
    # Verify query was called with correct SQL
    db.query.assert_called_once()
    query = db.query.call_args[0][0]
    assert "SELECT * FROM catalog1.schema1.customer" in query
    assert "LIMIT 3" in query
    
    # Test with invalid table path
    with pytest.raises(ValueError, match="Invalid table path"):
        await db.sample_table("")