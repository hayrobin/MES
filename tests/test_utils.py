"""Tests for utility modules."""

import pytest
from src.utils.exceptions import (
    MESException,
    OPCUAException,
    ModbusException,
    ConfigurationError
)
from src.utils.logger import setup_logger, get_logger


def test_exception_hierarchy():
    """Test exception hierarchy."""
    # Base exception
    with pytest.raises(MESException):
        raise MESException("Test error")
    
    # OPC UA exception
    with pytest.raises(OPCUAException):
        raise OPCUAException("OPC UA error")
    
    # Modbus exception
    with pytest.raises(ModbusException):
        raise ModbusException("Modbus error")
    
    # Configuration error
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("Config error")


def test_logger_setup():
    """Test logger setup."""
    # Setup logger
    logger = setup_logger("test", "INFO", json_format=False)
    assert logger is not None
    assert logger.name == "test"
    
    # Get logger
    logger2 = get_logger("test")
    assert logger2.name == "test"


def test_logger_json_format():
    """Test JSON logger format."""
    logger = setup_logger("test_json", "INFO", json_format=True)
    assert logger is not None
    assert len(logger.handlers) > 0
