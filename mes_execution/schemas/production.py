"""
Production Log Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ProductionLogCreate(BaseModel):
    """Schema for creating a production log entry"""
    work_order_id: int = Field(..., description="Work order ID")
    operation_execution_id: Optional[int] = Field(None, description="Operation execution ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Production timestamp")
    produced_quantity: Optional[Decimal] = Field(None, description="Produced quantity")
    scrap_quantity: Optional[Decimal] = Field(None, description="Scrap quantity")
    operator_name: Optional[str] = Field(None, description="Operator name")
    equipment_id: Optional[int] = Field(None, description="Equipment ID")
    batch_number: Optional[str] = Field(None, description="Batch number")


class ProductionLogResponse(ProductionLogCreate):
    """Schema for production log response"""
    log_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductionSummary(BaseModel):
    """Schema for production summary"""
    work_order_id: int
    work_order_no: str
    total_produced: Decimal
    total_scrap: Decimal
    total_rejected: Decimal
    target_quantity: Decimal
    completion_percentage: Decimal
    status: str
    
    class Config:
        from_attributes = True
