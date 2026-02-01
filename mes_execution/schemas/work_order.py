"""
Work Order Schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


class WorkOrderBase(BaseModel):
    """Base schema for Work Order"""
    work_order_no: str = Field(..., description="Unique work order number")
    product_id: Optional[int] = Field(None, description="Product ID from master data")
    equipment_id: Optional[int] = Field(None, description="Equipment ID")
    line_id: Optional[int] = Field(None, description="Line ID")
    target_quantity: Decimal = Field(..., description="Target production quantity")
    priority: int = Field(0, description="Priority level")
    planned_start_time: Optional[datetime] = None
    planned_end_time: Optional[datetime] = None
    shift_id: Optional[int] = None
    erp_order_ref: Optional[str] = None


class WorkOrderCreate(WorkOrderBase):
    """Schema for creating a new work order"""
    created_by: Optional[str] = None


class WorkOrderUpdate(BaseModel):
    """Schema for updating a work order"""
    target_quantity: Optional[Decimal] = None
    status: Optional[str] = None
    produced_quantity: Optional[Decimal] = None
    scrap_quantity: Optional[Decimal] = None
    rejected_quantity: Optional[Decimal] = None
    priority: Optional[int] = None


class OperationExecutionResponse(BaseModel):
    """Schema for operation execution response"""
    operation_execution_id: int
    operation_sequence: int
    operation_name: Optional[str]
    status: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    duration_minutes: Optional[Decimal]
    produced_quantity: Optional[Decimal]
    scrap_quantity: Optional[Decimal]
    operator_name: Optional[str]
    
    class Config:
        from_attributes = True


class WorkOrderResponse(WorkOrderBase):
    """Schema for work order response"""
    work_order_id: int
    status: str
    produced_quantity: Decimal
    scrap_quantity: Decimal
    rejected_quantity: Decimal
    actual_start_time: Optional[datetime]
    actual_end_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkOrderWithOperations(WorkOrderResponse):
    """Schema for work order with operations"""
    operations: List[OperationExecutionResponse] = []
    
    class Config:
        from_attributes = True
