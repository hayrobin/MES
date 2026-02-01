"""
Quality Inspection Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class QualityInspectionCreate(BaseModel):
    """Schema for creating a quality inspection record"""
    work_order_id: int = Field(..., description="Work order ID")
    operation_execution_id: Optional[int] = Field(None, description="Operation execution ID")
    inspection_time: datetime = Field(default_factory=datetime.utcnow, description="Inspection timestamp")
    inspection_result: str = Field(..., description="PASS or FAIL")
    rejection_code_id: Optional[int] = Field(None, description="Rejection code ID if failed")
    rejected_quantity: Optional[Decimal] = Field(None, description="Quantity rejected")
    inspector_name: Optional[str] = Field(None, description="Inspector name")
    remarks: Optional[str] = Field(None, description="Additional remarks")


class QualityInspectionResponse(QualityInspectionCreate):
    """Schema for quality inspection response"""
    inspection_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RejectionSummary(BaseModel):
    """Schema for rejection summary"""
    rejection_code_id: Optional[int]
    rejection_code: Optional[str]
    total_rejected: Decimal
    count: int
    
    class Config:
        from_attributes = True
