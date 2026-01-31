# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 4: Product & Production Definitions
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import product as models
from mes_config.schemas import product as schemas
from mes_config.services.validation import validate_unique_code, validate_foreign_key_exists
from mes_config.models.governance import ApprovalStatus

router = APIRouter()


# Product Family endpoints
@router.get("/product-families", response_model=List[schemas.ProductFamilyResponse])
def list_product_families(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all product families"""
    query = db.query(models.ProductFamily)
    if is_active is not None:
        query = query.filter(models.ProductFamily.is_active == is_active)
    families = query.offset(skip).limit(limit).all()
    return families


@router.get("/product-families/{family_id}", response_model=schemas.ProductFamilyResponse)
def get_product_family(family_id: int, db: Session = Depends(get_db)):
    """Get a specific product family by ID"""
    family = db.query(models.ProductFamily).filter(models.ProductFamily.family_id == family_id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Product family not found")
    return family


@router.post("/product-families", response_model=schemas.ProductFamilyResponse, status_code=status.HTTP_201_CREATED)
def create_product_family(family: schemas.ProductFamilyCreate, db: Session = Depends(get_db)):
    """Create a new product family"""
    validate_unique_code(db, models.ProductFamily, "family_code", family.family_code)
    
    db_family = models.ProductFamily(**family.model_dump())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family


@router.put("/product-families/{family_id}", response_model=schemas.ProductFamilyResponse)
def update_product_family(family_id: int, family: schemas.ProductFamilyUpdate, db: Session = Depends(get_db)):
    """Update a product family"""
    db_family = db.query(models.ProductFamily).filter(models.ProductFamily.family_id == family_id).first()
    if not db_family:
        raise HTTPException(status_code=404, detail="Product family not found")
    
    for field, value in family.model_dump(exclude_unset=True).items():
        setattr(db_family, field, value)
    
    db.commit()
    db.refresh(db_family)
    return db_family


@router.delete("/product-families/{family_id}", response_model=schemas.ProductFamilyResponse)
def delete_product_family(family_id: int, db: Session = Depends(get_db)):
    """Archive a product family"""
    db_family = db.query(models.ProductFamily).filter(models.ProductFamily.family_id == family_id).first()
    if not db_family:
        raise HTTPException(status_code=404, detail="Product family not found")
    
    db_family.approval_status = ApprovalStatus.ARCHIVED
    db_family.is_active = 0
    db.commit()
    db.refresh(db_family)
    return db_family


# Product Master endpoints
@router.get("/products", response_model=List[schemas.ProductMasterResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_family_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all products"""
    query = db.query(models.ProductMaster)
    if product_family_id:
        query = query.filter(models.ProductMaster.product_family_id == product_family_id)
    if is_active is not None:
        query = query.filter(models.ProductMaster.is_active == is_active)
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=schemas.ProductMasterResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(models.ProductMaster).filter(models.ProductMaster.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=schemas.ProductMasterResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductMasterCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    validate_unique_code(db, models.ProductMaster, "product_code", product.product_code)
    
    db_product = models.ProductMaster(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=schemas.ProductMasterResponse)
def update_product(product_id: int, product: schemas.ProductMasterUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(models.ProductMaster).filter(models.ProductMaster.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", response_model=schemas.ProductMasterResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Archive a product"""
    db_product = db.query(models.ProductMaster).filter(models.ProductMaster.product_id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.approval_status = ApprovalStatus.ARCHIVED
    db_product.is_active = 0
    db.commit()
    db.refresh(db_product)
    return db_product


# Product Equipment Compatibility endpoints
@router.get("/product-equipment-compatibility", response_model=List[schemas.ProductEquipmentCompatibilityResponse])
def list_product_equipment_compatibility(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_id: Optional[int] = Query(None),
    equipment_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all product equipment compatibility records"""
    query = db.query(models.ProductEquipmentCompatibility)
    if product_id:
        query = query.filter(models.ProductEquipmentCompatibility.product_id == product_id)
    if equipment_id:
        query = query.filter(models.ProductEquipmentCompatibility.equipment_id == equipment_id)
    if is_active is not None:
        query = query.filter(models.ProductEquipmentCompatibility.is_active == is_active)
    compatibility = query.offset(skip).limit(limit).all()
    return compatibility


@router.get("/product-equipment-compatibility/{compatibility_id}", response_model=schemas.ProductEquipmentCompatibilityResponse)
def get_product_equipment_compatibility(compatibility_id: int, db: Session = Depends(get_db)):
    """Get a specific product equipment compatibility by ID"""
    compatibility = db.query(models.ProductEquipmentCompatibility).filter(models.ProductEquipmentCompatibility.compatibility_id == compatibility_id).first()
    if not compatibility:
        raise HTTPException(status_code=404, detail="Product equipment compatibility not found")
    return compatibility


@router.post("/product-equipment-compatibility", response_model=schemas.ProductEquipmentCompatibilityResponse, status_code=status.HTTP_201_CREATED)
def create_product_equipment_compatibility(compatibility: schemas.ProductEquipmentCompatibilityCreate, db: Session = Depends(get_db)):
    """Create a new product equipment compatibility"""
    db_compatibility = models.ProductEquipmentCompatibility(**compatibility.model_dump())
    db.add(db_compatibility)
    db.commit()
    db.refresh(db_compatibility)
    return db_compatibility


@router.put("/product-equipment-compatibility/{compatibility_id}", response_model=schemas.ProductEquipmentCompatibilityResponse)
def update_product_equipment_compatibility(compatibility_id: int, compatibility: schemas.ProductEquipmentCompatibilityUpdate, db: Session = Depends(get_db)):
    """Update a product equipment compatibility"""
    db_compatibility = db.query(models.ProductEquipmentCompatibility).filter(models.ProductEquipmentCompatibility.compatibility_id == compatibility_id).first()
    if not db_compatibility:
        raise HTTPException(status_code=404, detail="Product equipment compatibility not found")
    
    for field, value in compatibility.model_dump(exclude_unset=True).items():
        setattr(db_compatibility, field, value)
    
    db.commit()
    db.refresh(db_compatibility)
    return db_compatibility


@router.delete("/product-equipment-compatibility/{compatibility_id}", response_model=schemas.ProductEquipmentCompatibilityResponse)
def delete_product_equipment_compatibility(compatibility_id: int, db: Session = Depends(get_db)):
    """Archive a product equipment compatibility"""
    db_compatibility = db.query(models.ProductEquipmentCompatibility).filter(models.ProductEquipmentCompatibility.compatibility_id == compatibility_id).first()
    if not db_compatibility:
        raise HTTPException(status_code=404, detail="Product equipment compatibility not found")
    
    db_compatibility.approval_status = ApprovalStatus.ARCHIVED
    db_compatibility.is_active = 0
    db.commit()
    db.refresh(db_compatibility)
    return db_compatibility
