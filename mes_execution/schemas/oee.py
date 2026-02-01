"""
OEE (Overall Equipment Effectiveness) Schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


class OEEMetrics(BaseModel):
    """Schema for real-time OEE metrics"""
    equipment_id: int
    period_start: datetime
    period_end: datetime
    availability: Decimal = Field(..., description="Availability percentage")
    performance: Decimal = Field(..., description="Performance percentage")
    quality: Decimal = Field(..., description="Quality percentage")
    oee: Decimal = Field(..., description="Overall OEE percentage")
    
    class Config:
        from_attributes = True


class OEESnapshot(OEEMetrics):
    """Schema for OEE snapshot (cached calculation)"""
    oee_id: int
    period_type: str
    planned_production_time: Optional[Decimal]
    actual_run_time: Optional[Decimal]
    downtime_minutes: Optional[Decimal]
    ideal_cycle_time: Optional[Decimal]
    total_pieces: Optional[int]
    good_pieces: Optional[int]
    rejected_pieces: Optional[int]
    calculated_at: datetime
    
    class Config:
        from_attributes = True


class DowntimeReason(BaseModel):
    """Schema for downtime reason breakdown"""
    reason_code: str
    reason_description: Optional[str]
    duration_minutes: Decimal
    percentage: Decimal


class OEEBreakdown(BaseModel):
    """Schema for detailed OEE breakdown"""
    equipment_id: int
    equipment_name: Optional[str]
    period_start: datetime
    period_end: datetime
    
    # OEE metrics
    availability: Decimal
    performance: Decimal
    quality: Decimal
    oee: Decimal
    
    # Breakdown data
    planned_production_time: Decimal
    actual_run_time: Decimal
    downtime_minutes: Decimal
    downtime_reasons: List[DowntimeReason] = []
    
    total_pieces: int
    good_pieces: int
    rejected_pieces: int
    
    ideal_cycle_time: Decimal
    actual_cycle_time: Optional[Decimal]
