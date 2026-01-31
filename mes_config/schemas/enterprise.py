# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 1: Enterprise & Organizational Configuration
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Enterprise Schemas
class EnterpriseBase(BaseModel):
    enterprise_code: str
    enterprise_name: str
    erp_reference: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: int = 1


class EnterpriseCreate(EnterpriseBase, GovernanceBase):
    pass


class EnterpriseUpdate(BaseModel):
    enterprise_name: Optional[str] = None
    erp_reference: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class EnterpriseResponse(EnterpriseBase, GovernanceBase, ResponseBase):
    enterprise_id: int


# Site Schemas
class SiteBase(BaseModel):
    site_code: str
    site_name: str
    enterprise_id: int
    erp_reference: Optional[str] = None
    timezone: Optional[str] = None
    location: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: int = 1


class SiteCreate(SiteBase, GovernanceBase):
    pass


class SiteUpdate(BaseModel):
    site_name: Optional[str] = None
    enterprise_id: Optional[int] = None
    erp_reference: Optional[str] = None
    timezone: Optional[str] = None
    location: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class SiteResponse(SiteBase, GovernanceBase, ResponseBase):
    site_id: int


# Area Schemas
class AreaBase(BaseModel):
    area_code: str
    area_name: str
    site_id: int
    description: Optional[str] = None
    is_active: int = 1


class AreaCreate(AreaBase, GovernanceBase):
    pass


class AreaUpdate(BaseModel):
    area_name: Optional[str] = None
    site_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class AreaResponse(AreaBase, GovernanceBase, ResponseBase):
    area_id: int


# Line Schemas
class LineBase(BaseModel):
    line_code: str
    line_name: str
    area_id: int
    site_id: int
    description: Optional[str] = None
    is_active: int = 1


class LineCreate(LineBase, GovernanceBase):
    pass


class LineUpdate(BaseModel):
    line_name: Optional[str] = None
    area_id: Optional[int] = None
    site_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class LineResponse(LineBase, GovernanceBase, ResponseBase):
    line_id: int


# Department Schemas
class DepartmentBase(BaseModel):
    department_code: str
    department_name: str
    site_id: int
    parent_department_id: Optional[int] = None
    manager_name: Optional[str] = None
    cost_center: Optional[str] = None
    is_active: int = 1


class DepartmentCreate(DepartmentBase, GovernanceBase):
    pass


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    site_id: Optional[int] = None
    parent_department_id: Optional[int] = None
    manager_name: Optional[str] = None
    cost_center: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class DepartmentResponse(DepartmentBase, GovernanceBase, ResponseBase):
    department_id: int


# Shift Calendar Schemas
class ShiftCalendarBase(BaseModel):
    shift_code: str
    shift_name: str
    site_id: int
    start_time: time
    end_time: time
    duration_minutes: int
    days_of_week: str
    description: Optional[str] = None
    is_active: int = 1


class ShiftCalendarCreate(ShiftCalendarBase, GovernanceBase):
    pass


class ShiftCalendarUpdate(BaseModel):
    shift_name: Optional[str] = None
    site_id: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    days_of_week: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class ShiftCalendarResponse(ShiftCalendarBase, GovernanceBase, ResponseBase):
    shift_id: int


# Unit of Measure Schemas
class UnitOfMeasureBase(BaseModel):
    uom_code: str
    uom_name: str
    uom_type: str
    conversion_factor: Optional[str] = None
    base_uom_code: Optional[str] = None
    is_active: int = 1


class UnitOfMeasureCreate(UnitOfMeasureBase, GovernanceBase):
    pass


class UnitOfMeasureUpdate(BaseModel):
    uom_name: Optional[str] = None
    uom_type: Optional[str] = None
    conversion_factor: Optional[str] = None
    base_uom_code: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class UnitOfMeasureResponse(UnitOfMeasureBase, GovernanceBase, ResponseBase):
    uom_id: int
