"""
AI Assistant Service
Natural language query processing for production data
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..models.work_order import WorkOrder
from ..models.equipment_state import EquipmentState


class AIAssistant:
    """
    AI Assistant for production queries
    Provides natural language interface to production data
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def process_query(self, query: str, user_role: str = "OPERATOR") -> Dict:
        """
        Process natural language query and return results
        
        Args:
            query: Natural language query
            user_role: User role for filtering data
        
        Returns:
            Dictionary with response and data
        """
        # Input validation and sanitization
        if not query or not isinstance(query, str):
            return {
                "response": "Invalid query provided.",
                "data": None
            }
        
        # Limit query length to prevent resource exhaustion
        MAX_QUERY_LENGTH = 500
        if len(query) > MAX_QUERY_LENGTH:
            return {
                "response": f"Query too long. Maximum length is {MAX_QUERY_LENGTH} characters.",
                "data": None
            }
        
        # Basic sanitization - strip whitespace and convert to lowercase for comparison
        query_lower = query.strip().lower()
        
        # Intent detection
        if "running" in query_lower or "in progress" in query_lower:
            return self._query_running_orders()
        elif "delayed" in query_lower:
            return self._query_delayed_orders()
        elif "oee" in query_lower or "efficiency" in query_lower:
            return self._query_oee()
        elif "completed" in query_lower or "finished" in query_lower:
            return self._query_completed_orders()
        else:
            return {
                "response": "I can help you with: running orders, delayed orders, OEE metrics, and completed orders.",
                "data": None
            }
    
    def _query_running_orders(self) -> Dict:
        """Get currently running work orders"""
        running_orders = self.db.query(WorkOrder).filter(
            WorkOrder.status == 'RUNNING'
        ).all()
        
        if not running_orders:
            return {
                "response": "No work orders are currently running.",
                "data": []
            }
        
        orders_info = []
        for order in running_orders:
            completion = 0
            if order.target_quantity > 0:
                completion = float((order.produced_quantity / order.target_quantity) * 100)
            
            orders_info.append({
                "work_order_no": order.work_order_no,
                "status": order.status,
                "produced": float(order.produced_quantity),
                "target": float(order.target_quantity),
                "completion": round(completion, 2)
            })
        
        response = f"Found {len(running_orders)} running work order(s):"
        for info in orders_info:
            response += f"\n- {info['work_order_no']}: {info['completion']}% complete ({info['produced']}/{info['target']})"
        
        return {
            "response": response,
            "data": orders_info
        }
    
    def _query_delayed_orders(self) -> Dict:
        """Get delayed work orders"""
        now = datetime.utcnow()
        
        delayed_orders = self.db.query(WorkOrder).filter(
            WorkOrder.planned_end_time < now,
            WorkOrder.status.in_(['RUNNING', 'PAUSED', 'PLANNED'])
        ).all()
        
        if not delayed_orders:
            return {
                "response": "No delayed work orders found.",
                "data": []
            }
        
        orders_info = []
        for order in delayed_orders:
            delay = (now - order.planned_end_time).total_seconds() / 3600  # hours
            
            orders_info.append({
                "work_order_no": order.work_order_no,
                "status": order.status,
                "delay_hours": round(delay, 2),
                "planned_end": order.planned_end_time.isoformat() if order.planned_end_time else None
            })
        
        response = f"Found {len(delayed_orders)} delayed work order(s):"
        for info in orders_info:
            response += f"\n- {info['work_order_no']}: {info['delay_hours']} hours delayed"
        
        return {
            "response": response,
            "data": orders_info
        }
    
    def _query_oee(self) -> Dict:
        """Get today's OEE summary"""
        # This is a placeholder - real implementation would call OEE calculator
        return {
            "response": "OEE query requires equipment ID and time period. Please specify: 'Show OEE for equipment X today'",
            "data": None
        }
    
    def _query_completed_orders(self) -> Dict:
        """Get today's completed orders"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        completed_orders = self.db.query(WorkOrder).filter(
            WorkOrder.status == 'COMPLETED',
            WorkOrder.actual_end_time >= today_start
        ).all()
        
        if not completed_orders:
            return {
                "response": "No work orders completed today.",
                "data": []
            }
        
        orders_info = []
        for order in completed_orders:
            orders_info.append({
                "work_order_no": order.work_order_no,
                "produced": float(order.produced_quantity),
                "target": float(order.target_quantity),
                "completed_at": order.actual_end_time.isoformat() if order.actual_end_time else None
            })
        
        response = f"Found {len(completed_orders)} completed work order(s) today:"
        for info in orders_info:
            response += f"\n- {info['work_order_no']}: {info['produced']}/{info['target']} units"
        
        return {
            "response": response,
            "data": orders_info
        }
