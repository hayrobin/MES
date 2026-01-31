# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 3: Material Master
"""

from pydantic import BaseModel
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Material Category Schemas
class MaterialCategoryBase(BaseModel):
    category_code: str
    category_name: str
    parent_category_id: Optional[int] = None
    description: Optional[str] = None
    is_active: int = 1


class MaterialCategoryCreate(MaterialCategoryBase, GovernanceBase):
    pass


class MaterialCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    parent_category_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class MaterialCategoryResponse(MaterialCategoryBase, GovernanceBase, ResponseBase):
    category_id: int


# Material Master Schemas
class MaterialMasterBase(BaseModel):
    material_code: str
    material_name: str
    material_category_id: int
    material_type: str
    base_uom: str
    batch_tracking_required: int = 0
    lot_tracking_required: int = 0
    serial_tracking_required: int = 0
    shelf_life_days: Optional[int] = None
    expiry_tracking_required: int = 0
    erp_material_code: Optional[str] = None
    supplier_reference: Optional[str] = None
    cost_center: Optional[str] = None
    description: Optional[str] = None
    is_active: int = 1


class MaterialMasterCreate(MaterialMasterBase, GovernanceBase):
    pass


class MaterialMasterUpdate(BaseModel):
    material_name: Optional[str] = None
    material_category_id: Optional[int] = None
    material_type: Optional[str] = None
    base_uom: Optional[str] = None
    batch_tracking_required: Optional[int] = None
    lot_tracking_required: Optional[int] = None
    serial_tracking_required: Optional[int] = None
    shelf_life_days: Optional[int] = None
    expiry_tracking_required: Optional[int] = None
    erp_material_code: Optional[str] = None
    supplier_reference: Optional[str] = None
    cost_center: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class MaterialMasterResponse(MaterialMasterBase, GovernanceBase, ResponseBase):
    material_id: int
