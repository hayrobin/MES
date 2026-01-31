# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 3: Material Master
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class MaterialCategory(Base, GovernanceMixin):
    """Material categories with hierarchical support"""
    
    __tablename__ = "mes_config_material_category"
    
    category_id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String(50), unique=True, nullable=False, index=True)
    category_name = Column(String(200), nullable=False)
    parent_category_id = Column(Integer, ForeignKey("mes_config_material_category.category_id"), nullable=True, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    parent_category = relationship("MaterialCategory", remote_side="MaterialCategory.category_id")
    materials = relationship("MaterialMaster", back_populates="category")


class MaterialMaster(Base, GovernanceMixin):
    """
    All materials master data
    Includes raw materials, semi-finished, finished goods, consumables
    """
    
    __tablename__ = "mes_config_material_master"
    
    material_id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String(50), unique=True, nullable=False, index=True)
    material_name = Column(String(200), nullable=False)
    material_category_id = Column(Integer, ForeignKey("mes_config_material_category.category_id"), nullable=False, index=True)
    material_type = Column(String(50), nullable=False)  # RAW, SEMI_FINISHED, FINISHED_GOOD, CONSUMABLE
    
    # Unit of measure
    base_uom = Column(String(20), nullable=False)
    
    # Tracking requirements (CONFIGURATION - defines what to track, not actual tracking)
    batch_tracking_required = Column(Integer, default=0, nullable=False)
    lot_tracking_required = Column(Integer, default=0, nullable=False)
    serial_tracking_required = Column(Integer, default=0, nullable=False)
    
    # Shelf life configuration
    shelf_life_days = Column(Integer, nullable=True)
    expiry_tracking_required = Column(Integer, default=0, nullable=False)
    
    # ERP integration references
    erp_material_code = Column(String(100), nullable=True, index=True)
    supplier_reference = Column(String(100), nullable=True)
    cost_center = Column(String(50), nullable=True)
    
    # Additional attributes
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    category = relationship("MaterialCategory", back_populates="materials")
