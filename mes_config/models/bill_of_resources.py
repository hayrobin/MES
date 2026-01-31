# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 5: Bill of Resources (BoR)
Defines product manufacturing requirements - equipment, materials, tooling, quality checkpoints
CONFIGURATION ONLY - not execution tracking
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class BillOfResources(Base, GovernanceMixin):
    """
    Product → Equipment mapping with operation sequences
    Defines manufacturing routing (CONFIGURATION - not work orders)
    """
    
    __tablename__ = "mes_config_bill_of_resources"
    
    bor_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    equipment_id = Column(Integer, nullable=False, index=True)
    operation_sequence = Column(Integer, nullable=False)
    operation_name = Column(String(200), nullable=True)
    
    # Time standards (CONFIGURATION - not actual times)
    standard_time = Column(Integer, nullable=True)  # minutes
    setup_time = Column(Integer, nullable=True)  # minutes
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)


class BorMaterial(Base, GovernanceMixin):
    """
    Product → Material requirements
    Defines material consumption standards (CONFIGURATION - not actual consumption)
    """
    
    __tablename__ = "mes_config_bor_material"
    
    bor_material_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    material_id = Column(Integer, nullable=False, index=True)
    
    # Consumption standards
    standard_quantity = Column(Numeric(18, 4), nullable=False)
    uom = Column(String(20), nullable=False)
    scrap_factor = Column(Numeric(5, 2), nullable=True, default=0)  # percentage
    
    operation_sequence = Column(Integer, nullable=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)


class BorTooling(Base, GovernanceMixin):
    """
    Product → Tooling references
    Defines required tooling (CONFIGURATION - not tooling management)
    """
    
    __tablename__ = "mes_config_bor_tooling"
    
    bor_tooling_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    tooling_code = Column(String(50), nullable=False, index=True)
    tooling_name = Column(String(200), nullable=False)
    
    operation_sequence = Column(Integer, nullable=True)
    quantity_required = Column(Integer, nullable=True, default=1)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)


class BorQualityCheckpoint(Base, GovernanceMixin):
    """
    Product → Quality checkpoint definitions
    DEFINITION ONLY - NO execution data, NO actual inspection records
    Defines what checkpoints exist, not inspection results
    """
    
    __tablename__ = "mes_config_bor_quality_checkpoint"
    
    checkpoint_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    checkpoint_code = Column(String(50), nullable=False, index=True)
    checkpoint_name = Column(String(200), nullable=False)
    checkpoint_type = Column(String(50), nullable=False)  # INCOMING, IN_PROCESS, FINAL
    
    operation_sequence = Column(Integer, nullable=True)
    required = Column(Integer, default=1, nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
