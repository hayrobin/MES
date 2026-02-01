"""
Equipment State Tracking Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Text, CheckConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class EquipmentState(Base):
    """
    Equipment State Tracking
    Tracks equipment states for availability and OEE calculation
    """
    __tablename__ = "mes_execution_equipment_state"

    state_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, nullable=False, index=True)  # FK to mes_config_equipment_master
    
    # State tracking
    state = Column(String(20), nullable=False)
    state_start_time = Column(TIMESTAMP, nullable=False, index=True)
    state_end_time = Column(TIMESTAMP, nullable=True)
    duration_minutes = Column(DECIMAL(10, 2), nullable=True)
    
    # Reason tracking
    reason_code = Column(String(50), nullable=True)
    reason_description = Column(Text, nullable=True)
    
    # Context
    work_order_id = Column(Integer, ForeignKey("mes_execution_work_order.work_order_id"), nullable=True)
    operator_name = Column(String(100), nullable=True)
    
    # Audit
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="equipment_states")
    
    __table_args__ = (
        CheckConstraint(
            "state IN ('RUNNING', 'IDLE', 'DOWN', 'SETUP', 'MAINTENANCE')",
            name="chk_equipment_state"
        ),
        Index('idx_equipment_state_equipment', 'equipment_id'),
        Index('idx_equipment_state_start_time', 'state_start_time'),
    )
    
    def __repr__(self):
        return f"<EquipmentState(id={self.state_id}, equipment={self.equipment_id}, state={self.state})>"
