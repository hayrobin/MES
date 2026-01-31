# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 8: Governance & Control
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any
from .base import ResponseBase
from mes_config.models.governance import AuditAction


# Audit Trail Schemas
class AuditTrailBase(BaseModel):
    table_name: str
    record_id: int
    action: AuditAction
    changed_by: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None


class AuditTrailCreate(AuditTrailBase):
    pass


class AuditTrailResponse(AuditTrailBase, ResponseBase):
    audit_id: int
    changed_at: datetime


# User Role Schemas
class UserRoleBase(BaseModel):
    role_code: str
    role_name: str
    description: Optional[str] = None
    is_active: int = 1


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    role_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None


class UserRoleResponse(UserRoleBase, ResponseBase):
    role_id: int


# Role Permission Schemas
class RolePermissionBase(BaseModel):
    role_id: int
    resource: str
    can_create: int = 0
    can_read: int = 1
    can_update: int = 0
    can_delete: int = 0
    can_approve: int = 0


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    can_create: Optional[int] = None
    can_read: Optional[int] = None
    can_update: Optional[int] = None
    can_delete: Optional[int] = None
    can_approve: Optional[int] = None


class RolePermissionResponse(RolePermissionBase, ResponseBase):
    permission_id: int


# Approval Request Schema
class ApprovalRequest(BaseModel):
    approved_by: str
    approval_notes: Optional[str] = None
