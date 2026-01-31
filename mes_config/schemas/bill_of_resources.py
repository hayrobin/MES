# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 5: Bill of Resources
"""

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Bill of Resources Schemas
class BillOfResourcesBase(BaseModel):
    product_id: int
    equipment_id: int
    operation_sequence: int
    operation_name: Optional[str] = None
    standard_time: Optional[int] = None
    setup_time: Optional[int] = None
    description: Optional[str] = None
    is_active: int = 1


class BillOfResourcesCreate(BillOfResourcesBase, GovernanceBase):
    pass


class BillOfResourcesUpdate(BaseModel):
    product_id: Optional[int] = None
    equipment_id: Optional[int] = None
    operation_sequence: Optional[int] = None
    operation_name: Optional[str] = None
    standard_time: Optional[int] = None
    setup_time: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class BillOfResourcesResponse(BillOfResourcesBase, GovernanceBase, ResponseBase):
    bor_id: int


# BoR Material Schemas
class BorMaterialBase(BaseModel):
    product_id: int
    material_id: int
    standard_quantity: Decimal
    uom: str
    scrap_factor: Optional[Decimal] = 0
    operation_sequence: Optional[int] = None
    description: Optional[str] = None
    is_active: int = 1


class BorMaterialCreate(BorMaterialBase, GovernanceBase):
    pass


class BorMaterialUpdate(BaseModel):
    product_id: Optional[int] = None
    material_id: Optional[int] = None
    standard_quantity: Optional[Decimal] = None
    uom: Optional[str] = None
    scrap_factor: Optional[Decimal] = None
    operation_sequence: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class BorMaterialResponse(BorMaterialBase, GovernanceBase, ResponseBase):
    bor_material_id: int


# BoR Tooling Schemas
class BorToolingBase(BaseModel):
    product_id: int
    tooling_code: str
    tooling_name: str
    operation_sequence: Optional[int] = None
    quantity_required: int = 1
    description: Optional[str] = None
    is_active: int = 1


class BorToolingCreate(BorToolingBase, GovernanceBase):
    pass


class BorToolingUpdate(BaseModel):
    product_id: Optional[int] = None
    tooling_code: Optional[str] = None
    tooling_name: Optional[str] = None
    operation_sequence: Optional[int] = None
    quantity_required: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class BorToolingResponse(BorToolingBase, GovernanceBase, ResponseBase):
    bor_tooling_id: int


# BoR Quality Checkpoint Schemas
class BorQualityCheckpointBase(BaseModel):
    product_id: int
    checkpoint_code: str
    checkpoint_name: str
    checkpoint_type: str
    operation_sequence: Optional[int] = None
    required: int = 1
    description: Optional[str] = None
    is_active: int = 1


class BorQualityCheckpointCreate(BorQualityCheckpointBase, GovernanceBase):
    pass


class BorQualityCheckpointUpdate(BaseModel):
    product_id: Optional[int] = None
    checkpoint_code: Optional[str] = None
    checkpoint_name: Optional[str] = None
    checkpoint_type: Optional[str] = None
    operation_sequence: Optional[int] = None
    required: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class BorQualityCheckpointResponse(BorQualityCheckpointBase, GovernanceBase, ResponseBase):
    checkpoint_id: int
