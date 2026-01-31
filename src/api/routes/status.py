"""Status and health check routes."""

from fastapi import APIRouter
from datetime import datetime
from ...api.schemas import SystemStatus, DeviceStatus
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/status", tags=["status"])

# Track startup time
startup_time = datetime.utcnow()


@router.get("/", response_model=SystemStatus)
async def get_system_status():
    """Get system health and status."""
    try:
        from ...api.main import app_state
        
        # Calculate uptime
        uptime = (datetime.utcnow() - startup_time).total_seconds()
        
        # Get device statuses
        devices = []
        
        # OPC UA clients
        for client in app_state.opcua_clients:
            devices.append(DeviceStatus(
                name=client.config.name,
                type="opcua_client",
                status="connected" if client.connected else "disconnected",
                last_seen=datetime.utcnow() if client.connected else None
            ))
        
        # Modbus drivers
        for driver in app_state.modbus_drivers:
            devices.append(DeviceStatus(
                name=driver.config.name,
                type="modbus",
                status="connected" if driver.client.connected else "disconnected",
                last_seen=datetime.utcnow() if driver.client.connected else None
            ))
        
        # Check database
        db_connected = app_state.storage is not None and app_state.storage.engine is not None
        
        return SystemStatus(
            status="running",
            uptime=uptime,
            devices=devices,
            database_connected=db_connected
        )
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        return SystemStatus(
            status="error",
            uptime=0,
            devices=[],
            database_connected=False
        )


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}
