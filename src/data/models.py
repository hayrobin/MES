"""Database models for MES data storage."""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, 
    ForeignKey, Index, Text, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Device(Base):
    """Device registry table."""
    
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    device_type = Column(String(50), nullable=False)  # opcua, modbus
    connection_string = Column(String(500), nullable=False)
    status = Column(String(20), default="disconnected")  # connected, disconnected, error
    last_seen = Column(DateTime, nullable=True)
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    data_points = relationship("DataPoint", back_populates="device", cascade="all, delete-orphan")
    realtime_data = relationship("RealtimeData", back_populates="device", cascade="all, delete-orphan")
    historical_data = relationship("HistoricalData", back_populates="device", cascade="all, delete-orphan")


class DataPoint(Base):
    """Data point registry table."""
    
    __tablename__ = "data_points"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    address = Column(String(500), nullable=False)  # node_id, register address, etc.
    data_type = Column(String(50), nullable=False)  # float, int, bool, string
    unit = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    writable = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    device = relationship("Device", back_populates="data_points")
    
    # Composite index for faster lookups
    __table_args__ = (
        Index('ix_device_name', 'device_id', 'name'),
    )


class RealtimeData(Base):
    """Real-time data table (latest values only)."""
    
    __tablename__ = "realtime_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    data_point_name = Column(String(200), nullable=False, index=True)
    value = Column(String(500), nullable=True)
    quality = Column(String(20), default="good")  # good, bad, uncertain
    timestamp = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    device = relationship("Device", back_populates="realtime_data")
    
    # Composite unique index - one row per device/data_point
    __table_args__ = (
        Index('ix_realtime_device_point', 'device_id', 'data_point_name', unique=True),
    )


class HistoricalData(Base):
    """Historical time-series data table."""
    
    __tablename__ = "historical_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    data_point_name = Column(String(200), nullable=False, index=True)
    value = Column(String(500), nullable=True)
    quality = Column(String(20), default="good")
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    device = relationship("Device", back_populates="historical_data")
    
    # Composite index for time-series queries
    __table_args__ = (
        Index('ix_historical_device_point_time', 'device_id', 'data_point_name', 'timestamp'),
    )


class ProductionEvent(Base):
    """Production events table."""
    
    __tablename__ = "production_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(100), nullable=False, index=True)  # start, stop, pause, resume
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True, index=True)
    product_id = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=True)
    event_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Alarm(Base):
    """Alarms and events table."""
    
    __tablename__ = "alarms"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True, index=True)
    severity = Column(String(20), nullable=False, index=True)  # info, warning, error, critical
    message = Column(Text, nullable=False)
    acknowledged = Column(Boolean, default=False, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(100), nullable=True)
    resolved = Column(Boolean, default=False, index=True)
    resolved_at = Column(DateTime, nullable=True)
    alarm_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
