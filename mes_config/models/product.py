# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 4: Product & Production Definitions
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class ProductFamily(Base, GovernanceMixin):
    """Product families/grades for grouping products"""
    
    __tablename__ = "mes_config_product_family"
    
    family_id = Column(Integer, primary_key=True, index=True)
    family_code = Column(String(50), unique=True, nullable=False, index=True)
    family_name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    products = relationship("ProductMaster", back_populates="family")


class ProductMaster(Base, GovernanceMixin):
    """Finished products master data"""
    
    __tablename__ = "mes_config_product_master"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    product_family_id = Column(Integer, ForeignKey("mes_config_product_family.family_id"), nullable=True, index=True)
    
    # Production standards (CONFIGURATION - not live tracking)
    standard_cycle_time = Column(Integer, nullable=True)  # seconds/unit
    standard_output_rate = Column(Numeric(18, 4), nullable=True)  # units/hour
    
    # Unit of measure
    base_uom = Column(String(20), nullable=False)
    
    # ERP integration
    erp_product_code = Column(String(100), nullable=True, index=True)
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    family = relationship("ProductFamily", back_populates="products")
    equipment_compatibility = relationship("ProductEquipmentCompatibility", back_populates="product")


class ProductEquipmentCompatibility(Base, GovernanceMixin):
    """
    Product-Equipment mapping
    Defines which products can be produced on which equipment
    CONFIGURATION ONLY - not production scheduling
    """
    
    __tablename__ = "mes_config_product_equipment_compatibility"
    
    compatibility_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("mes_config_product_master.product_id"), nullable=False, index=True)
    equipment_id = Column(Integer, nullable=False, index=True)
    
    # Compatibility attributes
    is_preferred_equipment = Column(Integer, default=0, nullable=False)
    setup_time = Column(Integer, nullable=True)  # minutes
    capacity_constraint = Column(Numeric(18, 4), nullable=True)  # max units/hour on this equipment
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    product = relationship("ProductMaster", back_populates="equipment_compatibility")
