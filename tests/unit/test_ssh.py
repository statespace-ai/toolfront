"""Unit tests for SSH tunnel functionality."""

import pytest
from unittest.mock import patch, MagicMock

from toolfront.ssh import (
    SSHConfig,
    SSHTunnelManager,
    parse_ssh_params,
    extract_ssh_params,
)


class TestSSHConfig:
    """Test SSH configuration parsing and validation."""

    def test_ssh_config_creation(self):
        """Test basic SSH config creation."""
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem",
            remote_host="db.internal.com",
            remote_port=5432
        )
        
        assert config.ssh_host == "bastion.example.com"
        assert config.ssh_port == 22  # default
        assert config.ssh_user == "ubuntu"
        assert config.ssh_key_path == "/path/to/key.pem"
        assert config.remote_host == "db.internal.com"
        assert config.remote_port == 5432

    def test_ssh_config_defaults(self):
        """Test SSH config with default values."""
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        assert config.ssh_port == 22
        assert config.remote_host == "localhost"
        assert config.remote_port == 5432


class TestSSHParamParsing:
    """Test SSH parameter parsing from URLs."""

    def test_parse_ssh_params_with_key(self):
        """Test parsing SSH parameters with key authentication."""
        params = {
            "ssh_host": "bastion.example.com",
            "ssh_user": "ubuntu",
            "ssh_key_path": "/path/to/key.pem",
            "ssh_port": "2222"
        }
        
        config = parse_ssh_params(params)
        
        assert config is not None
        assert config.ssh_host == "bastion.example.com"
        assert config.ssh_port == 2222
        assert config.ssh_user == "ubuntu"
        assert config.ssh_key_path == "/path/to/key.pem"
        assert config.ssh_password is None

    def test_parse_ssh_params_with_password(self):
        """Test parsing SSH parameters with password authentication."""
        params = {
            "ssh_host": "bastion.example.com",
            "ssh_user": "ubuntu",
            "ssh_password": "secret123"
        }
        
        config = parse_ssh_params(params)
        
        assert config is not None
        assert config.ssh_host == "bastion.example.com"
        assert config.ssh_user == "ubuntu"
        assert config.ssh_password == "secret123"
        assert config.ssh_key_path is None

    def test_parse_ssh_params_no_ssh_host(self):
        """Test that None is returned when no ssh_host is provided."""
        params = {"ssh_user": "ubuntu", "ssh_key_path": "/path/to/key.pem"}
        
        config = parse_ssh_params(params)
        
        assert config is None

    def test_parse_ssh_params_missing_user(self):
        """Test error when ssh_user is missing."""
        params = {"ssh_host": "bastion.example.com", "ssh_key_path": "/path/to/key.pem"}
        
        with pytest.raises(ValueError, match="ssh_user is required"):
            parse_ssh_params(params)

    def test_parse_ssh_params_missing_auth(self):
        """Test error when both password and key are missing."""
        params = {"ssh_host": "bastion.example.com", "ssh_user": "ubuntu"}
        
        with pytest.raises(ValueError, match="Either ssh_password or ssh_key_path is required"):
            parse_ssh_params(params)


class TestSSHUrlExtraction:
    """Test SSH parameter extraction from database URLs."""

    def test_extract_ssh_params_postgresql(self):
        """Test SSH parameter extraction from PostgreSQL URL."""
        url = (
            "postgresql://user:pass@db.example.com:5432/mydb"
            "?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/path/to/key.pem"
        )
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config is not None
        assert clean_url == "postgresql://user:pass@db.example.com:5432/mydb"
        assert ssh_config.ssh_host == "bastion.example.com"
        assert ssh_config.ssh_user == "ubuntu"
        assert ssh_config.ssh_key_path == "/path/to/key.pem"
        assert ssh_config.remote_host == "db.example.com"
        assert ssh_config.remote_port == 5432

    def test_extract_ssh_params_mysql(self):
        """Test SSH parameter extraction from MySQL URL."""
        url = (
            "mysql://user:pass@db.example.com:3306/mydb"
            "?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_password=secret"
        )
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config is not None
        assert clean_url == "mysql://user:pass@db.example.com:3306/mydb"
        assert ssh_config.remote_host == "db.example.com"
        assert ssh_config.remote_port == 3306

    def test_extract_ssh_params_mixed_params(self):
        """Test SSH extraction with mixed parameters."""
        url = (
            "postgresql://user:pass@db.example.com:5432/mydb"
            "?sslmode=require&ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/key.pem&timeout=30"
        )
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config is not None
        assert "sslmode=require" in clean_url
        assert "timeout=30" in clean_url
        assert "ssh_host" not in clean_url
        assert "ssh_user" not in clean_url
        assert "ssh_key_path" not in clean_url

    def test_extract_ssh_params_no_ssh(self):
        """Test URL without SSH parameters."""
        url = "postgresql://user:pass@db.example.com:5432/mydb?sslmode=require"
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config is None
        assert clean_url == url

    def test_extract_ssh_params_default_ports(self):
        """Test SSH extraction with default database ports."""
        # Test PostgreSQL default port
        url = (
            "postgresql://user:pass@db.example.com/mydb"
            "?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/key.pem"
        )
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config.remote_port == 5432  # PostgreSQL default
        
        # Test MySQL default port
        url = (
            "mysql://user:pass@db.example.com/mydb"
            "?ssh_host=bastion.example.com&ssh_user=ubuntu&ssh_key_path=/key.pem"
        )
        
        clean_url, ssh_config = extract_ssh_params(url)
        
        assert ssh_config.remote_port == 3306  # MySQL default


class TestSSHTunnelManager:
    """Test SSH tunnel manager functionality."""

    def test_tunnel_manager_creation(self):
        """Test SSH tunnel manager creation."""
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        manager = SSHTunnelManager(config)
        
        assert manager.config == config
        assert manager.tunnel is None
        assert manager.local_port is None

    def test_is_active_false_initially(self):
        """Test that tunnel is not active initially."""
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        manager = SSHTunnelManager(config)
        
        assert not manager.is_active()

    @patch('toolfront.ssh.socket.socket')
    def test_find_free_port(self, mock_socket):
        """Test finding a free port."""
        mock_sock = MagicMock()
        mock_sock.getsockname.return_value = ("localhost", 12345)
        mock_socket.return_value.__enter__.return_value = mock_sock
        
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem"
        )
        
        manager = SSHTunnelManager(config)
        port = manager._find_free_port()
        
        assert port == 12345

    @patch('toolfront.ssh.Path')
    def test_get_ssh_key_path_expansion(self, mock_path):
        """Test SSH key path expansion."""
        mock_path_obj = MagicMock()
        mock_path_obj.expanduser.return_value = mock_path_obj
        mock_path_obj.exists.return_value = True
        mock_path_obj.__str__ = lambda x: "/home/user/.ssh/id_rsa"
        mock_path.return_value = mock_path_obj
        
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="~/.ssh/id_rsa"
        )
        
        manager = SSHTunnelManager(config)
        key_path = manager._get_ssh_key_path()
        
        assert key_path == "/home/user/.ssh/id_rsa"

    @patch('toolfront.ssh.Path')
    def test_get_ssh_key_path_not_found(self, mock_path):
        """Test error when SSH key file doesn't exist."""
        mock_path_obj = MagicMock()
        mock_path_obj.expanduser.return_value = mock_path_obj
        mock_path_obj.exists.return_value = False
        mock_path.return_value = mock_path_obj
        
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/nonexistent/key.pem"
        )
        
        manager = SSHTunnelManager(config)
        
        with pytest.raises(FileNotFoundError):
            manager._get_ssh_key_path()

    @patch('toolfront.ssh.SSHTunnelForwarder')
    @patch('toolfront.ssh.Path')
    async def test_tunnel_context_manager(self, mock_path, mock_tunnel_forwarder):
        """Test tunnel context manager lifecycle."""
        # Mock path handling
        mock_path_obj = MagicMock()
        mock_path_obj.expanduser.return_value = mock_path_obj
        mock_path_obj.exists.return_value = True
        mock_path_obj.__str__ = lambda x: "/path/to/key.pem"
        mock_path.return_value = mock_path_obj
        
        # Mock tunnel forwarder
        mock_tunnel = MagicMock()
        mock_tunnel.local_bind_port = 12345
        mock_tunnel_forwarder.return_value = mock_tunnel
        
        config = SSHConfig(
            ssh_host="bastion.example.com",
            ssh_user="ubuntu",
            ssh_key_path="/path/to/key.pem",
            local_port=54321  # Use specific port
        )
        
        manager = SSHTunnelManager(config)
        
        async with manager.tunnel() as local_port:
            assert local_port == 12345
            mock_tunnel.start.assert_called_once()
        
        mock_tunnel.stop.assert_called_once()