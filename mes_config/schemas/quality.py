# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 6: Quality Rejection & Defect Codes
"""

from pydantic import BaseModel
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Rejection Code Category Schemas
class RejectionCodeCategoryBase(BaseModel):
    category_code: str
    category_name: str
    rejection_type: str
    description: Optional[str] = None
    is_active: int = 1


class RejectionCodeCategoryCreate(RejectionCodeCategoryBase, GovernanceBase):
    pass


class RejectionCodeCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    rejection_type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class RejectionCodeCategoryResponse(RejectionCodeCategoryBase, GovernanceBase, ResponseBase):
    category_id: int


# Material Rejection Code Schemas
class MaterialRejectionCodeBase(BaseModel):
    rejection_code: str
    rejection_name: str
    category_id: int
    rejection_source: Optional[str] = None
    classification: str
    severity_level: int = 3
    cost_impact_indicator: str = "Medium"
    root_cause_description: Optional[str] = None
    description: Optional[str] = None
    is_active: int = 1


class MaterialRejectionCodeCreate(MaterialRejectionCodeBase, GovernanceBase):
    pass


class MaterialRejectionCodeUpdate(BaseModel):
    rejection_name: Optional[str] = None
    category_id: Optional[int] = None
    rejection_source: Optional[str] = None
    classification: Optional[str] = None
    severity_level: Optional[int] = None
    cost_impact_indicator: Optional[str] = None
    root_cause_description: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class MaterialRejectionCodeResponse(MaterialRejectionCodeBase, GovernanceBase, ResponseBase):
    rejection_code_id: int


# Production Rejection Code Schemas
class ProductionRejectionCodeBase(BaseModel):
    rejection_code: str
    rejection_name: str
    category_id: int
    defect_type: Optional[str] = None
    defect_source: Optional[str] = None
    classification: str
    severity_level: int = 3
    cost_impact_indicator: str = "Medium"
    corrective_action_required: int = 0
    root_cause_description: Optional[str] = None
    description: Optional[str] = None
    is_active: int = 1


class ProductionRejectionCodeCreate(ProductionRejectionCodeBase, GovernanceBase):
    pass


class ProductionRejectionCodeUpdate(BaseModel):
    rejection_name: Optional[str] = None
    category_id: Optional[int] = None
    defect_type: Optional[str] = None
    defect_source: Optional[str] = None
    classification: Optional[str] = None
    severity_level: Optional[int] = None
    cost_impact_indicator: Optional[str] = None
    corrective_action_required: Optional[int] = None
    root_cause_description: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class ProductionRejectionCodeResponse(ProductionRejectionCodeBase, GovernanceBase, ResponseBase):
    rejection_code_id: int
