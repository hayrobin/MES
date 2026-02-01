"""
OEE Calculation Cache Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, String, CheckConstraint, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OEESnapshot(Base):
    """
    OEE Calculation Cache
    Stores pre-calculated OEE metrics for different time periods
    """
    __tablename__ = "mes_execution_oee_snapshot"

    oee_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, nullable=False)  # FK to mes_config_equipment_master
    
    # Period definition
    period_start = Column(TIMESTAMP, nullable=False)
    period_end = Column(TIMESTAMP, nullable=False)
    period_type = Column(String(20), nullable=False)
    
    # OEE metrics (percentages)
    availability = Column(DECIMAL(5, 2), nullable=True)
    performance = Column(DECIMAL(5, 2), nullable=True)
    quality = Column(DECIMAL(5, 2), nullable=True)
    oee = Column(DECIMAL(5, 2), nullable=True)
    
    # Supporting data for OEE calculation
    planned_production_time = Column(DECIMAL(10, 2), nullable=True)
    actual_run_time = Column(DECIMAL(10, 2), nullable=True)
    downtime_minutes = Column(DECIMAL(10, 2), nullable=True)
    ideal_cycle_time = Column(DECIMAL(10, 4), nullable=True)
    total_pieces = Column(Integer, nullable=True)
    good_pieces = Column(Integer, nullable=True)
    rejected_pieces = Column(Integer, nullable=True)
    
    # Audit
    calculated_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint(
            "period_type IN ('SHIFT', 'HOUR', 'DAY')",
            name="chk_period_type"
        ),
        Index('idx_oee_equipment_period', 'equipment_id', 'period_start'),
    )
    
    def __repr__(self):
        return f"<OEESnapshot(id={self.oee_id}, equipment={self.equipment_id}, oee={self.oee}%)>"
