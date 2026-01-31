# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 7: OEE Targets & KPI Configuration
"""

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from .base import GovernanceBase, ResponseBase


# OEE Target Schemas
class OeeTargetBase(BaseModel):
    target_type: str
    product_id: Optional[int] = None
    line_id: Optional[int] = None
    equipment_id: Optional[int] = None
    site_id: Optional[int] = None
    availability_target: Decimal
    performance_target: Decimal
    quality_target: Decimal
    oee_target: Decimal
    description: Optional[str] = None
    is_active: int = 1


class OeeTargetCreate(OeeTargetBase, GovernanceBase):
    pass


class OeeTargetUpdate(BaseModel):
    target_type: Optional[str] = None
    product_id: Optional[int] = None
    line_id: Optional[int] = None
    equipment_id: Optional[int] = None
    site_id: Optional[int] = None
    availability_target: Optional[Decimal] = None
    performance_target: Optional[Decimal] = None
    quality_target: Optional[Decimal] = None
    oee_target: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class OeeTargetResponse(OeeTargetBase, GovernanceBase, ResponseBase):
    target_id: int


# KPI Definition Schemas
class KpiDefinitionBase(BaseModel):
    kpi_code: str
    kpi_name: str
    kpi_category: str
    kpi_type: str
    unit_of_measure: Optional[str] = None
    target_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    calculation_formula_description: Optional[str] = None
    aggregation_level: Optional[str] = None
    measurement_frequency: Optional[str] = None
    description: Optional[str] = None
    is_active: int = 1


class KpiDefinitionCreate(KpiDefinitionBase, GovernanceBase):
    pass


class KpiDefinitionUpdate(BaseModel):
    kpi_name: Optional[str] = None
    kpi_category: Optional[str] = None
    kpi_type: Optional[str] = None
    unit_of_measure: Optional[str] = None
    target_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    calculation_formula_description: Optional[str] = None
    aggregation_level: Optional[str] = None
    measurement_frequency: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class KpiDefinitionResponse(KpiDefinitionBase, GovernanceBase, ResponseBase):
    kpi_id: int
