# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 7: OEE Targets & KPI Configuration
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import kpi_targets as models
from mes_config.schemas import kpi_targets as schemas
from mes_config.services.validation import validate_unique_code
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# OEE Target endpoints
@router.get("/oee-targets", response_model=List[schemas.OeeTargetResponse])
def list_oee_targets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    target_type: Optional[str] = Query(None),
    product_id: Optional[int] = Query(None),
    line_id: Optional[int] = Query(None),
    equipment_id: Optional[int] = Query(None),
    site_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all OEE targets"""
    query = db.query(models.OeeTarget)
    if target_type:
        query = query.filter(models.OeeTarget.target_type == target_type)
    if product_id:
        query = query.filter(models.OeeTarget.product_id == product_id)
    if line_id:
        query = query.filter(models.OeeTarget.line_id == line_id)
    if equipment_id:
        query = query.filter(models.OeeTarget.equipment_id == equipment_id)
    if site_id:
        query = query.filter(models.OeeTarget.site_id == site_id)
    if is_active is not None:
        query = query.filter(models.OeeTarget.is_active == is_active)
    targets = query.offset(skip).limit(limit).all()
    return targets


@router.get("/oee-targets/{target_id}", response_model=schemas.OeeTargetResponse)
def get_oee_target(target_id: int, db: Session = Depends(get_db)):
    """Get a specific OEE target by ID"""
    target = db.query(models.OeeTarget).filter(models.OeeTarget.target_id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="OEE target not found")
    return target


@router.post("/oee-targets", response_model=schemas.OeeTargetResponse, status_code=status.HTTP_201_CREATED)
def create_oee_target(target: schemas.OeeTargetCreate, db: Session = Depends(get_db)):
    """Create a new OEE target"""
    db_target = models.OeeTarget(**target.model_dump())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target


@router.put("/oee-targets/{target_id}", response_model=schemas.OeeTargetResponse)
def update_oee_target(target_id: int, target: schemas.OeeTargetUpdate, db: Session = Depends(get_db)):
    """Update an OEE target"""
    db_target = db.query(models.OeeTarget).filter(models.OeeTarget.target_id == target_id).first()
    if not db_target:
        raise HTTPException(status_code=404, detail="OEE target not found")
    
    for field, value in target.model_dump(exclude_unset=True).items():
        setattr(db_target, field, value)
    
    db.commit()
    db.refresh(db_target)
    return db_target


@router.delete("/oee-targets/{target_id}", response_model=schemas.OeeTargetResponse)
def delete_oee_target(target_id: int, db: Session = Depends(get_db)):
    """Archive an OEE target"""
    db_target = db.query(models.OeeTarget).filter(models.OeeTarget.target_id == target_id).first()
    if not db_target:
        raise HTTPException(status_code=404, detail="OEE target not found")
    
    db_target.approval_status = ApprovalStatus.ARCHIVED
    db_target.is_active = 0
    db.commit()
    db.refresh(db_target)
    return db_target


# KPI Definition endpoints
@router.get("/kpi-definitions", response_model=List[schemas.KpiDefinitionResponse])
def list_kpi_definitions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    kpi_category: Optional[str] = Query(None),
    kpi_type: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all KPI definitions"""
    query = db.query(models.KpiDefinition)
    if kpi_category:
        query = query.filter(models.KpiDefinition.kpi_category == kpi_category)
    if kpi_type:
        query = query.filter(models.KpiDefinition.kpi_type == kpi_type)
    if is_active is not None:
        query = query.filter(models.KpiDefinition.is_active == is_active)
    kpis = query.offset(skip).limit(limit).all()
    return kpis


@router.get("/kpi-definitions/{kpi_id}", response_model=schemas.KpiDefinitionResponse)
def get_kpi_definition(kpi_id: int, db: Session = Depends(get_db)):
    """Get a specific KPI definition by ID"""
    kpi = db.query(models.KpiDefinition).filter(models.KpiDefinition.kpi_id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI definition not found")
    return kpi


@router.post("/kpi-definitions", response_model=schemas.KpiDefinitionResponse, status_code=status.HTTP_201_CREATED)
def create_kpi_definition(kpi: schemas.KpiDefinitionCreate, db: Session = Depends(get_db)):
    """Create a new KPI definition"""
    validate_unique_code(db, models.KpiDefinition, "kpi_code", kpi.kpi_code)
    
    db_kpi = models.KpiDefinition(**kpi.model_dump())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi


@router.put("/kpi-definitions/{kpi_id}", response_model=schemas.KpiDefinitionResponse)
def update_kpi_definition(kpi_id: int, kpi: schemas.KpiDefinitionUpdate, db: Session = Depends(get_db)):
    """Update a KPI definition"""
    db_kpi = db.query(models.KpiDefinition).filter(models.KpiDefinition.kpi_id == kpi_id).first()
    if not db_kpi:
        raise HTTPException(status_code=404, detail="KPI definition not found")
    
    for field, value in kpi.model_dump(exclude_unset=True).items():
        setattr(db_kpi, field, value)
    
    db.commit()
    db.refresh(db_kpi)
    return db_kpi


@router.delete("/kpi-definitions/{kpi_id}", response_model=schemas.KpiDefinitionResponse)
def delete_kpi_definition(kpi_id: int, db: Session = Depends(get_db)):
    """Archive a KPI definition"""
    db_kpi = db.query(models.KpiDefinition).filter(models.KpiDefinition.kpi_id == kpi_id).first()
    if not db_kpi:
        raise HTTPException(status_code=404, detail="KPI definition not found")
    
    db_kpi.approval_status = ApprovalStatus.ARCHIVED
    db_kpi.is_active = 0
    db.commit()
    db.refresh(db_kpi)
    return db_kpi
