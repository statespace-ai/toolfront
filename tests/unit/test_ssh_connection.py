"""Unit tests for SSH tunnel connection functionality."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from toolfront.models.connection import Connection, SSHTunnelledDatabase
from toolfront.ssh import SSHConfig


class TestSSHConnection:
    """Test SSH tunnel integration with Connection class."""

    @patch('toolfront.models.connection.extract_ssh_params')
    async def test_connection_detects_ssh_params(self, mock_extract):
        """Test that Connection detects SSH parameters in URL."""
        # Setup mock
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        mock_extract.return_value = ("postgresql://user:pass@db.example.com:5432/mydb", ssh_config)
        
        url_with_ssh = (
            "postgresql://user:pass@db.example.com:5432/mydb"
            "?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/path/to/key.pem"
        )
        
        connection = Connection(url=url_with_ssh)
        db = await connection.connect()
        
        assert isinstance(db, SSHTunnelledDatabase)
        assert db.ssh_config == ssh_config
        mock_extract.assert_called_once_with(url_with_ssh)

    @patch('toolfront.models.connection.extract_ssh_params')
    async def test_connection_no_ssh_params(self, mock_extract):
        """Test Connection without SSH parameters."""
        mock_extract.return_value = ("postgresql://user:pass@db.example.com:5432/mydb", None)
        
        url_without_ssh = "postgresql://user:pass@db.example.com:5432/mydb"
        
        connection = Connection(url=url_without_ssh)
        db = await connection.connect()
        
        # Should return a regular PostgreSQL database, not SSH tunnelled
        assert not isinstance(db, SSHTunnelledDatabase)
        assert db.__class__.__name__ == "PostgreSQL"

    @patch('toolfront.models.connection.extract_ssh_params')
    async def test_connection_ssh_unsupported_database(self, mock_extract):
        """Test SSH tunnel with unsupported database type."""
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        mock_extract.return_value = ("bigquery://project/dataset", ssh_config)
        
        url_with_ssh = "bigquery://project/dataset?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/key.pem"
        
        connection = Connection(url=url_with_ssh)
        
        with pytest.raises(ValueError, match="SSH tunnels are not yet supported for bigquery"):
            await connection.connect()

    @patch('toolfront.models.connection.extract_ssh_params')
    async def test_connection_with_url_map(self, mock_extract):
        """Test Connection with URL mapping and SSH parameters."""
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        # Mock the extract function to handle the mapped URL
        def mock_extract_side_effect(url):
            if "real_password" in url:
                return ("postgresql://user:real_password@db.example.com:5432/mydb", ssh_config)
            return (url, None)
        
        mock_extract.side_effect = mock_extract_side_effect
        
        obfuscated_url = "postgresql://user:***@db.example.com:5432/mydb?ssh_host=bastion&ssh_user=ubuntu&ssh_key_path=/key.pem"
        real_url = "postgresql://user:real_password@db.example.com:5432/mydb?ssh_host=bastion&ssh_user=ubuntu&ssh_key_path=/key.pem"
        
        url_map = {obfuscated_url: real_url}
        
        connection = Connection(url=obfuscated_url)
        db = await connection.connect(url_map=url_map)
        
        assert isinstance(db, SSHTunnelledDatabase)
        # The extract function should have been called with the real URL
        mock_extract.assert_called_with(real_url)


class TestSSHTunnelledDatabase:
    """Test SSHTunnelledDatabase functionality."""

    def test_ssh_tunnelled_database_creation(self):
        """Test creation of SSH tunnelled database."""
        from sqlalchemy.engine.url import make_url
        
        url = make_url("postgresql://user:pass@db.example.com:5432/mydb")
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
        
        assert db.url == url
        assert db.ssh_config == ssh_config
        assert db._tunnel_manager is not None

    @patch('toolfront.models.connection.SSHTunnelManager')
    async def test_test_connection_postgresql(self, mock_tunnel_manager_class):
        """Test connection testing through SSH tunnel for PostgreSQL."""
        from sqlalchemy.engine.url import make_url
        
        # Setup mocks
        mock_tunnel_manager = MagicMock()
        mock_tunnel_manager.tunnel.return_value.__aenter__ = AsyncMock(return_value=12345)
        mock_tunnel_manager.tunnel.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_tunnel_manager_class.return_value = mock_tunnel_manager
        
        with patch('toolfront.models.connection.PostgreSQL') as mock_postgres:
            mock_db = MagicMock()
            mock_db.test_connection = AsyncMock(return_value=MagicMock(connected=True, message="Success"))
            mock_postgres.return_value = mock_db
            
            url = make_url("postgresql://user:pass@db.example.com:5432/mydb")
            ssh_config = SSHConfig(
                ssh_host="bastion.example.com",
                ssh_user="ubuntu",
                ssh_key_path="/path/to/key.pem"
            )
            
            db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
            result = await db.test_connection()
            
            assert result.connected
            assert result.message == "Success"
            
            # Verify PostgreSQL was created with tunnelled URL
            mock_postgres.assert_called_once()
            call_args = mock_postgres.call_args
            tunnelled_url = call_args[1]['url']
            assert tunnelled_url.host == "localhost"
            assert tunnelled_url.port == 12345

    @patch('toolfront.models.connection.SSHTunnelManager')
    async def test_test_connection_mysql(self, mock_tunnel_manager_class):
        """Test connection testing through SSH tunnel for MySQL."""
        from sqlalchemy.engine.url import make_url
        
        # Setup mocks
        mock_tunnel_manager = MagicMock()
        mock_tunnel_manager.tunnel.return_value.__aenter__ = AsyncMock(return_value=12345)
        mock_tunnel_manager.tunnel.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_tunnel_manager_class.return_value = mock_tunnel_manager
        
        with patch('toolfront.models.connection.MySQL') as mock_mysql:
            mock_db = MagicMock()
            mock_db.test_connection = AsyncMock(return_value=MagicMock(connected=True, message="Success"))
            mock_mysql.return_value = mock_db
            
            url = make_url("mysql://user:pass@db.example.com:3306/mydb")
            ssh_config = SSHConfig(
                ssh_host="bastion.example.com",
                ssh_user="ubuntu",
                ssh_key_path="/path/to/key.pem"
            )
            
            db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
            result = await db.test_connection()
            
            assert result.connected
            assert result.message == "Success"
            
            # Verify MySQL was created with tunnelled URL
            mock_mysql.assert_called_once()
            call_args = mock_mysql.call_args
            tunnelled_url = call_args[1]['url']
            assert tunnelled_url.host == "localhost"
            assert tunnelled_url.port == 12345

    @patch('toolfront.models.connection.SSHTunnelManager')
    async def test_connection_failure_handling(self, mock_tunnel_manager_class):
        """Test SSH tunnel connection failure handling."""
        from sqlalchemy.engine.url import make_url
        
        # Setup mocks to simulate tunnel failure
        mock_tunnel_manager = MagicMock()
        mock_tunnel_manager.tunnel.return_value.__aenter__ = AsyncMock(side_effect=Exception("SSH connection failed"))
        mock_tunnel_manager_class.return_value = mock_tunnel_manager
        
        url = make_url("postgresql://user:pass@db.example.com:5432/mydb")
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
        result = await db.test_connection()
        
        assert not result.connected
        assert "SSH tunnel connection failed" in result.message

    @patch('toolfront.models.connection.SSHTunnelManager')
    async def test_get_tables_through_tunnel(self, mock_tunnel_manager_class):
        """Test getting tables through SSH tunnel."""
        from sqlalchemy.engine.url import make_url
        
        # Setup mocks
        mock_tunnel_manager = MagicMock()
        mock_tunnel_manager.tunnel.return_value.__aenter__ = AsyncMock(return_value=12345)
        mock_tunnel_manager.tunnel.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_tunnel_manager_class.return_value = mock_tunnel_manager
        
        with patch('toolfront.models.connection.PostgreSQL') as mock_postgres:
            mock_db = MagicMock()
            mock_db.get_tables = AsyncMock(return_value=["table1", "table2"])
            mock_postgres.return_value = mock_db
            
            url = make_url("postgresql://user:pass@db.example.com:5432/mydb")
            ssh_config = SSHConfig(
                ssh_host="bastion.example.com",
                ssh_user="ubuntu",
                ssh_key_path="/path/to/key.pem"
            )
            
            db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
            tables = await db.get_tables()
            
            assert tables == ["table1", "table2"]
            mock_db.get_tables.assert_called_once()

    @patch('toolfront.models.connection.SSHTunnelManager')
    async def test_query_through_tunnel(self, mock_tunnel_manager_class):
        """Test executing queries through SSH tunnel."""
        from sqlalchemy.engine.url import make_url
        import pandas as pd
        
        # Setup mocks
        mock_tunnel_manager = MagicMock()
        mock_tunnel_manager.tunnel.return_value.__aenter__ = AsyncMock(return_value=12345)
        mock_tunnel_manager.tunnel.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_tunnel_manager_class.return_value = mock_tunnel_manager
        
        with patch('toolfront.models.connection.PostgreSQL') as mock_postgres:
            mock_db = MagicMock()
            expected_result = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
            mock_db.query = AsyncMock(return_value=expected_result)
            mock_postgres.return_value = mock_db
            
            url = make_url("postgresql://user:pass@db.example.com:5432/mydb")
            ssh_config = SSHConfig(
                ssh_host="bastion.example.com",
                ssh_user="ubuntu",
                ssh_key_path="/path/to/key.pem"
            )
            
            db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
            result = await db.query("SELECT * FROM test_table")
            
            pd.testing.assert_frame_equal(result, expected_result)
            mock_db.query.assert_called_once_with("SELECT * FROM test_table")

    async def test_unsupported_database_type(self):
        """Test error with unsupported database type for SSH tunnels."""
        from sqlalchemy.engine.url import make_url
        
        url = make_url("sqlite:///test.db")
        ssh_config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        db = SSHTunnelledDatabase(url=url, ssh_config=ssh_config)
        
        with pytest.raises(ValueError, match="SSH tunnels not supported for sqlite"):
            await db.test_connection()
        
        with pytest.raises(ValueError, match="SSH tunnels not supported for sqlite"):
            await db.get_tables()
        
        with pytest.raises(ValueError, match="SSH tunnels not supported for sqlite"):
            await db.query("SELECT 1")