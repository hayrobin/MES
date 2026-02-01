"""
Work Order Service
Business logic for work order execution
"""

from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.work_order import WorkOrder
from ..models.operation import OperationExecution
from ..schemas.work_order import WorkOrderCreate, WorkOrderUpdate


class WorkOrderService:
    """Service for managing work order execution"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_work_order(self, work_order_data: WorkOrderCreate) -> WorkOrder:
        """Create a new work order"""
        work_order = WorkOrder(
            work_order_no=work_order_data.work_order_no,
            product_id=work_order_data.product_id,
            equipment_id=work_order_data.equipment_id,
            line_id=work_order_data.line_id,
            target_quantity=work_order_data.target_quantity,
            priority=work_order_data.priority,
            planned_start_time=work_order_data.planned_start_time,
            planned_end_time=work_order_data.planned_end_time,
            shift_id=work_order_data.shift_id,
            erp_order_ref=work_order_data.erp_order_ref,
            created_by=work_order_data.created_by,
            status='PLANNED'
        )
        
        self.db.add(work_order)
        self.db.commit()
        self.db.refresh(work_order)
        
        return work_order
    
    def get_work_order(self, work_order_id: int) -> Optional[WorkOrder]:
        """Get work order by ID"""
        return self.db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
    
    def get_work_order_by_no(self, work_order_no: str) -> Optional[WorkOrder]:
        """Get work order by work order number"""
        return self.db.query(WorkOrder).filter(
            WorkOrder.work_order_no == work_order_no
        ).first()
    
    def list_work_orders(
        self,
        status: Optional[str] = None,
        line_id: Optional[int] = None,
        equipment_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkOrder]:
        """List work orders with optional filters"""
        query = self.db.query(WorkOrder)
        
        if status:
            query = query.filter(WorkOrder.status == status)
        if line_id:
            query = query.filter(WorkOrder.line_id == line_id)
        if equipment_id:
            query = query.filter(WorkOrder.equipment_id == equipment_id)
        
        query = query.order_by(WorkOrder.priority.desc(), WorkOrder.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def start_work_order(self, work_order_id: int, operator_name: Optional[str] = None) -> WorkOrder:
        """Start a work order"""
        work_order = self.get_work_order(work_order_id)
        
        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")
        
        if work_order.status not in ['PLANNED', 'PAUSED']:
            raise ValueError(f"Cannot start work order in {work_order.status} status")
        
        work_order.status = 'RUNNING'
        
        if not work_order.actual_start_time:
            work_order.actual_start_time = datetime.utcnow()
        
        work_order.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(work_order)
        
        return work_order
    
    def pause_work_order(self, work_order_id: int) -> WorkOrder:
        """Pause a running work order"""
        work_order = self.get_work_order(work_order_id)
        
        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")
        
        if work_order.status != 'RUNNING':
            raise ValueError(f"Cannot pause work order in {work_order.status} status")
        
        work_order.status = 'PAUSED'
        work_order.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(work_order)
        
        return work_order
    
    def complete_work_order(self, work_order_id: int) -> WorkOrder:
        """Complete a work order"""
        work_order = self.get_work_order(work_order_id)
        
        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")
        
        if work_order.status not in ['RUNNING', 'PAUSED']:
            raise ValueError(f"Cannot complete work order in {work_order.status} status")
        
        work_order.status = 'COMPLETED'
        work_order.actual_end_time = datetime.utcnow()
        work_order.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(work_order)
        
        return work_order
    
    def update_work_order(self, work_order_id: int, update_data: WorkOrderUpdate) -> WorkOrder:
        """Update work order details"""
        work_order = self.get_work_order(work_order_id)
        
        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(work_order, field, value)
        
        work_order.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(work_order)
        
        return work_order
    
    def start_operation(
        self,
        operation_execution_id: int,
        operator_name: Optional[str] = None
    ) -> OperationExecution:
        """Start an operation"""
        operation = self.db.query(OperationExecution).filter(
            OperationExecution.operation_execution_id == operation_execution_id
        ).first()
        
        if not operation:
            raise ValueError(f"Operation {operation_execution_id} not found")
        
        if operation.status != 'PENDING':
            raise ValueError(f"Cannot start operation in {operation.status} status")
        
        operation.status = 'IN_PROGRESS'
        operation.start_time = datetime.utcnow()
        
        if operator_name:
            operation.operator_name = operator_name
        
        self.db.commit()
        self.db.refresh(operation)
        
        return operation
    
    def complete_operation(
        self,
        operation_execution_id: int,
        produced_quantity: Optional[Decimal] = None,
        scrap_quantity: Optional[Decimal] = None
    ) -> OperationExecution:
        """Complete an operation"""
        operation = self.db.query(OperationExecution).filter(
            OperationExecution.operation_execution_id == operation_execution_id
        ).first()
        
        if not operation:
            raise ValueError(f"Operation {operation_execution_id} not found")
        
        if operation.status != 'IN_PROGRESS':
            raise ValueError(f"Cannot complete operation in {operation.status} status")
        
        operation.status = 'COMPLETED'
        operation.end_time = datetime.utcnow()
        
        if operation.start_time:
            duration = (operation.end_time - operation.start_time).total_seconds() / 60
            operation.duration_minutes = Decimal(str(duration))
        
        if produced_quantity is not None:
            operation.produced_quantity = produced_quantity
        
        if scrap_quantity is not None:
            operation.scrap_quantity = scrap_quantity
        
        # Update work order totals
        if operation.work_order:
            self._update_work_order_quantities(operation.work_order_id)
        
        self.db.commit()
        self.db.refresh(operation)
        
        return operation
    
    def _update_work_order_quantities(self, work_order_id: int):
        """Update work order total quantities from operations"""
        work_order = self.get_work_order(work_order_id)
        
        if not work_order:
            return
        
        from sqlalchemy import func
        
        # Sum up quantities from all completed operations
        totals = self.db.query(
            func.sum(OperationExecution.produced_quantity).label('total_produced'),
            func.sum(OperationExecution.scrap_quantity).label('total_scrap')
        ).filter(
            OperationExecution.work_order_id == work_order_id,
            OperationExecution.status == 'COMPLETED'
        ).first()
        
        if totals:
            work_order.produced_quantity = totals.total_produced or Decimal('0')
            work_order.scrap_quantity = totals.total_scrap or Decimal('0')
            work_order.updated_at = datetime.utcnow()
