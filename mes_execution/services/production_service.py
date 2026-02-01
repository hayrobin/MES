"""
Production Service
Business logic for production tracking and logging
"""

from datetime import datetime
from typing import List, Optional, Dict
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.production_log import ProductionLog
from ..models.work_order import WorkOrder
from ..schemas.production import ProductionLogCreate


class ProductionService:
    """Service for managing production logging"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_production(self, production_data: ProductionLogCreate) -> ProductionLog:
        """Log production data"""
        production_log = ProductionLog(
            work_order_id=production_data.work_order_id,
            operation_execution_id=production_data.operation_execution_id,
            timestamp=production_data.timestamp,
            produced_quantity=production_data.produced_quantity,
            scrap_quantity=production_data.scrap_quantity,
            operator_name=production_data.operator_name,
            equipment_id=production_data.equipment_id,
            batch_number=production_data.batch_number,
        )
        
        self.db.add(production_log)
        self.db.commit()
        self.db.refresh(production_log)
        
        # Update work order quantities
        self._update_work_order_from_logs(production_data.work_order_id)
        
        return production_log
    
    def get_production_summary(self, work_order_id: int) -> Dict:
        """Get production summary for a work order"""
        work_order = self.db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")
        
        # Get totals from production logs
        totals = self.db.query(
            func.sum(ProductionLog.produced_quantity).label('total_produced'),
            func.sum(ProductionLog.scrap_quantity).label('total_scrap')
        ).filter(
            ProductionLog.work_order_id == work_order_id
        ).first()
        
        total_produced = totals.total_produced or Decimal('0')
        total_scrap = totals.total_scrap or Decimal('0')
        
        completion_percentage = Decimal('0')
        if work_order.target_quantity > 0:
            completion_percentage = (total_produced / work_order.target_quantity) * 100
        
        return {
            'work_order_id': work_order.work_order_id,
            'work_order_no': work_order.work_order_no,
            'total_produced': total_produced,
            'total_scrap': total_scrap,
            'total_rejected': work_order.rejected_quantity,
            'target_quantity': work_order.target_quantity,
            'completion_percentage': round(completion_percentage, 2),
            'status': work_order.status,
        }
    
    def get_production_logs(
        self,
        work_order_id: Optional[int] = None,
        equipment_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductionLog]:
        """Get production logs with filters"""
        query = self.db.query(ProductionLog)
        
        if work_order_id:
            query = query.filter(ProductionLog.work_order_id == work_order_id)
        if equipment_id:
            query = query.filter(ProductionLog.equipment_id == equipment_id)
        if start_time:
            query = query.filter(ProductionLog.timestamp >= start_time)
        if end_time:
            query = query.filter(ProductionLog.timestamp < end_time)
        
        query = query.order_by(ProductionLog.timestamp.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def _update_work_order_from_logs(self, work_order_id: int):
        """Update work order quantities from production logs"""
        totals = self.db.query(
            func.sum(ProductionLog.produced_quantity).label('total_produced'),
            func.sum(ProductionLog.scrap_quantity).label('total_scrap')
        ).filter(
            ProductionLog.work_order_id == work_order_id
        ).first()
        
        work_order = self.db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if work_order and totals:
            work_order.produced_quantity = totals.total_produced or Decimal('0')
            work_order.scrap_quantity = totals.total_scrap or Decimal('0')
            work_order.updated_at = datetime.utcnow()
            self.db.commit()
