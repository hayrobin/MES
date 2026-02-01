"""
Equipment Status API Endpoints
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from pydantic import BaseModel
from decimal import Decimal

from ..database import get_db
from ..models.equipment_state import EquipmentState

router = APIRouter(prefix="/api/v1/execution/equipment", tags=["equipment"])


class EquipmentStateCreate(BaseModel):
    """Schema for creating equipment state"""
    state: str
    reason_code: Optional[str] = None
    reason_description: Optional[str] = None
    work_order_id: Optional[int] = None
    operator_name: Optional[str] = None


class EquipmentStateResponse(BaseModel):
    """Schema for equipment state response"""
    state_id: int
    equipment_id: int
    state: str
    state_start_time: datetime
    state_end_time: Optional[datetime]
    duration_minutes: Optional[Decimal]
    reason_code: Optional[str]
    reason_description: Optional[str]
    work_order_id: Optional[int]
    operator_name: Optional[str]
    
    class Config:
        from_attributes = True


class CurrentEquipmentStatus(BaseModel):
    """Schema for current equipment status"""
    equipment_id: int
    current_state: str
    state_start_time: datetime
    duration_minutes: float
    work_order_id: Optional[int]


@router.get("/{equipment_id}/status", response_model=CurrentEquipmentStatus)
def get_current_status(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current state of equipment
    """
    # Get the most recent state
    current_state = db.query(EquipmentState).filter(
        EquipmentState.equipment_id == equipment_id,
        EquipmentState.state_end_time.is_(None)
    ).order_by(desc(EquipmentState.state_start_time)).first()
    
    if not current_state:
        raise HTTPException(status_code=404, detail="No current state found for equipment")
    
    # Calculate duration
    duration = (datetime.utcnow() - current_state.state_start_time).total_seconds() / 60
    
    return CurrentEquipmentStatus(
        equipment_id=equipment_id,
        current_state=current_state.state,
        state_start_time=current_state.state_start_time,
        duration_minutes=round(duration, 2),
        work_order_id=current_state.work_order_id
    )


@router.post("/{equipment_id}/state", response_model=EquipmentStateResponse, status_code=201)
def update_equipment_state(
    equipment_id: int,
    state_data: EquipmentStateCreate,
    db: Session = Depends(get_db)
):
    """
    Update equipment state
    """
    # Close any open states for this equipment
    open_states = db.query(EquipmentState).filter(
        EquipmentState.equipment_id == equipment_id,
        EquipmentState.state_end_time.is_(None)
    ).all()
    
    now = datetime.utcnow()
    
    for open_state in open_states:
        open_state.state_end_time = now
        duration = (now - open_state.state_start_time).total_seconds() / 60
        open_state.duration_minutes = Decimal(str(duration))
    
    # Create new state
    new_state = EquipmentState(
        equipment_id=equipment_id,
        state=state_data.state,
        state_start_time=now,
        reason_code=state_data.reason_code,
        reason_description=state_data.reason_description,
        work_order_id=state_data.work_order_id,
        operator_name=state_data.operator_name,
    )
    
    db.add(new_state)
    db.commit()
    db.refresh(new_state)
    
    return new_state


@router.get("/{equipment_id}/timeline", response_model=List[EquipmentStateResponse])
def get_state_timeline(
    equipment_id: int,
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    db: Session = Depends(get_db)
):
    """
    Get equipment state timeline
    """
    query = db.query(EquipmentState).filter(
        EquipmentState.equipment_id == equipment_id
    )
    
    if start_time:
        query = query.filter(EquipmentState.state_start_time >= start_time)
    if end_time:
        query = query.filter(EquipmentState.state_start_time < end_time)
    
    states = query.order_by(EquipmentState.state_start_time.desc()).limit(100).all()
    
    return states
