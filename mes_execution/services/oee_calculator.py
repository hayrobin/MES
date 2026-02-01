"""
OEE (Overall Equipment Effectiveness) Calculator Service
Implements industry-standard OEE calculation methodology
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.equipment_state import EquipmentState
from ..models.production_log import ProductionLog
from ..models.quality_inspection import QualityInspection
from ..models.oee_snapshot import OEESnapshot


class OEECalculator:
    """
    OEE Calculator Service
    
    Formula:
    OEE = Availability × Performance × Quality
    
    Availability = (Operating Time / Planned Production Time) × 100
      where Operating Time = Planned Time - Downtime
    
    Performance = (Ideal Cycle Time × Total Pieces / Operating Time) × 100
    
    Quality = (Good Pieces / Total Pieces) × 100
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_realtime_oee(
        self,
        equipment_id: int,
        start_time: datetime,
        end_time: datetime,
        ideal_cycle_time: Optional[Decimal] = None,
        planned_production_time: Optional[Decimal] = None,
    ) -> Dict:
        """
        Calculate real-time OEE for an equipment in a given time period
        
        Args:
            equipment_id: Equipment ID
            start_time: Period start time
            end_time: Period end time
            ideal_cycle_time: Ideal cycle time in minutes per piece
            planned_production_time: Planned production time in minutes
        
        Returns:
            Dictionary with OEE metrics
        """
        # Default planned production time to period duration if not provided
        if planned_production_time is None:
            period_duration = (end_time - start_time).total_seconds() / 60  # in minutes
            planned_production_time = Decimal(str(period_duration))
        
        # Calculate downtime from equipment state
        downtime = self._calculate_downtime(equipment_id, start_time, end_time)
        
        # Calculate operating time
        operating_time = planned_production_time - downtime
        
        # Calculate availability
        if planned_production_time > 0:
            availability = (operating_time / planned_production_time) * 100
        else:
            availability = Decimal('0')
        
        # Get production data
        production_data = self._get_production_data(equipment_id, start_time, end_time)
        total_pieces = production_data['total_pieces']
        good_pieces = production_data['good_pieces']
        rejected_pieces = production_data['rejected_pieces']
        
        # Calculate performance
        if ideal_cycle_time and operating_time > 0 and ideal_cycle_time > 0:
            ideal_production_time = ideal_cycle_time * total_pieces
            performance = (ideal_production_time / operating_time) * 100
            # Cap performance at 100% (can't exceed ideal)
            performance = min(performance, Decimal('100'))
        else:
            performance = Decimal('0')
        
        # Calculate quality
        if total_pieces > 0:
            quality = (good_pieces / total_pieces) * 100
        else:
            quality = Decimal('0')
        
        # Calculate OEE
        oee = (availability * performance * quality) / 10000  # Divide by 10000 since all are percentages
        
        return {
            'equipment_id': equipment_id,
            'period_start': start_time,
            'period_end': end_time,
            'availability': round(availability, 2),
            'performance': round(performance, 2),
            'quality': round(quality, 2),
            'oee': round(oee, 2),
            'planned_production_time': float(planned_production_time),
            'actual_run_time': float(operating_time),
            'downtime_minutes': float(downtime),
            'ideal_cycle_time': float(ideal_cycle_time) if ideal_cycle_time else None,
            'total_pieces': total_pieces,
            'good_pieces': good_pieces,
            'rejected_pieces': rejected_pieces,
        }
    
    def _calculate_downtime(
        self,
        equipment_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> Decimal:
        """Calculate total downtime in minutes for equipment"""
        # Query equipment states with DOWN status
        downtime_states = self.db.query(EquipmentState).filter(
            and_(
                EquipmentState.equipment_id == equipment_id,
                EquipmentState.state == 'DOWN',
                EquipmentState.state_start_time >= start_time,
                EquipmentState.state_start_time < end_time
            )
        ).all()
        
        total_downtime = Decimal('0')
        for state in downtime_states:
            if state.duration_minutes:
                total_downtime += state.duration_minutes
            elif state.state_end_time:
                # Calculate duration if not stored
                duration = (state.state_end_time - state.state_start_time).total_seconds() / 60
                total_downtime += Decimal(str(duration))
        
        return total_downtime
    
    def _get_production_data(
        self,
        equipment_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> Dict:
        """Get production data for the time period"""
        # Get total produced pieces
        produced = self.db.query(
            func.sum(ProductionLog.produced_quantity)
        ).filter(
            and_(
                ProductionLog.equipment_id == equipment_id,
                ProductionLog.timestamp >= start_time,
                ProductionLog.timestamp < end_time
            )
        ).scalar() or Decimal('0')
        
        # Get total rejected pieces
        rejected = self.db.query(
            func.sum(QualityInspection.rejected_quantity)
        ).join(
            ProductionLog,
            QualityInspection.work_order_id == ProductionLog.work_order_id
        ).filter(
            and_(
                ProductionLog.equipment_id == equipment_id,
                QualityInspection.inspection_time >= start_time,
                QualityInspection.inspection_time < end_time,
                QualityInspection.inspection_result == 'FAIL'
            )
        ).scalar() or Decimal('0')
        
        # Convert to int for piece counts, rounding to nearest integer
        total_pieces = int(round(float(produced))) if produced else 0
        rejected_pieces = int(round(float(rejected))) if rejected else 0
        good_pieces = max(0, total_pieces - rejected_pieces)
        
        return {
            'total_pieces': total_pieces,
            'good_pieces': good_pieces,
            'rejected_pieces': rejected_pieces,
        }
    
    def save_oee_snapshot(
        self,
        equipment_id: int,
        start_time: datetime,
        end_time: datetime,
        period_type: str,
        ideal_cycle_time: Optional[Decimal] = None,
        planned_production_time: Optional[Decimal] = None,
    ) -> OEESnapshot:
        """
        Calculate and save OEE snapshot to cache
        
        Args:
            equipment_id: Equipment ID
            start_time: Period start time
            end_time: Period end time
            period_type: SHIFT, HOUR, or DAY
            ideal_cycle_time: Ideal cycle time
            planned_production_time: Planned production time
        
        Returns:
            Saved OEESnapshot object
        """
        oee_data = self.calculate_realtime_oee(
            equipment_id,
            start_time,
            end_time,
            ideal_cycle_time,
            planned_production_time
        )
        
        # Create snapshot
        snapshot = OEESnapshot(
            equipment_id=equipment_id,
            period_start=start_time,
            period_end=end_time,
            period_type=period_type,
            availability=oee_data['availability'],
            performance=oee_data['performance'],
            quality=oee_data['quality'],
            oee=oee_data['oee'],
            planned_production_time=Decimal(str(oee_data['planned_production_time'])),
            actual_run_time=Decimal(str(oee_data['actual_run_time'])),
            downtime_minutes=Decimal(str(oee_data['downtime_minutes'])),
            ideal_cycle_time=Decimal(str(oee_data['ideal_cycle_time'])) if oee_data['ideal_cycle_time'] else None,
            total_pieces=oee_data['total_pieces'],
            good_pieces=oee_data['good_pieces'],
            rejected_pieces=oee_data['rejected_pieces'],
        )
        
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        
        return snapshot
    
    def get_downtime_breakdown(
        self,
        equipment_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict]:
        """Get breakdown of downtime reasons"""
        downtime_states = self.db.query(
            EquipmentState.reason_code,
            EquipmentState.reason_description,
            func.sum(EquipmentState.duration_minutes).label('total_duration')
        ).filter(
            and_(
                EquipmentState.equipment_id == equipment_id,
                EquipmentState.state == 'DOWN',
                EquipmentState.state_start_time >= start_time,
                EquipmentState.state_start_time < end_time
            )
        ).group_by(
            EquipmentState.reason_code,
            EquipmentState.reason_description
        ).all()
        
        total_downtime = sum(d.total_duration for d in downtime_states if d.total_duration)
        
        breakdown = []
        for downtime in downtime_states:
            if downtime.total_duration:
                percentage = (downtime.total_duration / total_downtime * 100) if total_downtime > 0 else 0
                breakdown.append({
                    'reason_code': downtime.reason_code or 'UNKNOWN',
                    'reason_description': downtime.reason_description,
                    'duration_minutes': float(downtime.total_duration),
                    'percentage': round(percentage, 2)
                })
        
        return breakdown
