"""
Material Consumption Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class MaterialConsumptionCreate(BaseModel):
    """Schema for creating a material consumption record"""
    work_order_id: int = Field(..., description="Work order ID")
    operation_execution_id: Optional[int] = Field(None, description="Operation execution ID")
    material_id: Optional[int] = Field(None, description="Material ID from master data")
    planned_quantity: Optional[Decimal] = Field(None, description="Planned quantity")
    actual_quantity: Decimal = Field(..., description="Actual consumed quantity")
    uom: Optional[str] = Field(None, description="Unit of measure")
    batch_number: Optional[str] = Field(None, description="Batch number for traceability")
    heat_number: Optional[str] = Field(None, description="Heat number for traceability")
    lot_number: Optional[str] = Field(None, description="Lot number for traceability")
    serial_number: Optional[str] = Field(None, description="Serial number for traceability")
    entered_by: Optional[str] = Field(None, description="User who entered the data")


class MaterialConsumptionResponse(MaterialConsumptionCreate):
    """Schema for material consumption response"""
    consumption_id: int
    consumption_time: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
