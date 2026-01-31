# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 5: Bill of Resources
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import bill_of_resources as models
from mes_config.schemas import bill_of_resources as schemas
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# Bill of Resources endpoints
@router.get("/bill-of-resources", response_model=List[schemas.BillOfResourcesResponse])
def list_bill_of_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[int] = Query(None),
    equipment_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all bill of resources"""
    query = db.query(models.BillOfResources)
    if product_id:
        query = query.filter(models.BillOfResources.product_id == product_id)
    if equipment_id:
        query = query.filter(models.BillOfResources.equipment_id == equipment_id)
    if is_active is not None:
        query = query.filter(models.BillOfResources.is_active == is_active)
    bor = query.offset(skip).limit(limit).all()
    return bor


@router.get("/bill-of-resources/{bor_id}", response_model=schemas.BillOfResourcesResponse)
def get_bill_of_resources(bor_id: int, db: Session = Depends(get_db)):
    """Get a specific bill of resources by ID"""
    bor = db.query(models.BillOfResources).filter(models.BillOfResources.bor_id == bor_id).first()
    if not bor:
        raise HTTPException(status_code=404, detail="Bill of resources not found")
    return bor


@router.post("/bill-of-resources", response_model=schemas.BillOfResourcesResponse, status_code=status.HTTP_201_CREATED)
def create_bill_of_resources(bor: schemas.BillOfResourcesCreate, db: Session = Depends(get_db)):
    """Create a new bill of resources"""
    db_bor = models.BillOfResources(**bor.model_dump())
    db.add(db_bor)
    db.commit()
    db.refresh(db_bor)
    return db_bor


@router.put("/bill-of-resources/{bor_id}", response_model=schemas.BillOfResourcesResponse)
def update_bill_of_resources(bor_id: int, bor: schemas.BillOfResourcesUpdate, db: Session = Depends(get_db)):
    """Update a bill of resources"""
    db_bor = db.query(models.BillOfResources).filter(models.BillOfResources.bor_id == bor_id).first()
    if not db_bor:
        raise HTTPException(status_code=404, detail="Bill of resources not found")
    
    for field, value in bor.model_dump(exclude_unset=True).items():
        setattr(db_bor, field, value)
    
    db.commit()
    db.refresh(db_bor)
    return db_bor


@router.delete("/bill-of-resources/{bor_id}", response_model=schemas.BillOfResourcesResponse)
def delete_bill_of_resources(bor_id: int, db: Session = Depends(get_db)):
    """Archive a bill of resources"""
    db_bor = db.query(models.BillOfResources).filter(models.BillOfResources.bor_id == bor_id).first()
    if not db_bor:
        raise HTTPException(status_code=404, detail="Bill of resources not found")
    
    db_bor.approval_status = ApprovalStatus.ARCHIVED
    db_bor.is_active = 0
    db.commit()
    db.refresh(db_bor)
    return db_bor


# BoR Material endpoints
@router.get("/bor-materials", response_model=List[schemas.BorMaterialResponse])
def list_bor_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[int] = Query(None),
    material_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all BoR materials"""
    query = db.query(models.BorMaterial)
    if product_id:
        query = query.filter(models.BorMaterial.product_id == product_id)
    if material_id:
        query = query.filter(models.BorMaterial.material_id == material_id)
    if is_active is not None:
        query = query.filter(models.BorMaterial.is_active == is_active)
    materials = query.offset(skip).limit(limit).all()
    return materials


@router.get("/bor-materials/{bor_material_id}", response_model=schemas.BorMaterialResponse)
def get_bor_material(bor_material_id: int, db: Session = Depends(get_db)):
    """Get a specific BoR material by ID"""
    material = db.query(models.BorMaterial).filter(models.BorMaterial.bor_material_id == bor_material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="BoR material not found")
    return material


@router.post("/bor-materials", response_model=schemas.BorMaterialResponse, status_code=status.HTTP_201_CREATED)
def create_bor_material(material: schemas.BorMaterialCreate, db: Session = Depends(get_db)):
    """Create a new BoR material"""
    db_material = models.BorMaterial(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.put("/bor-materials/{bor_material_id}", response_model=schemas.BorMaterialResponse)
def update_bor_material(bor_material_id: int, material: schemas.BorMaterialUpdate, db: Session = Depends(get_db)):
    """Update a BoR material"""
    db_material = db.query(models.BorMaterial).filter(models.BorMaterial.bor_material_id == bor_material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="BoR material not found")
    
    for field, value in material.model_dump(exclude_unset=True).items():
        setattr(db_material, field, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/bor-materials/{bor_material_id}", response_model=schemas.BorMaterialResponse)
def delete_bor_material(bor_material_id: int, db: Session = Depends(get_db)):
    """Archive a BoR material"""
    db_material = db.query(models.BorMaterial).filter(models.BorMaterial.bor_material_id == bor_material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="BoR material not found")
    
    db_material.approval_status = ApprovalStatus.ARCHIVED
    db_material.is_active = 0
    db.commit()
    db.refresh(db_material)
    return db_material


# BoR Tooling endpoints
@router.get("/bor-tooling", response_model=List[schemas.BorToolingResponse])
def list_bor_tooling(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all BoR tooling"""
    query = db.query(models.BorTooling)
    if product_id:
        query = query.filter(models.BorTooling.product_id == product_id)
    if is_active is not None:
        query = query.filter(models.BorTooling.is_active == is_active)
    tooling = query.offset(skip).limit(limit).all()
    return tooling


@router.get("/bor-tooling/{bor_tooling_id}", response_model=schemas.BorToolingResponse)
def get_bor_tooling(bor_tooling_id: int, db: Session = Depends(get_db)):
    """Get a specific BoR tooling by ID"""
    tooling = db.query(models.BorTooling).filter(models.BorTooling.bor_tooling_id == bor_tooling_id).first()
    if not tooling:
        raise HTTPException(status_code=404, detail="BoR tooling not found")
    return tooling


@router.post("/bor-tooling", response_model=schemas.BorToolingResponse, status_code=status.HTTP_201_CREATED)
def create_bor_tooling(tooling: schemas.BorToolingCreate, db: Session = Depends(get_db)):
    """Create a new BoR tooling"""
    db_tooling = models.BorTooling(**tooling.model_dump())
    db.add(db_tooling)
    db.commit()
    db.refresh(db_tooling)
    return db_tooling


@router.put("/bor-tooling/{bor_tooling_id}", response_model=schemas.BorToolingResponse)
def update_bor_tooling(bor_tooling_id: int, tooling: schemas.BorToolingUpdate, db: Session = Depends(get_db)):
    """Update a BoR tooling"""
    db_tooling = db.query(models.BorTooling).filter(models.BorTooling.bor_tooling_id == bor_tooling_id).first()
    if not db_tooling:
        raise HTTPException(status_code=404, detail="BoR tooling not found")
    
    for field, value in tooling.model_dump(exclude_unset=True).items():
        setattr(db_tooling, field, value)
    
    db.commit()
    db.refresh(db_tooling)
    return db_tooling


@router.delete("/bor-tooling/{bor_tooling_id}", response_model=schemas.BorToolingResponse)
def delete_bor_tooling(bor_tooling_id: int, db: Session = Depends(get_db)):
    """Archive a BoR tooling"""
    db_tooling = db.query(models.BorTooling).filter(models.BorTooling.bor_tooling_id == bor_tooling_id).first()
    if not db_tooling:
        raise HTTPException(status_code=404, detail="BoR tooling not found")
    
    db_tooling.approval_status = ApprovalStatus.ARCHIVED
    db_tooling.is_active = 0
    db.commit()
    db.refresh(db_tooling)
    return db_tooling


# BoR Quality Checkpoint endpoints
@router.get("/bor-quality-checkpoints", response_model=List[schemas.BorQualityCheckpointResponse])
def list_bor_quality_checkpoints(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[int] = Query(None),
    checkpoint_type: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all BoR quality checkpoints"""
    query = db.query(models.BorQualityCheckpoint)
    if product_id:
        query = query.filter(models.BorQualityCheckpoint.product_id == product_id)
    if checkpoint_type:
        query = query.filter(models.BorQualityCheckpoint.checkpoint_type == checkpoint_type)
    if is_active is not None:
        query = query.filter(models.BorQualityCheckpoint.is_active == is_active)
    checkpoints = query.offset(skip).limit(limit).all()
    return checkpoints


@router.get("/bor-quality-checkpoints/{checkpoint_id}", response_model=schemas.BorQualityCheckpointResponse)
def get_bor_quality_checkpoint(checkpoint_id: int, db: Session = Depends(get_db)):
    """Get a specific BoR quality checkpoint by ID"""
    checkpoint = db.query(models.BorQualityCheckpoint).filter(models.BorQualityCheckpoint.checkpoint_id == checkpoint_id).first()
    if not checkpoint:
        raise HTTPException(status_code=404, detail="BoR quality checkpoint not found")
    return checkpoint


@router.post("/bor-quality-checkpoints", response_model=schemas.BorQualityCheckpointResponse, status_code=status.HTTP_201_CREATED)
def create_bor_quality_checkpoint(checkpoint: schemas.BorQualityCheckpointCreate, db: Session = Depends(get_db)):
    """Create a new BoR quality checkpoint"""
    db_checkpoint = models.BorQualityCheckpoint(**checkpoint.model_dump())
    db.add(db_checkpoint)
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint


@router.put("/bor-quality-checkpoints/{checkpoint_id}", response_model=schemas.BorQualityCheckpointResponse)
def update_bor_quality_checkpoint(checkpoint_id: int, checkpoint: schemas.BorQualityCheckpointUpdate, db: Session = Depends(get_db)):
    """Update a BoR quality checkpoint"""
    db_checkpoint = db.query(models.BorQualityCheckpoint).filter(models.BorQualityCheckpoint.checkpoint_id == checkpoint_id).first()
    if not db_checkpoint:
        raise HTTPException(status_code=404, detail="BoR quality checkpoint not found")
    
    for field, value in checkpoint.model_dump(exclude_unset=True).items():
        setattr(db_checkpoint, field, value)
    
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint


@router.delete("/bor-quality-checkpoints/{checkpoint_id}", response_model=schemas.BorQualityCheckpointResponse)
def delete_bor_quality_checkpoint(checkpoint_id: int, db: Session = Depends(get_db)):
    """Archive a BoR quality checkpoint"""
    db_checkpoint = db.query(models.BorQualityCheckpoint).filter(models.BorQualityCheckpoint.checkpoint_id == checkpoint_id).first()
    if not db_checkpoint:
        raise HTTPException(status_code=404, detail="BoR quality checkpoint not found")
    
    db_checkpoint.approval_status = ApprovalStatus.ARCHIVED
    db_checkpoint.is_active = 0
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint
