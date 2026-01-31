"""Modbus routes."""

from fastapi import APIRouter, HTTPException
from ...api.schemas import ModbusReadRequest, ModbusWriteRequest
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/modbus", tags=["modbus"])


@router.post("/read")
async def read_modbus_register(request: ModbusReadRequest):
    """Read Modbus register value."""
    try:
        from ...api.main import app_state
        
        # Find driver by device name
        driver = None
        for d in app_state.modbus_drivers:
            if d.config.name == request.device_name:
                driver = d
                break
        
        if not driver:
            raise HTTPException(status_code=404, detail=f"Device {request.device_name} not found")
        
        # Find register config
        register_config = None
        for reg in driver.config.registers:
            if reg.name == request.register_name:
                register_config = reg
                break
        
        if not register_config:
            raise HTTPException(status_code=404, detail=f"Register {request.register_name} not found")
        
        # Read value
        value = await driver._read_register(register_config)
        return {"device": request.device_name, "register": request.register_name, "value": value}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading Modbus register: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write")
async def write_modbus_register(request: ModbusWriteRequest):
    """Write Modbus register value."""
    try:
        from ...api.main import app_state
        
        # Find driver by device name
        driver = None
        for d in app_state.modbus_drivers:
            if d.config.name == request.device_name:
                driver = d
                break
        
        if not driver:
            raise HTTPException(status_code=404, detail=f"Device {request.device_name} not found")
        
        # Write value
        await driver.write_register(request.register_name, request.value)
        return {"status": "success", "device": request.device_name, "register": request.register_name, "value": request.value}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error writing Modbus register: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
