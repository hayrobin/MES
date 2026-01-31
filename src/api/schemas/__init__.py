"""API request/response schemas."""

from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


# Device schemas
class DeviceCreate(BaseModel):
    """Schema for creating a device."""
    
    name: str
    device_type: str
    connection_string: str
    config: Optional[Dict[str, Any]] = None


class DeviceResponse(BaseModel):
    """Schema for device response."""
    
    id: int
    name: str
    device_type: str
    connection_string: str
    status: str
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Data point schemas
class DataPointCreate(BaseModel):
    """Schema for creating a data point."""
    
    device_id: int
    name: str
    address: str
    data_type: str
    unit: Optional[str] = None
    description: Optional[str] = None
    writable: bool = False


class DataPointResponse(BaseModel):
    """Schema for data point response."""
    
    id: int
    device_id: int
    name: str
    address: str
    data_type: str
    unit: Optional[str] = None
    description: Optional[str] = None
    writable: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Real-time data schemas
class RealtimeDataResponse(BaseModel):
    """Schema for real-time data response."""
    
    device_id: int
    data_point_name: str
    value: Optional[str]
    quality: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Historical data schemas
class HistoricalDataQuery(BaseModel):
    """Schema for historical data query."""
    
    device_id: int
    data_point_name: str
    start_time: datetime
    end_time: datetime


class HistoricalDataResponse(BaseModel):
    """Schema for historical data response."""
    
    device_id: int
    data_point_name: str
    value: Optional[str]
    quality: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


# OPC UA schemas
class OPCUABrowseRequest(BaseModel):
    """Schema for OPC UA browse request."""
    
    client_name: str
    node_id: Optional[str] = None


class OPCUANodeInfo(BaseModel):
    """Schema for OPC UA node information."""
    
    node_id: str
    browse_name: str
    display_name: str
    node_class: str


class OPCUAReadRequest(BaseModel):
    """Schema for OPC UA read request."""
    
    client_name: str
    node_id: str


class OPCUAWriteRequest(BaseModel):
    """Schema for OPC UA write request."""
    
    client_name: str
    node_id: str
    value: Any


# Modbus schemas
class ModbusReadRequest(BaseModel):
    """Schema for Modbus read request."""
    
    device_name: str
    register_name: str


class ModbusWriteRequest(BaseModel):
    """Schema for Modbus write request."""
    
    device_name: str
    register_name: str
    value: Any


# System status schemas
class DeviceStatus(BaseModel):
    """Schema for device status."""
    
    name: str
    type: str
    status: str
    last_seen: Optional[datetime] = None


class SystemStatus(BaseModel):
    """Schema for system status."""
    
    status: str
    uptime: float
    devices: List[DeviceStatus]
    database_connected: bool


# Production schemas
class ProductionMetrics(BaseModel):
    """Schema for production metrics."""
    
    total_events: int
    production_running: bool
    current_product_id: Optional[str] = None
    total_quantity: int
    
    
# Alarm schemas
class AlarmResponse(BaseModel):
    """Schema for alarm response."""
    
    id: int
    device_id: Optional[int]
    severity: str
    message: str
    acknowledged: bool
    resolved: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True
