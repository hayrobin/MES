"""
Material Consumption API Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.material_consumption import MaterialConsumption
from ..schemas.material import (
    MaterialConsumptionCreate,
    MaterialConsumptionResponse,
)

router = APIRouter(prefix="/api/v1/execution/materials", tags=["materials"])


@router.post("/consume", response_model=MaterialConsumptionResponse, status_code=201)
def record_material_consumption(
    consumption_data: MaterialConsumptionCreate,
    db: Session = Depends(get_db)
):
    """
    Record material consumption with batch/heat tracking
    """
    consumption = MaterialConsumption(
        work_order_id=consumption_data.work_order_id,
        operation_execution_id=consumption_data.operation_execution_id,
        material_id=consumption_data.material_id,
        planned_quantity=consumption_data.planned_quantity,
        actual_quantity=consumption_data.actual_quantity,
        uom=consumption_data.uom,
        batch_number=consumption_data.batch_number,
        heat_number=consumption_data.heat_number,
        lot_number=consumption_data.lot_number,
        serial_number=consumption_data.serial_number,
        entered_by=consumption_data.entered_by,
    )
    
    db.add(consumption)
    db.commit()
    db.refresh(consumption)
    
    return consumption


@router.get("/consumption", response_model=List[MaterialConsumptionResponse])
def get_material_consumption(
    work_order_id: int = Query(..., description="Work order ID"),
    db: Session = Depends(get_db)
):
    """
    Get material consumption history for a work order
    """
    consumptions = db.query(MaterialConsumption).filter(
        MaterialConsumption.work_order_id == work_order_id
    ).order_by(MaterialConsumption.consumption_time.desc()).all()
    
    return consumptions
