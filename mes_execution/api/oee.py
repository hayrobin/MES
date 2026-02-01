"""
OEE (Overall Equipment Effectiveness) API Endpoints
"""

from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from ..database import get_db
from ..services.oee_calculator import OEECalculator
from ..schemas.oee import OEEMetrics, OEESnapshot, OEEBreakdown

router = APIRouter(prefix="/api/v1/execution/oee", tags=["oee"])


@router.get("/realtime", response_model=OEEMetrics)
def get_realtime_oee(
    equipment_id: int = Query(..., description="Equipment ID"),
    start_time: Optional[datetime] = Query(None, description="Period start time"),
    end_time: Optional[datetime] = Query(None, description="Period end time"),
    ideal_cycle_time: Optional[float] = Query(None, description="Ideal cycle time in minutes"),
    planned_production_time: Optional[float] = Query(None, description="Planned production time in minutes"),
    db: Session = Depends(get_db)
):
    """
    Get real-time OEE calculation
    """
    # Default to current shift (8 hours) if not specified
    if not end_time:
        end_time = datetime.utcnow()
    if not start_time:
        start_time = end_time - timedelta(hours=8)
    
    calculator = OEECalculator(db)
    
    oee_data = calculator.calculate_realtime_oee(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time,
        ideal_cycle_time=Decimal(str(ideal_cycle_time)) if ideal_cycle_time else Decimal('1.0'),
        planned_production_time=Decimal(str(planned_production_time)) if planned_production_time else None
    )
    
    return OEEMetrics(
        equipment_id=oee_data['equipment_id'],
        period_start=oee_data['period_start'],
        period_end=oee_data['period_end'],
        availability=oee_data['availability'],
        performance=oee_data['performance'],
        quality=oee_data['quality'],
        oee=oee_data['oee']
    )


@router.get("/history")
def get_oee_history(
    equipment_id: int = Query(..., description="Equipment ID"),
    period_type: str = Query("SHIFT", description="Period type: SHIFT, HOUR, DAY"),
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    db: Session = Depends(get_db)
):
    """
    Get historical OEE data from snapshots
    """
    from ..models.oee_snapshot import OEESnapshot as OEESnapshotModel
    from sqlalchemy import and_
    
    query = db.query(OEESnapshotModel).filter(
        and_(
            OEESnapshotModel.equipment_id == equipment_id,
            OEESnapshotModel.period_type == period_type
        )
    )
    
    if start_date:
        query = query.filter(OEESnapshotModel.period_start >= start_date)
    if end_date:
        query = query.filter(OEESnapshotModel.period_end <= end_date)
    
    snapshots = query.order_by(OEESnapshotModel.period_start.desc()).limit(50).all()
    
    return snapshots


@router.get("/breakdown", response_model=OEEBreakdown)
def get_oee_breakdown(
    equipment_id: int = Query(..., description="Equipment ID"),
    date: datetime = Query(..., description="Date for breakdown"),
    ideal_cycle_time: Optional[float] = Query(1.0, description="Ideal cycle time"),
    db: Session = Depends(get_db)
):
    """
    Get detailed OEE breakdown with downtime reasons
    """
    # Calculate for the full day
    start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=1)
    
    calculator = OEECalculator(db)
    
    # Get OEE metrics
    oee_data = calculator.calculate_realtime_oee(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time,
        ideal_cycle_time=Decimal(str(ideal_cycle_time))
    )
    
    # Get downtime breakdown
    downtime_reasons = calculator.get_downtime_breakdown(
        equipment_id=equipment_id,
        start_time=start_time,
        end_time=end_time
    )
    
    # Calculate actual cycle time
    actual_cycle_time = None
    if oee_data['total_pieces'] > 0 and oee_data['actual_run_time'] > 0:
        actual_cycle_time = float(oee_data['actual_run_time']) / oee_data['total_pieces']
    
    return OEEBreakdown(
        equipment_id=equipment_id,
        equipment_name=f"Equipment_{equipment_id}",
        period_start=start_time,
        period_end=end_time,
        availability=oee_data['availability'],
        performance=oee_data['performance'],
        quality=oee_data['quality'],
        oee=oee_data['oee'],
        planned_production_time=Decimal(str(oee_data['planned_production_time'])),
        actual_run_time=Decimal(str(oee_data['actual_run_time'])),
        downtime_minutes=Decimal(str(oee_data['downtime_minutes'])),
        downtime_reasons=downtime_reasons,
        total_pieces=oee_data['total_pieces'],
        good_pieces=oee_data['good_pieces'],
        rejected_pieces=oee_data['rejected_pieces'],
        ideal_cycle_time=Decimal(str(ideal_cycle_time)),
        actual_cycle_time=Decimal(str(actual_cycle_time)) if actual_cycle_time else None
    )
