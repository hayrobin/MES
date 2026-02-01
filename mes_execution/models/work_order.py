"""
Work Order Execution State Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class WorkOrder(Base):
    """
    Work Order Execution State
    Tracks the execution of production work orders on the shop floor
    """
    __tablename__ = "mes_execution_work_order"

    work_order_id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_no = Column(String(50), unique=True, nullable=False, index=True)
    
    # References to configuration (Layer 2)
    product_id = Column(Integer, nullable=True)  # FK to mes_config_product_master
    equipment_id = Column(Integer, nullable=True)  # FK to mes_config_equipment_master
    line_id = Column(Integer, nullable=True)  # FK to mes_config_line
    
    # Production quantities
    target_quantity = Column(DECIMAL(15, 3), nullable=False)
    produced_quantity = Column(DECIMAL(15, 3), default=0)
    scrap_quantity = Column(DECIMAL(15, 3), default=0)
    rejected_quantity = Column(DECIMAL(15, 3), default=0)
    
    # Status tracking
    status = Column(
        String(20),
        nullable=False,
        default='PLANNED'
    )
    priority = Column(Integer, default=0)
    
    # Timing
    planned_start_time = Column(TIMESTAMP, nullable=True)
    planned_end_time = Column(TIMESTAMP, nullable=True)
    actual_start_time = Column(TIMESTAMP, nullable=True)
    actual_end_time = Column(TIMESTAMP, nullable=True)
    
    # Shift and ERP integration
    shift_id = Column(Integer, nullable=True)  # FK to mes_config_shift_calendar
    erp_order_ref = Column(String(100), nullable=True)
    
    # Audit fields
    created_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    operations = relationship("OperationExecution", back_populates="work_order", cascade="all, delete-orphan")
    production_logs = relationship("ProductionLog", back_populates="work_order", cascade="all, delete-orphan")
    material_consumptions = relationship("MaterialConsumption", back_populates="work_order", cascade="all, delete-orphan")
    quality_inspections = relationship("QualityInspection", back_populates="work_order", cascade="all, delete-orphan")
    equipment_states = relationship("EquipmentState", back_populates="work_order")
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('PLANNED', 'RUNNING', 'PAUSED', 'COMPLETED', 'CANCELLED')",
            name="chk_work_order_status"
        ),
    )
    
    def __repr__(self):
        return f"<WorkOrder(id={self.work_order_id}, no={self.work_order_no}, status={self.status})>"
