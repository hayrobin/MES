# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 4: Product & Production Definitions
"""

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Product Family Schemas
class ProductFamilyBase(BaseModel):
    family_code: str
    family_name: str
    description: Optional[str] = None
    is_active: int = 1


class ProductFamilyCreate(ProductFamilyBase, GovernanceBase):
    pass


class ProductFamilyUpdate(BaseModel):
    family_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class ProductFamilyResponse(ProductFamilyBase, GovernanceBase, ResponseBase):
    family_id: int


# Product Master Schemas
class ProductMasterBase(BaseModel):
    product_code: str
    product_name: str
    product_family_id: Optional[int] = None
    standard_cycle_time: Optional[int] = None
    standard_output_rate: Optional[Decimal] = None
    base_uom: str
    erp_product_code: Optional[str] = None
    description: Optional[str] = None
    is_active: int = 1


class ProductMasterCreate(ProductMasterBase, GovernanceBase):
    pass


class ProductMasterUpdate(BaseModel):
    product_name: Optional[str] = None
    product_family_id: Optional[int] = None
    standard_cycle_time: Optional[int] = None
    standard_output_rate: Optional[Decimal] = None
    base_uom: Optional[str] = None
    erp_product_code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class ProductMasterResponse(ProductMasterBase, GovernanceBase, ResponseBase):
    product_id: int


# Product Equipment Compatibility Schemas
class ProductEquipmentCompatibilityBase(BaseModel):
    product_id: int
    equipment_id: int
    is_preferred_equipment: int = 0
    setup_time: Optional[int] = None
    capacity_constraint: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: int = 1


class ProductEquipmentCompatibilityCreate(ProductEquipmentCompatibilityBase, GovernanceBase):
    pass


class ProductEquipmentCompatibilityUpdate(BaseModel):
    product_id: Optional[int] = None
    equipment_id: Optional[int] = None
    is_preferred_equipment: Optional[int] = None
    setup_time: Optional[int] = None
    capacity_constraint: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class ProductEquipmentCompatibilityResponse(ProductEquipmentCompatibilityBase, GovernanceBase, ResponseBase):
    compatibility_id: int
