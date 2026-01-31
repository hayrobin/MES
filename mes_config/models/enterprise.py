# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Module 1: Enterprise & Organizational Configuration
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from mes_config.database import Base
from mes_config.models.governance import GovernanceMixin


class Enterprise(Base, GovernanceMixin):
    """Company master data"""
    
    __tablename__ = "mes_config_enterprise"
    
    enterprise_id = Column(Integer, primary_key=True, index=True)
    enterprise_code = Column(String(50), unique=True, nullable=False, index=True)
    enterprise_name = Column(String(200), nullable=False)
    erp_reference = Column(String(100), nullable=True)
    address = Column(String(500), nullable=True)
    contact_email = Column(String(200), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    sites = relationship("Site", back_populates="enterprise")


class Site(Base, GovernanceMixin):
    """Manufacturing sites/plants"""
    
    __tablename__ = "mes_config_site"
    
    site_id = Column(Integer, primary_key=True, index=True)
    site_code = Column(String(50), unique=True, nullable=False, index=True)
    site_name = Column(String(200), nullable=False)
    enterprise_id = Column(Integer, ForeignKey("mes_config_enterprise.enterprise_id"), nullable=False, index=True)
    erp_reference = Column(String(100), nullable=True)
    timezone = Column(String(50), nullable=True)
    location = Column(String(500), nullable=True)
    contact_name = Column(String(200), nullable=True)
    contact_email = Column(String(200), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    enterprise = relationship("Enterprise", back_populates="sites")
    areas = relationship("Area", back_populates="site")


class Area(Base, GovernanceMixin):
    """Production areas within sites"""
    
    __tablename__ = "mes_config_area"
    
    area_id = Column(Integer, primary_key=True, index=True)
    area_code = Column(String(50), unique=True, nullable=False, index=True)
    area_name = Column(String(200), nullable=False)
    site_id = Column(Integer, ForeignKey("mes_config_site.site_id"), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    site = relationship("Site", back_populates="areas")
    lines = relationship("Line", back_populates="area")


class Line(Base, GovernanceMixin):
    """Production lines within areas"""
    
    __tablename__ = "mes_config_line"
    
    line_id = Column(Integer, primary_key=True, index=True)
    line_code = Column(String(50), unique=True, nullable=False, index=True)
    line_name = Column(String(200), nullable=False)
    area_id = Column(Integer, ForeignKey("mes_config_area.area_id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("mes_config_site.site_id"), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    area = relationship("Area", back_populates="lines")
    site = relationship("Site")


class Department(Base, GovernanceMixin):
    """Organizational departments"""
    
    __tablename__ = "mes_config_department"
    
    department_id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(50), unique=True, nullable=False, index=True)
    department_name = Column(String(200), nullable=False)
    site_id = Column(Integer, ForeignKey("mes_config_site.site_id"), nullable=False, index=True)
    parent_department_id = Column(Integer, ForeignKey("mes_config_department.department_id"), nullable=True, index=True)
    manager_name = Column(String(200), nullable=True)
    cost_center = Column(String(50), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    site = relationship("Site")
    parent_department = relationship("Department", remote_side="Department.department_id")


class ShiftCalendar(Base, GovernanceMixin):
    """
    Shift definitions (CONFIGURATION ONLY - NO execution tracking)
    Defines shift templates, not actual shift instances
    """
    
    __tablename__ = "mes_config_shift_calendar"
    
    shift_id = Column(Integer, primary_key=True, index=True)
    shift_code = Column(String(50), unique=True, nullable=False, index=True)
    shift_name = Column(String(100), nullable=False)
    site_id = Column(Integer, ForeignKey("mes_config_site.site_id"), nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    days_of_week = Column(String(50), nullable=False)  # e.g., "MON,TUE,WED,THU,FRI"
    description = Column(String(500), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    # Relationships
    site = relationship("Site")


class UnitOfMeasure(Base, GovernanceMixin):
    """Unit of measure master data"""
    
    __tablename__ = "mes_config_unit_of_measure"
    
    uom_id = Column(Integer, primary_key=True, index=True)
    uom_code = Column(String(20), unique=True, nullable=False, index=True)
    uom_name = Column(String(100), nullable=False)
    uom_type = Column(String(50), nullable=False)  # e.g., WEIGHT, LENGTH, VOLUME, QUANTITY, TIME
    conversion_factor = Column(String(20), nullable=True)  # Conversion to base unit
    base_uom_code = Column(String(20), nullable=True)  # Reference to base unit
    is_active = Column(Integer, default=1, nullable=False)
