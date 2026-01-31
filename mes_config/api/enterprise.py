# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
REST API routes for Module 1: Enterprise & Organizational Configuration
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from mes_config.database import get_db
from mes_config.models import enterprise as models
from mes_config.schemas import enterprise as schemas
from mes_config.services.crud import CRUDBase
from mes_config.services.validation import validate_unique_code, validate_foreign_key_exists
from mes_config.models.governance import ApprovalStatus

router = APIRouter()

# CRUD instances
enterprise_crud = CRUDBase[models.Enterprise, schemas.EnterpriseCreate, schemas.EnterpriseUpdate](models.Enterprise)
site_crud = CRUDBase[models.Site, schemas.SiteCreate, schemas.SiteUpdate](models.Site)
area_crud = CRUDBase[models.Area, schemas.AreaCreate, schemas.AreaUpdate](models.Area)
line_crud = CRUDBase[models.Line, schemas.LineCreate, schemas.LineUpdate](models.Line)
department_crud = CRUDBase[models.Department, schemas.DepartmentCreate, schemas.DepartmentUpdate](models.Department)
shift_calendar_crud = CRUDBase[models.ShiftCalendar, schemas.ShiftCalendarCreate, schemas.ShiftCalendarUpdate](models.ShiftCalendar)
uom_crud = CRUDBase[models.UnitOfMeasure, schemas.UnitOfMeasureCreate, schemas.UnitOfMeasureUpdate](models.UnitOfMeasure)


# Enterprise endpoints
@router.get("/enterprise", response_model=List[schemas.EnterpriseResponse])
def list_enterprises(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[int] = Query(None),
    approval_status: Optional[ApprovalStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """List all enterprises"""
    enterprises = enterprise_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active, approval_status=approval_status)
    return enterprises


@router.get("/enterprise/{enterprise_id}", response_model=schemas.EnterpriseResponse)
def get_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """Get a specific enterprise by ID"""
    enterprise = db.query(models.Enterprise).filter(models.Enterprise.enterprise_id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise


@router.post("/enterprise", response_model=schemas.EnterpriseResponse, status_code=status.HTTP_201_CREATED)
def create_enterprise(enterprise: schemas.EnterpriseCreate, db: Session = Depends(get_db)):
    """Create a new enterprise"""
    validate_unique_code(db, models.Enterprise, "enterprise_code", enterprise.enterprise_code)
    
    db_enterprise = models.Enterprise(**enterprise.model_dump())
    db.add(db_enterprise)
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise


@router.put("/enterprise/{enterprise_id}", response_model=schemas.EnterpriseResponse)
def update_enterprise(enterprise_id: int, enterprise: schemas.EnterpriseUpdate, db: Session = Depends(get_db)):
    """Update an enterprise"""
    db_enterprise = db.query(models.Enterprise).filter(models.Enterprise.enterprise_id == enterprise_id).first()
    if not db_enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    
    for field, value in enterprise.model_dump(exclude_unset=True).items():
        setattr(db_enterprise, field, value)
    
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise


@router.delete("/enterprise/{enterprise_id}", response_model=schemas.EnterpriseResponse)
def delete_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """Archive an enterprise"""
    db_enterprise = db.query(models.Enterprise).filter(models.Enterprise.enterprise_id == enterprise_id).first()
    if not db_enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    
    db_enterprise.approval_status = ApprovalStatus.ARCHIVED
    db_enterprise.is_active = 0
    db.commit()
    db.refresh(db_enterprise)
    return db_enterprise


# Site endpoints
@router.get("/sites", response_model=List[schemas.SiteResponse])
def list_sites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    enterprise_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all sites"""
    query = db.query(models.Site)
    if enterprise_id:
        query = query.filter(models.Site.enterprise_id == enterprise_id)
    if is_active is not None:
        query = query.filter(models.Site.is_active == is_active)
    sites = query.offset(skip).limit(limit).all()
    return sites


@router.get("/sites/{site_id}", response_model=schemas.SiteResponse)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """Get a specific site by ID"""
    site = db.query(models.Site).filter(models.Site.site_id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.post("/sites", response_model=schemas.SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db)):
    """Create a new site"""
    validate_unique_code(db, models.Site, "site_code", site.site_code)
    validate_foreign_key_exists(db, models.Enterprise, "enterprise_id", site.enterprise_id, "Enterprise")
    
    db_site = models.Site(**site.model_dump())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


@router.put("/sites/{site_id}", response_model=schemas.SiteResponse)
def update_site(site_id: int, site: schemas.SiteUpdate, db: Session = Depends(get_db)):
    """Update a site"""
    db_site = db.query(models.Site).filter(models.Site.site_id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    for field, value in site.model_dump(exclude_unset=True).items():
        setattr(db_site, field, value)
    
    db.commit()
    db.refresh(db_site)
    return db_site


@router.delete("/sites/{site_id}", response_model=schemas.SiteResponse)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    """Archive a site"""
    db_site = db.query(models.Site).filter(models.Site.site_id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    db_site.approval_status = ApprovalStatus.ARCHIVED
    db_site.is_active = 0
    db.commit()
    db.refresh(db_site)
    return db_site


# Area endpoints
@router.get("/areas", response_model=List[schemas.AreaResponse])
def list_areas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    site_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all areas"""
    query = db.query(models.Area)
    if site_id:
        query = query.filter(models.Area.site_id == site_id)
    if is_active is not None:
        query = query.filter(models.Area.is_active == is_active)
    areas = query.offset(skip).limit(limit).all()
    return areas


@router.post("/areas", response_model=schemas.AreaResponse, status_code=status.HTTP_201_CREATED)
def create_area(area: schemas.AreaCreate, db: Session = Depends(get_db)):
    """Create a new area"""
    validate_unique_code(db, models.Area, "area_code", area.area_code)
    db_area = models.Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


# Line endpoints
@router.get("/lines", response_model=List[schemas.LineResponse])
def list_lines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    area_id: Optional[int] = Query(None),
    site_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all lines"""
    query = db.query(models.Line)
    if area_id:
        query = query.filter(models.Line.area_id == area_id)
    if site_id:
        query = query.filter(models.Line.site_id == site_id)
    if is_active is not None:
        query = query.filter(models.Line.is_active == is_active)
    lines = query.offset(skip).limit(limit).all()
    return lines


@router.post("/lines", response_model=schemas.LineResponse, status_code=status.HTTP_201_CREATED)
def create_line(line: schemas.LineCreate, db: Session = Depends(get_db)):
    """Create a new line"""
    validate_unique_code(db, models.Line, "line_code", line.line_code)
    db_line = models.Line(**line.model_dump())
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    return db_line


# Department endpoints
@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    site_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all departments"""
    query = db.query(models.Department)
    if site_id:
        query = query.filter(models.Department.site_id == site_id)
    if is_active is not None:
        query = query.filter(models.Department.is_active == is_active)
    departments = query.offset(skip).limit(limit).all()
    return departments


@router.post("/departments", response_model=schemas.DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department"""
    validate_unique_code(db, models.Department, "department_code", department.department_code)
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


# Shift Calendar endpoints
@router.get("/shift-calendars", response_model=List[schemas.ShiftCalendarResponse])
def list_shift_calendars(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    site_id: Optional[int] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all shift calendars"""
    query = db.query(models.ShiftCalendar)
    if site_id:
        query = query.filter(models.ShiftCalendar.site_id == site_id)
    if is_active is not None:
        query = query.filter(models.ShiftCalendar.is_active == is_active)
    shifts = query.offset(skip).limit(limit).all()
    return shifts


@router.post("/shift-calendars", response_model=schemas.ShiftCalendarResponse, status_code=status.HTTP_201_CREATED)
def create_shift_calendar(shift: schemas.ShiftCalendarCreate, db: Session = Depends(get_db)):
    """Create a new shift calendar"""
    validate_unique_code(db, models.ShiftCalendar, "shift_code", shift.shift_code)
    db_shift = models.ShiftCalendar(**shift.model_dump())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift


# Unit of Measure endpoints
@router.get("/unit-of-measures", response_model=List[schemas.UnitOfMeasureResponse])
def list_unit_of_measures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    uom_type: Optional[str] = Query(None),
    is_active: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """List all units of measure"""
    query = db.query(models.UnitOfMeasure)
    if uom_type:
        query = query.filter(models.UnitOfMeasure.uom_type == uom_type)
    if is_active is not None:
        query = query.filter(models.UnitOfMeasure.is_active == is_active)
    uoms = query.offset(skip).limit(limit).all()
    return uoms


@router.post("/unit-of-measures", response_model=schemas.UnitOfMeasureResponse, status_code=status.HTTP_201_CREATED)
def create_unit_of_measure(uom: schemas.UnitOfMeasureCreate, db: Session = Depends(get_db)):
    """Create a new unit of measure"""
    validate_unique_code(db, models.UnitOfMeasure, "uom_code", uom.uom_code)
    db_uom = models.UnitOfMeasure(**uom.model_dump())
    db.add(db_uom)
    db.commit()
    db.refresh(db_uom)
    return db_uom
