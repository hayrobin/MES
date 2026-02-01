"""
Quality Inspection API Endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models.quality_inspection import QualityInspection
from ..schemas.quality import (
    QualityInspectionCreate,
    QualityInspectionResponse,
    RejectionSummary,
)

router = APIRouter(prefix="/api/v1/execution/quality", tags=["quality"])


@router.post("/inspect", response_model=QualityInspectionResponse, status_code=201)
def record_quality_inspection(
    inspection_data: QualityInspectionCreate,
    db: Session = Depends(get_db)
):
    """
    Record quality inspection/rejection
    """
    inspection = QualityInspection(
        work_order_id=inspection_data.work_order_id,
        operation_execution_id=inspection_data.operation_execution_id,
        inspection_time=inspection_data.inspection_time,
        inspection_result=inspection_data.inspection_result,
        rejection_code_id=inspection_data.rejection_code_id,
        rejected_quantity=inspection_data.rejected_quantity,
        inspector_name=inspection_data.inspector_name,
        remarks=inspection_data.remarks,
    )
    
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    
    # Update work order rejected quantity
    if inspection.inspection_result == 'FAIL' and inspection.rejected_quantity:
        from ..models.work_order import WorkOrder
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == inspection_data.work_order_id
        ).first()
        
        if work_order:
            work_order.rejected_quantity = (work_order.rejected_quantity or 0) + (inspection.rejected_quantity or 0)
            db.commit()
    
    return inspection


@router.get("/rejections", response_model=List[RejectionSummary])
def get_rejection_summary(
    work_order_id: int = Query(..., description="Work order ID"),
    db: Session = Depends(get_db)
):
    """
    Get rejection summary for a work order
    """
    rejections = db.query(
        QualityInspection.rejection_code_id,
        func.sum(QualityInspection.rejected_quantity).label('total_rejected'),
        func.count(QualityInspection.inspection_id).label('count')
    ).filter(
        QualityInspection.work_order_id == work_order_id,
        QualityInspection.inspection_result == 'FAIL'
    ).group_by(
        QualityInspection.rejection_code_id
    ).all()
    
    summary = []
    for rejection in rejections:
        summary.append({
            'rejection_code_id': rejection.rejection_code_id,
            'rejection_code': f"CODE_{rejection.rejection_code_id}" if rejection.rejection_code_id else "UNKNOWN",
            'total_rejected': rejection.total_rejected or 0,
            'count': rejection.count
        })
    
    return summary
