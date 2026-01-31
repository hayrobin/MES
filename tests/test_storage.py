"""Tests for database storage layer."""

import pytest
from datetime import datetime, timedelta
from src.data.storage import DatabaseStorage
from src.data.models import Base
from src.config.settings import DatabaseConfig


@pytest.fixture
async def storage():
    """Create test database storage."""
    config = DatabaseConfig(type="sqlite", database=":memory:")
    storage = DatabaseStorage(config)
    await storage.initialize()
    yield storage
    await storage.close()


@pytest.mark.asyncio
async def test_create_device(storage):
    """Test device creation."""
    device = await storage.create_device(
        name="TestDevice",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    
    assert device.id is not None
    assert device.name == "TestDevice"
    assert device.device_type == "modbus"
    assert device.status == "disconnected"


@pytest.mark.asyncio
async def test_get_device(storage):
    """Test getting device."""
    # Create device
    device = await storage.create_device(
        name="TestDevice",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    
    # Get by ID
    retrieved = await storage.get_device(device.id)
    assert retrieved is not None
    assert retrieved.id == device.id
    assert retrieved.name == "TestDevice"
    
    # Get by name
    retrieved = await storage.get_device_by_name("TestDevice")
    assert retrieved is not None
    assert retrieved.name == "TestDevice"


@pytest.mark.asyncio
async def test_update_device_status(storage):
    """Test updating device status."""
    # Create device
    device = await storage.create_device(
        name="TestDevice",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    
    # Update status
    await storage.update_device_status(device.id, "connected")
    
    # Verify
    updated = await storage.get_device(device.id)
    assert updated.status == "connected"
    assert updated.last_seen is not None


@pytest.mark.asyncio
async def test_realtime_data(storage):
    """Test real-time data operations."""
    # Create device
    device = await storage.create_device(
        name="TestDevice",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    
    # Update real-time data
    await storage.update_realtime_data(
        device_id=device.id,
        data_point_name="Temperature",
        value=25.5,
        quality="good"
    )
    
    # Get real-time data
    data = await storage.get_realtime_data(device_id=device.id)
    assert len(data) == 1
    assert data[0].data_point_name == "Temperature"
    assert data[0].value == "25.5"
    assert data[0].quality == "good"


@pytest.mark.asyncio
async def test_historical_data(storage):
    """Test historical data operations."""
    # Create device
    device = await storage.create_device(
        name="TestDevice",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    
    # Insert historical data
    now = datetime.utcnow()
    await storage.insert_historical_data(
        device_id=device.id,
        data_point_name="Temperature",
        value=25.5,
        timestamp=now
    )
    
    # Query historical data
    start_time = now - timedelta(hours=1)
    end_time = now + timedelta(hours=1)
    
    data = await storage.get_historical_data(
        device_id=device.id,
        data_point_name="Temperature",
        start_time=start_time,
        end_time=end_time
    )
    
    assert len(data) == 1
    assert data[0].value == "25.5"
