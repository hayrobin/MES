# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 6: Quality Rejection & Defect Codes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import quality as models
from mes_config.schemas import quality as schemas
from mes_config.services.validation import validate_unique_code, validate_foreign_key_exists
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# Rejection Code Category endpoints
@router.get("/rejection-code-categories", response_model=List[schemas.RejectionCodeCategoryResponse])
def list_rejection_code_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    rejection_type: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all rejection code categories"""
    query = db.query(models.RejectionCodeCategory)
    if rejection_type:
        query = query.filter(models.RejectionCodeCategory.rejection_type == rejection_type)
    if is_active is not None:
        query = query.filter(models.RejectionCodeCategory.is_active == is_active)
    categories = query.offset(skip).limit(limit).all()
    return categories


@router.get("/rejection-code-categories/{category_id}", response_model=schemas.RejectionCodeCategoryResponse)
def get_rejection_code_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific rejection code category by ID"""
    category = db.query(models.RejectionCodeCategory).filter(models.RejectionCodeCategory.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Rejection code category not found")
    return category


@router.post("/rejection-code-categories", response_model=schemas.RejectionCodeCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_rejection_code_category(category: schemas.RejectionCodeCategoryCreate, db: Session = Depends(get_db)):
    """Create a new rejection code category"""
    validate_unique_code(db, models.RejectionCodeCategory, "category_code", category.category_code)
    
    db_category = models.RejectionCodeCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/rejection-code-categories/{category_id}", response_model=schemas.RejectionCodeCategoryResponse)
def update_rejection_code_category(category_id: int, category: schemas.RejectionCodeCategoryUpdate, db: Session = Depends(get_db)):
    """Update a rejection code category"""
    db_category = db.query(models.RejectionCodeCategory).filter(models.RejectionCodeCategory.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Rejection code category not found")
    
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/rejection-code-categories/{category_id}", response_model=schemas.RejectionCodeCategoryResponse)
def delete_rejection_code_category(category_id: int, db: Session = Depends(get_db)):
    """Archive a rejection code category"""
    db_category = db.query(models.RejectionCodeCategory).filter(models.RejectionCodeCategory.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Rejection code category not found")
    
    db_category.approval_status = ApprovalStatus.ARCHIVED
    db_category.is_active = 0
    db.commit()
    db.refresh(db_category)
    return db_category


# Material Rejection Code endpoints
@router.get("/material-rejection-codes", response_model=List[schemas.MaterialRejectionCodeResponse])
def list_material_rejection_codes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    classification: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all material rejection codes"""
    query = db.query(models.MaterialRejectionCode)
    if category_id:
        query = query.filter(models.MaterialRejectionCode.category_id == category_id)
    if classification:
        query = query.filter(models.MaterialRejectionCode.classification == classification)
    if is_active is not None:
        query = query.filter(models.MaterialRejectionCode.is_active == is_active)
    codes = query.offset(skip).limit(limit).all()
    return codes


@router.get("/material-rejection-codes/{rejection_code_id}", response_model=schemas.MaterialRejectionCodeResponse)
def get_material_rejection_code(rejection_code_id: int, db: Session = Depends(get_db)):
    """Get a specific material rejection code by ID"""
    code = db.query(models.MaterialRejectionCode).filter(models.MaterialRejectionCode.rejection_code_id == rejection_code_id).first()
    if not code:
        raise HTTPException(status_code=404, detail="Material rejection code not found")
    return code


@router.post("/material-rejection-codes", response_model=schemas.MaterialRejectionCodeResponse, status_code=status.HTTP_201_CREATED)
def create_material_rejection_code(code: schemas.MaterialRejectionCodeCreate, db: Session = Depends(get_db)):
    """Create a new material rejection code"""
    validate_unique_code(db, models.MaterialRejectionCode, "rejection_code", code.rejection_code)
    validate_foreign_key_exists(db, models.RejectionCodeCategory, "category_id", code.category_id, "Rejection Code Category")
    
    db_code = models.MaterialRejectionCode(**code.model_dump())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


@router.put("/material-rejection-codes/{rejection_code_id}", response_model=schemas.MaterialRejectionCodeResponse)
def update_material_rejection_code(rejection_code_id: int, code: schemas.MaterialRejectionCodeUpdate, db: Session = Depends(get_db)):
    """Update a material rejection code"""
    db_code = db.query(models.MaterialRejectionCode).filter(models.MaterialRejectionCode.rejection_code_id == rejection_code_id).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Material rejection code not found")
    
    for field, value in code.model_dump(exclude_unset=True).items():
        setattr(db_code, field, value)
    
    db.commit()
    db.refresh(db_code)
    return db_code


@router.delete("/material-rejection-codes/{rejection_code_id}", response_model=schemas.MaterialRejectionCodeResponse)
def delete_material_rejection_code(rejection_code_id: int, db: Session = Depends(get_db)):
    """Archive a material rejection code"""
    db_code = db.query(models.MaterialRejectionCode).filter(models.MaterialRejectionCode.rejection_code_id == rejection_code_id).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Material rejection code not found")
    
    db_code.approval_status = ApprovalStatus.ARCHIVED
    db_code.is_active = 0
    db.commit()
    db.refresh(db_code)
    return db_code


# Production Rejection Code endpoints
@router.get("/production-rejection-codes", response_model=List[schemas.ProductionRejectionCodeResponse])
def list_production_rejection_codes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    defect_type: Optional[str] = Query(None),
    classification: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all production rejection codes"""
    query = db.query(models.ProductionRejectionCode)
    if category_id:
        query = query.filter(models.ProductionRejectionCode.category_id == category_id)
    if defect_type:
        query = query.filter(models.ProductionRejectionCode.defect_type == defect_type)
    if classification:
        query = query.filter(models.ProductionRejectionCode.classification == classification)
    if is_active is not None:
        query = query.filter(models.ProductionRejectionCode.is_active == is_active)
    codes = query.offset(skip).limit(limit).all()
    return codes


@router.get("/production-rejection-codes/{rejection_code_id}", response_model=schemas.ProductionRejectionCodeResponse)
def get_production_rejection_code(rejection_code_id: int, db: Session = Depends(get_db)):
    """Get a specific production rejection code by ID"""
    code = db.query(models.ProductionRejectionCode).filter(models.ProductionRejectionCode.rejection_code_id == rejection_code_id).first()
    if not code:
        raise HTTPException(status_code=404, detail="Production rejection code not found")
    return code


@router.post("/production-rejection-codes", response_model=schemas.ProductionRejectionCodeResponse, status_code=status.HTTP_201_CREATED)
def create_production_rejection_code(code: schemas.ProductionRejectionCodeCreate, db: Session = Depends(get_db)):
    """Create a new production rejection code"""
    validate_unique_code(db, models.ProductionRejectionCode, "rejection_code", code.rejection_code)
    validate_foreign_key_exists(db, models.RejectionCodeCategory, "category_id", code.category_id, "Rejection Code Category")
    
    db_code = models.ProductionRejectionCode(**code.model_dump())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


@router.put("/production-rejection-codes/{rejection_code_id}", response_model=schemas.ProductionRejectionCodeResponse)
def update_production_rejection_code(rejection_code_id: int, code: schemas.ProductionRejectionCodeUpdate, db: Session = Depends(get_db)):
    """Update a production rejection code"""
    db_code = db.query(models.ProductionRejectionCode).filter(models.ProductionRejectionCode.rejection_code_id == rejection_code_id).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Production rejection code not found")
    
    for field, value in code.model_dump(exclude_unset=True).items():
        setattr(db_code, field, value)
    
    db.commit()
    db.refresh(db_code)
    return db_code


@router.delete("/production-rejection-codes/{rejection_code_id}", response_model=schemas.ProductionRejectionCodeResponse)
def delete_production_rejection_code(rejection_code_id: int, db: Session = Depends(get_db)):
    """Archive a production rejection code"""
    db_code = db.query(models.ProductionRejectionCode).filter(models.ProductionRejectionCode.rejection_code_id == rejection_code_id).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Production rejection code not found")
    
    db_code.approval_status = ApprovalStatus.ARCHIVED
    db_code.is_active = 0
    db.commit()
    db.refresh(db_code)
    return db_code
