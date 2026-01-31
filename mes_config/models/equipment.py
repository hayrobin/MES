# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 2: Equipment & Capacity Definition
CRITICAL: NO live telemetry, NO OPC subscriptions, NO Modbus reads
Symbolic linkage fields only for future integration
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class EquipmentMaster(Base, GovernanceMixin):
    """
    Equipment hierarchy and master data
    Includes symbolic linkage fields for external systems (NO LIVE INTEGRATION)
    """
    
    __tablename__ = "mes_config_equipment_master"
    
    equipment_id = Column(Integer, primary_key=True, index=True)
    equipment_code = Column(String(50), unique=True, nullable=False, index=True)
    equipment_name = Column(String(200), nullable=False)
    equipment_type = Column(String(50), nullable=False)  # MACHINE, LINE, CELL, TOOL
    parent_equipment_id = Column(Integer, ForeignKey("mes_config_equipment_master.equipment_id"), nullable=True, index=True)
    
    # Location references
    site_id = Column(Integer, nullable=True, index=True)
    area_id = Column(Integer, nullable=True, index=True)
    line_id = Column(Integer, nullable=True, index=True)
    
    # Equipment details
    manufacturer = Column(String(200), nullable=True)
    model = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    installation_date = Column(String(20), nullable=True)  # ISO date string
    
    # Performance classification
    is_bottleneck = Column(Integer, default=0, nullable=False)
    criticality_level = Column(String(20), nullable=False, default="Medium")  # Low, Medium, High, Critical
    
    # Symbolic linkage fields (NO LIVE INTEGRATION)
    # These are STRING REFERENCES ONLY - not active connections
    external_asset_ref = Column(String(100), nullable=True, index=True)
    opc_namespace = Column(String(200), nullable=True)
    opc_node_id = Column(String(200), nullable=True)
    modbus_tag_ref = Column(String(100), nullable=True)
    scada_tag_ref = Column(String(100), nullable=True)
    
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    parent_equipment = relationship("EquipmentMaster", remote_side="EquipmentMaster.equipment_id")
    capacities = relationship("EquipmentCapacity", back_populates="equipment")


class EquipmentCapacity(Base, GovernanceMixin):
    """
    Equipment capacity configuration (RATED CAPACITY ONLY - NO live monitoring)
    Defines theoretical/design capacity, not actual performance
    """
    
    __tablename__ = "mes_config_equipment_capacity"
    
    capacity_id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("mes_config_equipment_master.equipment_id"), nullable=False, index=True)
    product_id = Column(Integer, nullable=True, index=True)  # Optional - default capacity if NULL
    
    # Capacity definition
    rated_capacity_value = Column(Numeric(18, 4), nullable=False)
    rated_capacity_uom = Column(String(50), nullable=False)  # units/hour, tons/hour, cycles/hour
    available_time_per_shift = Column(Integer, nullable=True)  # minutes
    setup_time = Column(Integer, nullable=True)  # minutes
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    equipment = relationship("EquipmentMaster", back_populates="capacities")
