# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 6: Quality Rejection & Defect Codes
Master data for rejection codes (CONFIGURATION - not actual rejection tracking)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class RejectionCodeCategory(Base, GovernanceMixin):
    """Rejection code categories"""
    
    __tablename__ = "mes_config_rejection_code_category"
    
    category_id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String(50), unique=True, nullable=False, index=True)
    category_name = Column(String(200), nullable=False)
    rejection_type = Column(String(50), nullable=False)  # MATERIAL, PRODUCTION
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    material_rejections = relationship("MaterialRejectionCode", back_populates="category")
    production_rejections = relationship("ProductionRejectionCode", back_populates="category")


class MaterialRejectionCode(Base, GovernanceMixin):
    """
    Material-specific rejection codes
    CONFIGURATION - defines possible rejection reasons, not actual rejections
    """
    
    __tablename__ = "mes_config_material_rejection_code"
    
    rejection_code_id = Column(Integer, primary_key=True, index=True)
    rejection_code = Column(String(50), unique=True, nullable=False, index=True)
    rejection_name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("mes_config_rejection_code_category.category_id"), nullable=False, index=True)
    
    # Material rejection specific attributes
    rejection_source = Column(String(100), nullable=True)  # INCOMING_INSPECTION, STORAGE_HANDLING, SUPPLIER_RELATED
    classification = Column(String(50), nullable=False)  # SCRAP, REWORK, DOWNGRADE, HOLD
    severity_level = Column(Integer, nullable=False, default=3)  # 1-5 scale
    cost_impact_indicator = Column(String(20), nullable=False, default="Medium")  # LOW, MEDIUM, HIGH
    
    root_cause_description = Column(String(1000), nullable=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    category = relationship("RejectionCodeCategory", back_populates="material_rejections")


class ProductionRejectionCode(Base, GovernanceMixin):
    """
    Production-specific rejection/defect codes
    CONFIGURATION - defines possible defect types, not actual defects
    """
    
    __tablename__ = "mes_config_production_rejection_code"
    
    rejection_code_id = Column(Integer, primary_key=True, index=True)
    rejection_code = Column(String(50), unique=True, nullable=False, index=True)
    rejection_name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("mes_config_rejection_code_category.category_id"), nullable=False, index=True)
    
    # Production defect specific attributes
    defect_type = Column(String(100), nullable=True)  # PROCESS, DIMENSIONAL, SURFACE, ASSEMBLY, OTHER
    defect_source = Column(String(100), nullable=True)  # OPERATOR, MACHINE, MATERIAL, METHOD, ENVIRONMENT (5M)
    classification = Column(String(50), nullable=False)  # SCRAP, REWORK, DOWNGRADE
    severity_level = Column(Integer, nullable=False, default=3)  # 1-5 scale
    cost_impact_indicator = Column(String(20), nullable=False, default="Medium")  # LOW, MEDIUM, HIGH
    
    corrective_action_required = Column(Integer, default=0, nullable=False)
    root_cause_description = Column(String(1000), nullable=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    category = relationship("RejectionCodeCategory", back_populates="production_rejections")
