"""OPC UA routes."""

from typing import List
from fastapi import APIRouter, HTTPException
from ...api.schemas import (
    OPCUABrowseRequest, OPCUANodeInfo,
    OPCUAReadRequest, OPCUAWriteRequest
)
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/opcua", tags=["opcua"])


@router.post("/browse", response_model=List[OPCUANodeInfo])
async def browse_opcua_nodes(request: OPCUABrowseRequest):
    """Browse OPC UA address space."""
    try:
        from ...api.main import app_state
        
        # Find client by name
        client = None
        for c in app_state.opcua_clients:
            if c.config.name == request.client_name:
                client = c
                break
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {request.client_name} not found")
        
        # Browse nodes
        nodes = await client.browse(request.node_id)
        return nodes
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error browsing OPC UA nodes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/read")
async def read_opcua_node(request: OPCUAReadRequest):
    """Read OPC UA node value."""
    try:
        from ...api.main import app_state
        
        # Find client by name
        client = None
        for c in app_state.opcua_clients:
            if c.config.name == request.client_name:
                client = c
                break
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {request.client_name} not found")
        
        # Read value
        value = await client.read_node(request.node_id)
        return {"node_id": request.node_id, "value": value}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading OPC UA node: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write")
async def write_opcua_node(request: OPCUAWriteRequest):
    """Write OPC UA node value."""
    try:
        from ...api.main import app_state
        
        # Find client by name
        client = None
        for c in app_state.opcua_clients:
            if c.config.name == request.client_name:
                client = c
                break
        
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {request.client_name} not found")
        
        # Write value
        await client.write_node(request.node_id, request.value)
        return {"status": "success", "node_id": request.node_id, "value": request.value}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error writing OPC UA node: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
