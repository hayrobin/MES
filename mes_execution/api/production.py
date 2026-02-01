"""
Production API Endpoints
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.production_service import ProductionService
from ..schemas.production import (
    ProductionLogCreate,
    ProductionLogResponse,
    ProductionSummary,
)

router = APIRouter(prefix="/api/v1/execution/production", tags=["production"])


@router.post("/log", response_model=ProductionLogResponse, status_code=201)
def log_production(
    production_data: ProductionLogCreate,
    db: Session = Depends(get_db)
):
    """
    Log production data (produced/scrap quantities)
    """
    service = ProductionService(db)
    return service.log_production(production_data)


@router.get("/summary", response_model=ProductionSummary)
def get_production_summary(
    work_order_id: int = Query(..., description="Work order ID"),
    db: Session = Depends(get_db)
):
    """
    Get production summary for a work order
    """
    service = ProductionService(db)
    
    try:
        summary = service.get_production_summary(work_order_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/logs", response_model=List[ProductionLogResponse])
def get_production_logs(
    work_order_id: Optional[int] = Query(None, description="Filter by work order ID"),
    equipment_id: Optional[int] = Query(None, description="Filter by equipment ID"),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get production logs with filters
    """
    service = ProductionService(db)
    return service.get_production_logs(
        work_order_id=work_order_id,
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )
