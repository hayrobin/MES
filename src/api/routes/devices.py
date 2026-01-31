"""Device management routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ...api.schemas import DeviceCreate, DeviceResponse
from ...data.storage import DatabaseStorage
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/devices", tags=["devices"])


def get_storage() -> DatabaseStorage:
    """Dependency to get database storage."""
    from ...api.main import app_state
    return app_state.storage


@router.get("/", response_model=List[DeviceResponse])
async def list_devices(storage: DatabaseStorage = Depends(get_storage)):
    """List all devices."""
    try:
        devices = await storage.get_all_devices()
        return devices
    except Exception as e:
        logger.error(f"Error listing devices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=DeviceResponse)
async def create_device(device: DeviceCreate, storage: DatabaseStorage = Depends(get_storage)):
    """Create a new device."""
    try:
        new_device = await storage.create_device(
            name=device.name,
            device_type=device.device_type,
            connection_string=device.connection_string,
            config=device.config
        )
        return new_device
    except Exception as e:
        logger.error(f"Error creating device: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, storage: DatabaseStorage = Depends(get_storage)):
    """Get device by ID."""
    try:
        device = await storage.get_device(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting device: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
