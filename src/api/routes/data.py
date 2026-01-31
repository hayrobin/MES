"""Data query routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ...api.schemas import RealtimeDataResponse, HistoricalDataQuery, HistoricalDataResponse
from ...data.storage import DatabaseStorage
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/data", tags=["data"])


def get_storage() -> DatabaseStorage:
    """Dependency to get database storage."""
    from ...api.main import app_state
    return app_state.storage


@router.get("/realtime", response_model=List[RealtimeDataResponse])
async def get_realtime_data(device_id: int = None, storage: DatabaseStorage = Depends(get_storage)):
    """Get real-time data values."""
    try:
        data = await storage.get_realtime_data(device_id)
        return data
    except Exception as e:
        logger.error(f"Error getting realtime data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history", response_model=List[HistoricalDataResponse])
async def get_historical_data(query: HistoricalDataQuery, storage: DatabaseStorage = Depends(get_storage)):
    """Query historical data."""
    try:
        data = await storage.get_historical_data(
            device_id=query.device_id,
            data_point_name=query.data_point_name,
            start_time=query.start_time,
            end_time=query.end_time
        )
        return data
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
