"""Main FastAPI application for the MES system."""

import asyncio
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config.loader import (
    load_mes_settings,
    load_opcua_server_config,
    load_opcua_clients_config,
    load_modbus_devices_config
)
from ..config.settings import MESSettings
from ..data.storage import DatabaseStorage
from ..data.acquisition import DataAcquisitionManager, DataPoint
from ..opcua.server import OPCUAServer
from ..opcua.client import OPCUAClient
from ..modbus.driver import ModbusDriver
from ..utils.logger import setup_logger, get_logger

# Import routes
from .routes import devices, data, opcua, modbus, status

# Global application state
class AppState:
    """Application state container."""
    
    def __init__(self):
        self.settings: MESSettings = None
        self.storage: DatabaseStorage = None
        self.data_manager: DataAcquisitionManager = None
        self.opcua_server: OPCUAServer = None
        self.opcua_clients: List[OPCUAClient] = []
        self.modbus_drivers: List[ModbusDriver] = []
        self.background_tasks: List[asyncio.Task] = []

app_state = AppState()


async def data_update_callback(data_point: DataPoint) -> None:
    """Callback for data updates from protocol drivers.
    
    Args:
        data_point: Updated data point
    """
    try:
        # Get device by name
        device = await app_state.storage.get_device_by_name(data_point.device_name)
        if not device:
            logger.warning(f"Device not found: {data_point.device_name}")
            return
        
        # Update real-time data
        await app_state.storage.update_realtime_data(
            device_id=device.id,
            data_point_name=data_point.point_name,
            value=data_point.value,
            quality=data_point.quality,
            timestamp=data_point.timestamp
        )
        
        # Insert historical data
        await app_state.storage.insert_historical_data(
            device_id=device.id,
            data_point_name=data_point.point_name,
            value=data_point.value,
            quality=data_point.quality,
            timestamp=data_point.timestamp
        )
        
    except Exception as e:
        logger.error(f"Error processing data update: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.
    
    Args:
        app: FastAPI application
    """
    # Startup
    logger.info("Starting Factory MES System...")
    
    # Load settings
    app_state.settings = load_mes_settings()
    
    # Initialize database
    app_state.storage = DatabaseStorage(app_state.settings.database)
    await app_state.storage.initialize()
    
    # Initialize data acquisition manager
    app_state.data_manager = DataAcquisitionManager()
    app_state.data_manager.register_callback(data_update_callback)
    await app_state.data_manager.start()
    
    # Start OPC UA server (if configured)
    try:
        opcua_server_config = load_opcua_server_config(app_state.settings.opcua_server_config)
        if opcua_server_config and opcua_server_config.nodes:
            app_state.opcua_server = OPCUAServer(opcua_server_config)
            server_task = asyncio.create_task(app_state.opcua_server.start())
            app_state.background_tasks.append(server_task)
            logger.info("OPC UA server task started")
    except Exception as e:
        logger.warning(f"OPC UA server not started: {str(e)}")
    
    # Start OPC UA clients (if configured)
    try:
        opcua_clients_configs = load_opcua_clients_config(app_state.settings.opcua_clients_config)
        for client_config in opcua_clients_configs:
            client = OPCUAClient(client_config, data_update_callback)
            app_state.opcua_clients.append(client)
            
            # Create device entry in database
            await app_state.storage.create_device(
                name=client_config.name,
                device_type="opcua_client",
                connection_string=client_config.endpoint,
                config=client_config.dict()
            )
            
            # Start client
            client_task = asyncio.create_task(client.run())
            app_state.background_tasks.append(client_task)
            logger.info(f"OPC UA client {client_config.name} started")
    except Exception as e:
        logger.warning(f"OPC UA clients not started: {str(e)}")
    
    # Start Modbus drivers (if configured)
    try:
        modbus_devices_configs = load_modbus_devices_config(app_state.settings.modbus_devices_config)
        for device_config in modbus_devices_configs:
            driver = ModbusDriver(device_config, data_update_callback)
            app_state.modbus_drivers.append(driver)
            
            # Create device entry in database
            await app_state.storage.create_device(
                name=device_config.name,
                device_type="modbus",
                connection_string=f"{device_config.host}:{device_config.port}",
                config=device_config.dict()
            )
            
            # Start driver
            await driver.start()
            logger.info(f"Modbus driver {device_config.name} started")
    except Exception as e:
        logger.warning(f"Modbus drivers not started: {str(e)}")
    
    logger.info("Factory MES System started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Factory MES System...")
    
    # Stop OPC UA server
    if app_state.opcua_server:
        await app_state.opcua_server.stop()
    
    # Stop OPC UA clients
    for client in app_state.opcua_clients:
        await client.stop()
    
    # Stop Modbus drivers
    for driver in app_state.modbus_drivers:
        await driver.stop()
    
    # Stop data manager
    await app_state.data_manager.stop()
    
    # Cancel background tasks
    for task in app_state.background_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    # Close database
    await app_state.storage.close()
    
    logger.info("Factory MES System shut down")


# Initialize logger
logger = setup_logger("mes", "INFO", json_format=False)

# Create FastAPI app
app = FastAPI(
    title="Factory MES System",
    description="Manufacturing Execution System with OPC UA and Modbus TCP/IP support",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(devices.router)
app.include_router(data.router)
app.include_router(opcua.router)
app.include_router(modbus.router)
app.include_router(status.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Factory MES System",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
