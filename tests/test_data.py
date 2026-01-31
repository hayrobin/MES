"""Tests for data acquisition layer."""

import pytest
from datetime import datetime
from src.data.acquisition import DataPoint, DataAcquisitionManager


def test_data_point_creation():
    """Test data point creation."""
    data_point = DataPoint(
        device_name="TestDevice",
        point_name="Temperature",
        value=25.5,
        quality="good"
    )
    
    assert data_point.device_name == "TestDevice"
    assert data_point.point_name == "Temperature"
    assert data_point.value == 25.5
    assert data_point.quality == "good"
    assert isinstance(data_point.timestamp, datetime)


def test_data_point_with_timestamp():
    """Test data point with explicit timestamp."""
    ts = datetime.now()
    data_point = DataPoint(
        device_name="TestDevice",
        point_name="Temperature",
        value=25.5,
        timestamp=ts
    )
    
    assert data_point.timestamp == ts


@pytest.mark.asyncio
async def test_data_acquisition_manager():
    """Test data acquisition manager."""
    manager = DataAcquisitionManager()
    
    # Test callback registration
    callback_called = False
    
    def test_callback(data_point: DataPoint):
        nonlocal callback_called
        callback_called = True
    
    manager.register_callback(test_callback)
    
    # Test data publishing
    data_point = DataPoint(
        device_name="TestDevice",
        point_name="Temperature",
        value=25.5
    )
    
    await manager.publish_data(data_point)
    assert callback_called


def test_data_validation():
    """Test data validation."""
    manager = DataAcquisitionManager()
    
    # Test float conversion
    is_valid, value = manager.validate_data("25.5", "float")
    assert is_valid
    assert value == 25.5
    
    # Test int conversion
    is_valid, value = manager.validate_data("10", "int")
    assert is_valid
    assert value == 10
    
    # Test bool conversion
    is_valid, value = manager.validate_data(True, "bool")
    assert is_valid
    assert value is True


def test_data_normalization():
    """Test data normalization."""
    manager = DataAcquisitionManager()
    
    # Test scale and offset
    value = manager.normalize_data(100, scale=0.1, offset=5.0)
    assert value == 15.0  # (100 * 0.1) + 5.0
    
    # Test with no scale/offset
    value = manager.normalize_data(100)
    assert value == 100.0
