"""Tests for configuration management."""

import pytest
from pathlib import Path
from src.config.settings import (
    OPCUANodeConfig,
    OPCUAServerConfig,
    OPCUAClientConfig,
    ModbusDeviceConfig,
    MESSettings
)


def test_opcua_node_config():
    """Test OPC UA node configuration."""
    node = OPCUANodeConfig(
        node_id="Temperature1",
        browse_name="Temperature1",
        display_name="Zone 1 Temperature",
        data_type="float",
        initial_value=25.0,
        writable=False
    )
    
    assert node.node_id == "Temperature1"
    assert node.data_type == "float"
    assert node.initial_value == 25.0
    assert node.writable is False


def test_opcua_server_config():
    """Test OPC UA server configuration."""
    config = OPCUAServerConfig(
        endpoint="opc.tcp://localhost:4840",
        server_name="Test Server",
        namespace="http://test.com",
        nodes=[]
    )
    
    assert config.endpoint == "opc.tcp://localhost:4840"
    assert config.server_name == "Test Server"
    assert len(config.nodes) == 0


def test_modbus_device_config():
    """Test Modbus device configuration."""
    config = ModbusDeviceConfig(
        name="TestDevice",
        host="192.168.1.50",
        port=502,
        unit_id=1,
        registers=[]
    )
    
    assert config.name == "TestDevice"
    assert config.host == "192.168.1.50"
    assert config.port == 502
    assert config.unit_id == 1


def test_mes_settings_defaults():
    """Test MES settings defaults."""
    settings = MESSettings()
    
    assert settings.app_name == "Factory MES"
    assert settings.log_level == "INFO"
    assert settings.database.type == "sqlite"
