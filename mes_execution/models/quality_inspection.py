"""
Quality Inspection & Rejection Log Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Text, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class QualityInspection(Base):
    """
    Quality Inspection & Rejection Log
    Tracks quality inspections and rejection data
    """
    __tablename__ = "mes_execution_quality_inspection"

    inspection_id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("mes_execution_work_order.work_order_id"), nullable=False)
    operation_execution_id = Column(Integer, ForeignKey("mes_execution_operation.operation_execution_id"), nullable=True)
    
    # Inspection details
    inspection_time = Column(TIMESTAMP, nullable=False)
    inspection_result = Column(String(20), nullable=False)
    
    # Rejection details
    rejection_code_id = Column(Integer, nullable=True)  # FK to mes_config_rejection_code
    rejected_quantity = Column(DECIMAL(15, 3), nullable=True)
    
    # Inspector tracking
    inspector_name = Column(String(100), nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Audit
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="quality_inspections")
    operation_execution = relationship("OperationExecution", back_populates="quality_inspections")
    
    __table_args__ = (
        CheckConstraint(
            "inspection_result IN ('PASS', 'FAIL')",
            name="chk_inspection_result"
        ),
    )
    
    def __repr__(self):
        return f"<QualityInspection(id={self.inspection_id}, result={self.inspection_result}, rejected={self.rejected_quantity})>"
