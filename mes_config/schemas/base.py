# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Base Pydantic schemas for MES Configuration Layer
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from mes_config.models.governance import ApprovalStatus


class GovernanceBase(BaseModel):
    """Base schema with governance fields"""
    version: int = 1
    effective_from: datetime
    effective_to: Optional[datetime] = None
    approval_status: ApprovalStatus = ApprovalStatus.DRAFT
    created_by: str = "system"
    created_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None


class ResponseBase(BaseModel):
    """Base response schema with ORM mode"""
    model_config = ConfigDict(from_attributes=True)
