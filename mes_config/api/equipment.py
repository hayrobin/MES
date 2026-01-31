# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 2: Equipment & Capacity Definition
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import equipment as models
from mes_config.schemas import equipment as schemas
from mes_config.services.validation import validate_unique_code, validate_foreign_key_exists
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# Equipment Master endpoints
@router.get("/equipment", response_model=List[schemas.EquipmentMasterResponse])
def list_equipment(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    equipment_type: Optional[str] = Query(None),
    site_id: Optional[int] = Query(None),
    area_id: Optional[int] = Query(None),
    line_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all equipment"""
    query = db.query(models.EquipmentMaster)
    if equipment_type:
        query = query.filter(models.EquipmentMaster.equipment_type == equipment_type)
    if site_id:
        query = query.filter(models.EquipmentMaster.site_id == site_id)
    if area_id:
        query = query.filter(models.EquipmentMaster.area_id == area_id)
    if line_id:
        query = query.filter(models.EquipmentMaster.line_id == line_id)
    if is_active is not None:
        query = query.filter(models.EquipmentMaster.is_active == is_active)
    equipment = query.offset(skip).limit(limit).all()
    return equipment


@router.get("/equipment/{equipment_id}", response_model=schemas.EquipmentMasterResponse)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Get a specific equipment by ID"""
    equipment = db.query(models.EquipmentMaster).filter(models.EquipmentMaster.equipment_id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.post("/equipment", response_model=schemas.EquipmentMasterResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment: schemas.EquipmentMasterCreate, db: Session = Depends(get_db)):
    """Create a new equipment"""
    validate_unique_code(db, models.EquipmentMaster, "equipment_code", equipment.equipment_code)
    
    db_equipment = models.EquipmentMaster(**equipment.model_dump())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.put("/equipment/{equipment_id}", response_model=schemas.EquipmentMasterResponse)
def update_equipment(equipment_id: int, equipment: schemas.EquipmentMasterUpdate, db: Session = Depends(get_db)):
    """Update an equipment"""
    db_equipment = db.query(models.EquipmentMaster).filter(models.EquipmentMaster.equipment_id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for field, value in equipment.model_dump(exclude_unset=True).items():
        setattr(db_equipment, field, value)
    
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.delete("/equipment/{equipment_id}", response_model=schemas.EquipmentMasterResponse)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """Archive an equipment"""
    db_equipment = db.query(models.EquipmentMaster).filter(models.EquipmentMaster.equipment_id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db_equipment.approval_status = ApprovalStatus.ARCHIVED
    db_equipment.is_active = 0
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


# Equipment Capacity endpoints
@router.get("/equipment-capacity", response_model=List[schemas.EquipmentCapacityResponse])
def list_equipment_capacity(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    equipment_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all equipment capacities"""
    query = db.query(models.EquipmentCapacity)
    if equipment_id:
        query = query.filter(models.EquipmentCapacity.equipment_id == equipment_id)
    if product_id:
        query = query.filter(models.EquipmentCapacity.product_id == product_id)
    if is_active is not None:
        query = query.filter(models.EquipmentCapacity.is_active == is_active)
    capacities = query.offset(skip).limit(limit).all()
    return capacities


@router.get("/equipment-capacity/{capacity_id}", response_model=schemas.EquipmentCapacityResponse)
def get_equipment_capacity(capacity_id: int, db: Session = Depends(get_db)):
    """Get a specific equipment capacity by ID"""
    capacity = db.query(models.EquipmentCapacity).filter(models.EquipmentCapacity.capacity_id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=404, detail="Equipment capacity not found")
    return capacity


@router.post("/equipment-capacity", response_model=schemas.EquipmentCapacityResponse, status_code=status.HTTP_201_CREATED)
def create_equipment_capacity(capacity: schemas.EquipmentCapacityCreate, db: Session = Depends(get_db)):
    """Create a new equipment capacity"""
    validate_foreign_key_exists(db, models.EquipmentMaster, "equipment_id", capacity.equipment_id, "Equipment")
    
    db_capacity = models.EquipmentCapacity(**capacity.model_dump())
    db.add(db_capacity)
    db.commit()
    db.refresh(db_capacity)
    return db_capacity


@router.put("/equipment-capacity/{capacity_id}", response_model=schemas.EquipmentCapacityResponse)
def update_equipment_capacity(capacity_id: int, capacity: schemas.EquipmentCapacityUpdate, db: Session = Depends(get_db)):
    """Update an equipment capacity"""
    db_capacity = db.query(models.EquipmentCapacity).filter(models.EquipmentCapacity.capacity_id == capacity_id).first()
    if not db_capacity:
        raise HTTPException(status_code=404, detail="Equipment capacity not found")
    
    for field, value in capacity.model_dump(exclude_unset=True).items():
        setattr(db_capacity, field, value)
    
    db.commit()
    db.refresh(db_capacity)
    return db_capacity


@router.delete("/equipment-capacity/{capacity_id}", response_model=schemas.EquipmentCapacityResponse)
def delete_equipment_capacity(capacity_id: int, db: Session = Depends(get_db)):
    """Archive an equipment capacity"""
    db_capacity = db.query(models.EquipmentCapacity).filter(models.EquipmentCapacity.capacity_id == capacity_id).first()
    if not db_capacity:
        raise HTTPException(status_code=404, detail="Equipment capacity not found")
    
    db_capacity.approval_status = ApprovalStatus.ARCHIVED
    db_capacity.is_active = 0
    db.commit()
    db.refresh(db_capacity)
    return db_capacity
