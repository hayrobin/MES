"""Configuration file loader."""

import yaml
from pathlib import Path
from typing import List, Dict, Any
from .settings import (
    OPCUAServerConfig,
    OPCUAClientConfig,
    ModbusDeviceConfig,
    MESSettings
)
from ..utils.exceptions import ConfigurationError
from ..utils.logger import get_logger

logger = get_logger(__name__)


def load_yaml(file_path: str) -> Dict[str, Any]:
    """Load YAML configuration file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML data
        
    Raises:
        ConfigurationError: If file cannot be loaded
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"Configuration file not found: {file_path}")
            return {}
            
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data or {}
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration from {file_path}: {str(e)}")


def load_opcua_server_config(file_path: str) -> OPCUAServerConfig:
    """Load OPC UA server configuration.
    
    Args:
        file_path: Path to configuration file
        
    Returns:
        OPC UA server configuration
    """
    data = load_yaml(file_path)
    return OPCUAServerConfig(**data)


def load_opcua_clients_config(file_path: str) -> List[OPCUAClientConfig]:
    """Load OPC UA clients configuration.
    
    Args:
        file_path: Path to configuration file
        
    Returns:
        List of OPC UA client configurations
    """
    data = load_yaml(file_path)
    clients = data.get('clients', [])
    return [OPCUAClientConfig(**client) for client in clients]


def load_modbus_devices_config(file_path: str) -> List[ModbusDeviceConfig]:
    """Load Modbus devices configuration.
    
    Args:
        file_path: Path to configuration file
        
    Returns:
        List of Modbus device configurations
    """
    data = load_yaml(file_path)
    devices = data.get('devices', [])
    return [ModbusDeviceConfig(**device) for device in devices]


def load_mes_settings() -> MESSettings:
    """Load MES settings from environment and config files.
    
    Returns:
        MES settings
    """
    return MESSettings()
