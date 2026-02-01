"""
Production Log Model (Time-series)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProductionLog(Base):
    """
    Production Log (Time-series)
    Captures production data with timestamps for tracking
    """
    __tablename__ = "mes_execution_production_log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("mes_execution_work_order.work_order_id"), nullable=False)
    operation_execution_id = Column(Integer, ForeignKey("mes_execution_operation.operation_execution_id"), nullable=True)
    
    # Time-series data
    timestamp = Column(TIMESTAMP, nullable=False, index=True)
    produced_quantity = Column(DECIMAL(15, 3), nullable=True)
    scrap_quantity = Column(DECIMAL(15, 3), nullable=True)
    
    # Context information
    operator_name = Column(String(100), nullable=True)
    equipment_id = Column(Integer, nullable=True)  # FK to mes_config_equipment_master
    batch_number = Column(String(100), nullable=True)
    
    # Audit
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="production_logs")
    operation_execution = relationship("OperationExecution", back_populates="production_logs")
    
    __table_args__ = (
        Index('idx_production_log_timestamp', 'timestamp'),
        Index('idx_production_log_work_order', 'work_order_id'),
    )
    
    def __repr__(self):
        return f"<ProductionLog(id={self.log_id}, wo={self.work_order_id}, qty={self.produced_quantity})>"
