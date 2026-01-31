# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 3: Material Master
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import material as models
from mes_config.schemas import material as schemas
from mes_config.services.validation import validate_unique_code, validate_foreign_key_exists
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# Material Category endpoints
@router.get("/material-categories", response_model=List[schemas.MaterialCategoryResponse])
def list_material_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    parent_category_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all material categories"""
    query = db.query(models.MaterialCategory)
    if parent_category_id:
        query = query.filter(models.MaterialCategory.parent_category_id == parent_category_id)
    if is_active is not None:
        query = query.filter(models.MaterialCategory.is_active == is_active)
    categories = query.offset(skip).limit(limit).all()
    return categories


@router.get("/material-categories/{category_id}", response_model=schemas.MaterialCategoryResponse)
def get_material_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific material category by ID"""
    category = db.query(models.MaterialCategory).filter(models.MaterialCategory.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Material category not found")
    return category


@router.post("/material-categories", response_model=schemas.MaterialCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_material_category(category: schemas.MaterialCategoryCreate, db: Session = Depends(get_db)):
    """Create a new material category"""
    validate_unique_code(db, models.MaterialCategory, "category_code", category.category_code)
    
    db_category = models.MaterialCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/material-categories/{category_id}", response_model=schemas.MaterialCategoryResponse)
def update_material_category(category_id: int, category: schemas.MaterialCategoryUpdate, db: Session = Depends(get_db)):
    """Update a material category"""
    db_category = db.query(models.MaterialCategory).filter(models.MaterialCategory.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Material category not found")
    
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/material-categories/{category_id}", response_model=schemas.MaterialCategoryResponse)
def delete_material_category(category_id: int, db: Session = Depends(get_db)):
    """Archive a material category"""
    db_category = db.query(models.MaterialCategory).filter(models.MaterialCategory.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Material category not found")
    
    db_category.approval_status = ApprovalStatus.ARCHIVED
    db_category.is_active = 0
    db.commit()
    db.refresh(db_category)
    return db_category


# Material Master endpoints
@router.get("/materials", response_model=List[schemas.MaterialMasterResponse])
def list_materials(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    material_category_id: Optional[int] = Query(None),
    material_type: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all materials"""
    query = db.query(models.MaterialMaster)
    if material_category_id:
        query = query.filter(models.MaterialMaster.material_category_id == material_category_id)
    if material_type:
        query = query.filter(models.MaterialMaster.material_type == material_type)
    if is_active is not None:
        query = query.filter(models.MaterialMaster.is_active == is_active)
    materials = query.offset(skip).limit(limit).all()
    return materials


@router.get("/materials/{material_id}", response_model=schemas.MaterialMasterResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    """Get a specific material by ID"""
    material = db.query(models.MaterialMaster).filter(models.MaterialMaster.material_id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.post("/materials", response_model=schemas.MaterialMasterResponse, status_code=status.HTTP_201_CREATED)
def create_material(material: schemas.MaterialMasterCreate, db: Session = Depends(get_db)):
    """Create a new material"""
    validate_unique_code(db, models.MaterialMaster, "material_code", material.material_code)
    validate_foreign_key_exists(db, models.MaterialCategory, "category_id", material.material_category_id, "Material Category")
    
    db_material = models.MaterialMaster(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.put("/materials/{material_id}", response_model=schemas.MaterialMasterResponse)
def update_material(material_id: int, material: schemas.MaterialMasterUpdate, db: Session = Depends(get_db)):
    """Update a material"""
    db_material = db.query(models.MaterialMaster).filter(models.MaterialMaster.material_id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    for field, value in material.model_dump(exclude_unset=True).items():
        setattr(db_material, field, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/materials/{material_id}", response_model=schemas.MaterialMasterResponse)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    """Archive a material"""
    db_material = db.query(models.MaterialMaster).filter(models.MaterialMaster.material_id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db_material.approval_status = ApprovalStatus.ARCHIVED
    db_material.is_active = 0
    db.commit()
    db.refresh(db_material)
    return db_material
