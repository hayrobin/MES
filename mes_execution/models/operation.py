"""
Operation Execution Log Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class OperationExecution(Base):
    """
    Operation Execution Log
    Tracks individual operations within a work order execution
    """
    __tablename__ = "mes_execution_operation"

    operation_execution_id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("mes_execution_work_order.work_order_id"), nullable=False)
    operation_id = Column(Integer, nullable=True)  # FK to mes_config_bor_operation
    
    # Operation details
    operation_sequence = Column(Integer, nullable=False)
    operation_name = Column(String(200), nullable=True)
    
    # Status tracking
    status = Column(
        String(20),
        nullable=False,
        default='PENDING'
    )
    
    # Timing
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    duration_minutes = Column(DECIMAL(10, 2), nullable=True)
    
    # Production tracking
    produced_quantity = Column(DECIMAL(15, 3), nullable=True)
    scrap_quantity = Column(DECIMAL(15, 3), nullable=True)
    
    # Operator tracking
    operator_name = Column(String(100), nullable=True)
    operator_id = Column(String(50), nullable=True)
    
    # Audit
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="operations")
    production_logs = relationship("ProductionLog", back_populates="operation_execution", cascade="all, delete-orphan")
    material_consumptions = relationship("MaterialConsumption", back_populates="operation_execution")
    quality_inspections = relationship("QualityInspection", back_populates="operation_execution")
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'SKIPPED')",
            name="chk_operation_status"
        ),
    )
    
    def __repr__(self):
        return f"<OperationExecution(id={self.operation_execution_id}, seq={self.operation_sequence}, status={self.status})>"
