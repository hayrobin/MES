#!/usr/bin/env python3
"""Storage demo - demonstrates programmatic use of MES."""
import asyncio
from datetime import datetime, timedelta
from src.data.storage import DatabaseStorage
from src.config.settings import DatabaseConfig

async def main():
    print("Factory MES Storage Demo")
    config = DatabaseConfig(type="sqlite", database=":memory:")
    storage = DatabaseStorage(config)
    await storage.initialize()
    
    # Create device
    device = await storage.create_device(
        name="Demo Sensor",
        device_type="modbus",
        connection_string="192.168.1.50:502"
    )
    print(f"Created device: {device.name}")
    
    # Add data
    await storage.update_realtime_data(
        device_id=device.id,
        data_point_name="Temperature",
        value=25.5
    )
    print("Added temperature data")
    
    # Query data
    data = await storage.get_realtime_data(device_id=device.id)
    for d in data:
        print(f"  {d.data_point_name}: {d.value}")
    
    await storage.close()
    print("Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())
