"""
Material Consumption Log Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MaterialConsumption(Base):
    """
    Material Consumption Log
    Tracks material consumption with batch/heat/lot traceability
    """
    __tablename__ = "mes_execution_material_consumption"

    consumption_id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_id = Column(Integer, ForeignKey("mes_execution_work_order.work_order_id"), nullable=False)
    operation_execution_id = Column(Integer, ForeignKey("mes_execution_operation.operation_execution_id"), nullable=True)
    material_id = Column(Integer, nullable=True)  # FK to mes_config_material_master
    
    # Quantity tracking
    planned_quantity = Column(DECIMAL(15, 3), nullable=True)
    actual_quantity = Column(DECIMAL(15, 3), nullable=False)
    uom = Column(String(10), nullable=True)
    
    # Traceability
    batch_number = Column(String(100), nullable=True)
    heat_number = Column(String(100), nullable=True)
    lot_number = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    
    # Audit
    consumption_time = Column(TIMESTAMP, default=datetime.utcnow)
    entered_by = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="material_consumptions")
    operation_execution = relationship("OperationExecution", back_populates="material_consumptions")
    
    def __repr__(self):
        return f"<MaterialConsumption(id={self.consumption_id}, material={self.material_id}, qty={self.actual_quantity})>"
