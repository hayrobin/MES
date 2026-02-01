"""
Work Orders API Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..services.work_order_service import WorkOrderService
from ..schemas.work_order import (
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderResponse,
    WorkOrderWithOperations,
)

router = APIRouter(prefix="/api/v1/execution/work-orders", tags=["work-orders"])


@router.get("/", response_model=List[WorkOrderResponse])
def list_work_orders(
    status: Optional[str] = Query(None, description="Filter by status"),
    line_id: Optional[int] = Query(None, description="Filter by line ID"),
    equipment_id: Optional[int] = Query(None, description="Filter by equipment ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List work orders with optional filters
    """
    service = WorkOrderService(db)
    work_orders = service.list_work_orders(
        status=status,
        line_id=line_id,
        equipment_id=equipment_id,
        skip=skip,
        limit=limit
    )
    return work_orders


@router.get("/{work_order_id}", response_model=WorkOrderWithOperations)
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get work order details with operations
    """
    service = WorkOrderService(db)
    work_order = service.get_work_order(work_order_id)
    
    if not work_order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    return work_order


@router.post("/", response_model=WorkOrderResponse, status_code=201)
def create_work_order(
    work_order: WorkOrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new work order
    """
    service = WorkOrderService(db)
    
    # Check if work order number already exists
    existing = service.get_work_order_by_no(work_order.work_order_no)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Work order {work_order.work_order_no} already exists"
        )
    
    return service.create_work_order(work_order)


class WorkOrderStartRequest(BaseModel):
    """Schema for starting a work order"""
    operator_name: Optional[str] = None


@router.post("/{work_order_id}/start", response_model=WorkOrderResponse)
def start_work_order(
    work_order_id: int,
    request: Optional[WorkOrderStartRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Start a work order
    """
    service = WorkOrderService(db)
    operator_name = request.operator_name if request else None
    
    try:
        return service.start_work_order(work_order_id, operator_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{work_order_id}/pause", response_model=WorkOrderResponse)
def pause_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    """
    Pause a work order
    """
    service = WorkOrderService(db)
    
    try:
        return service.pause_work_order(work_order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{work_order_id}/complete", response_model=WorkOrderResponse)
def complete_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    """
    Complete a work order
    """
    service = WorkOrderService(db)
    
    try:
        return service.complete_work_order(work_order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{work_order_id}", response_model=WorkOrderResponse)
def update_work_order(
    work_order_id: int,
    update_data: WorkOrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update work order details
    """
    service = WorkOrderService(db)
    
    try:
        return service.update_work_order(work_order_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
