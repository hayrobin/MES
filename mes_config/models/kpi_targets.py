# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 7: OEE Targets & KPI Configuration
TARGET CONFIGURATION ONLY - NO actual KPI calculations or monitoring
Defines what to measure and target values, not the measurements themselves
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class OeeTarget(Base, GovernanceMixin):
    """
    OEE targets by product/line/machine/site
    CONFIGURATION - defines target values, not actual OEE measurements
    """
    
    __tablename__ = "mes_config_oee_target"
    
    target_id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String(50), nullable=False, index=True)  # PRODUCT, LINE, MACHINE, SITE
    
    # Target scope (nullable - depends on target_type)
    product_id = Column(Integer, nullable=True, index=True)
    line_id = Column(Integer, nullable=True, index=True)
    equipment_id = Column(Integer, nullable=True, index=True)
    site_id = Column(Integer, nullable=True, index=True)
    
    # OEE component targets (percentages as decimals, e.g., 85.5 = 85.5%)
    availability_target = Column(Numeric(5, 2), nullable=False)  # Target availability %
    performance_target = Column(Numeric(5, 2), nullable=False)  # Target performance %
    quality_target = Column(Numeric(5, 2), nullable=False)  # Target quality %
    oee_target = Column(Numeric(5, 2), nullable=False)  # Overall OEE target % (calculated from above)
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)


class KpiDefinition(Base, GovernanceMixin):
    """
    KPI definitions and thresholds
    CONFIGURATION ONLY - NO actual calculations
    Defines KPI metadata, formulas (as text), and target/threshold values
    """
    
    __tablename__ = "mes_config_kpi_definition"
    
    kpi_id = Column(Integer, primary_key=True, index=True)
    kpi_code = Column(String(50), unique=True, nullable=False, index=True)
    kpi_name = Column(String(200), nullable=False)
    
    # KPI classification
    kpi_category = Column(String(50), nullable=False)  # QUALITY, PRODUCTIVITY, EFFICIENCY, COST
    kpi_type = Column(String(100), nullable=False)  # YIELD, SCRAP_RATE, REWORK_RATE, THROUGHPUT, CAPACITY_UTILIZATION, OEE, DOWNTIME
    
    # Target and thresholds
    unit_of_measure = Column(String(50), nullable=True)
    target_value = Column(Numeric(18, 4), nullable=True)
    warning_threshold = Column(Numeric(18, 4), nullable=True)
    critical_threshold = Column(Numeric(18, 4), nullable=True)
    
    # Formula as documentation (TEXT - not executable code)
    calculation_formula_description = Column(Text, nullable=True)
    
    # Additional metadata
    aggregation_level = Column(String(50), nullable=True)  # PRODUCT, LINE, SITE, ENTERPRISE
    measurement_frequency = Column(String(50), nullable=True)  # HOURLY, SHIFT, DAILY, WEEKLY
    
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
