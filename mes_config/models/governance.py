# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from mes_config.database import Base
import enum


class ApprovalStatus(enum.Enum):
    """Approval status for master data records"""
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    ARCHIVED = "ARCHIVED"


class AuditAction(enum.Enum):
    """Audit trail actions"""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    APPROVE = "APPROVE"
    ARCHIVE = "ARCHIVE"


class GovernanceMixin:
    """
    Mixin for governance fields to be included in all configuration tables.
    Provides versioning, audit trail, and approval workflow support.
    """
    
    version = Column(Integer, default=1, nullable=False)
    effective_from = Column(DateTime, nullable=False, default=func.now())
    effective_to = Column(DateTime, nullable=True)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.DRAFT, nullable=False)
    
    created_by = Column(String(100), nullable=False, default="system")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)


class AuditTrail(Base):
    """Audit trail for all configuration changes"""
    
    __tablename__ = "mes_config_audit_trail"
    
    audit_id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False, index=True)
    record_id = Column(Integer, nullable=False, index=True)
    action = Column(SQLEnum(AuditAction), nullable=False)
    changed_by = Column(String(100), nullable=False)
    changed_at = Column(DateTime, nullable=False, default=func.now())
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)


class UserRole(Base):
    """User roles for role-based access control"""
    
    __tablename__ = "mes_config_user_role"
    
    role_id = Column(Integer, primary_key=True, index=True)
    role_code = Column(String(50), unique=True, nullable=False, index=True)
    role_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)  # Using Integer for SQLite compatibility


class RolePermission(Base):
    """Role to permission mapping"""
    
    __tablename__ = "mes_config_role_permission"
    
    permission_id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    can_create = Column(Integer, default=0, nullable=False)
    can_read = Column(Integer, default=1, nullable=False)
    can_update = Column(Integer, default=0, nullable=False)
    can_delete = Column(Integer, default=0, nullable=False)
    can_approve = Column(Integer, default=0, nullable=False)
