# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Pydantic schemas for Module 2: Equipment & Capacity Definition
"""

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from .base import GovernanceBase, ResponseBase


# Equipment Master Schemas
class EquipmentMasterBase(BaseModel):
    equipment_code: str
    equipment_name: str
    equipment_type: str
    parent_equipment_id: Optional[int] = None
    site_id: Optional[int] = None
    area_id: Optional[int] = None
    line_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    installation_date: Optional[str] = None
    is_bottleneck: int = 0
    criticality_level: str = "Medium"
    external_asset_ref: Optional[str] = None
    opc_namespace: Optional[str] = None
    opc_node_id: Optional[str] = None
    modbus_tag_ref: Optional[str] = None
    scada_tag_ref: Optional[str] = None
    is_active: int = 1


class EquipmentMasterCreate(EquipmentMasterBase, GovernanceBase):
    pass


class EquipmentMasterUpdate(BaseModel):
    equipment_name: Optional[str] = None
    equipment_type: Optional[str] = None
    parent_equipment_id: Optional[int] = None
    site_id: Optional[int] = None
    area_id: Optional[int] = None
    line_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    installation_date: Optional[str] = None
    is_bottleneck: Optional[int] = None
    criticality_level: Optional[str] = None
    external_asset_ref: Optional[str] = None
    opc_namespace: Optional[str] = None
    opc_node_id: Optional[str] = None
    modbus_tag_ref: Optional[str] = None
    scada_tag_ref: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class EquipmentMasterResponse(EquipmentMasterBase, GovernanceBase, ResponseBase):
    equipment_id: int


# Equipment Capacity Schemas
class EquipmentCapacityBase(BaseModel):
    equipment_id: int
    product_id: Optional[int] = None
    rated_capacity_value: Decimal
    rated_capacity_uom: str
    available_time_per_shift: Optional[int] = None
    setup_time: Optional[int] = None
    description: Optional[str] = None
    is_active: int = 1


class EquipmentCapacityCreate(EquipmentCapacityBase, GovernanceBase):
    pass


class EquipmentCapacityUpdate(BaseModel):
    equipment_id: Optional[int] = None
    product_id: Optional[int] = None
    rated_capacity_value: Optional[Decimal] = None
    rated_capacity_uom: Optional[str] = None
    available_time_per_shift: Optional[int] = None
    setup_time: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    updated_by: Optional[str] = None


class EquipmentCapacityResponse(EquipmentCapacityBase, GovernanceBase, ResponseBase):
    capacity_id: int
