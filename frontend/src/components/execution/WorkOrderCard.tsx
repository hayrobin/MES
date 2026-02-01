/**
 * Work Order Card Component
 * Card-based display for work orders (shop-floor optimized)
 */

import React from 'react';
import type { WorkOrder } from '../../types';
import LargeButton from '../shared/LargeButton';

interface WorkOrderCardProps {
  workOrder: WorkOrder;
  onStart?: (id: number) => void;
  onPause?: (id: number) => void;
  onComplete?: (id: number) => void;
  onViewDetails?: (id: number) => void;
}

const WorkOrderCard: React.FC<WorkOrderCardProps> = ({
  workOrder,
  onStart,
  onPause,
  onComplete,
  onViewDetails,
}) => {
  const getStatusClass = (status: string) => {
    const classes = {
      RUNNING: 'status-running',
      PAUSED: 'status-paused',
      COMPLETED: 'status-completed',
      PLANNED: 'status-planned',
      CANCELLED: 'bg-red-100 text-red-800 border border-red-300',
    };
    return classes[status as keyof typeof classes] || 'status-planned';
  };

  const completionPercentage = workOrder.target_quantity > 0
    ? (workOrder.produced_quantity / workOrder.target_quantity) * 100
    : 0;

  return (
    <div className="card hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-2xl font-bold text-gray-900">{workOrder.work_order_no}</h3>
          <p className="text-sm text-gray-600">Priority: {workOrder.priority}</p>
        </div>
        <span className={`status-badge ${getStatusClass(workOrder.status)}`}>
          {workOrder.status}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-1">
          <span className="font-semibold">Progress</span>
          <span className="text-gray-600">
            {workOrder.produced_quantity} / {workOrder.target_quantity}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-blue-600 h-4 rounded-full transition-all"
            style={{ width: `${Math.min(completionPercentage, 100)}%` }}
          />
        </div>
        <div className="text-right text-sm text-gray-600 mt-1">
          {completionPercentage.toFixed(1)}%
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-3 gap-3 mb-4 text-center">
        <div>
          <div className="text-sm text-gray-600">Produced</div>
          <div className="text-xl font-bold text-green-600">{workOrder.produced_quantity}</div>
        </div>
        <div>
          <div className="text-sm text-gray-600">Scrap</div>
          <div className="text-xl font-bold text-orange-600">{workOrder.scrap_quantity}</div>
        </div>
        <div>
          <div className="text-sm text-gray-600">Rejected</div>
          <div className="text-xl font-bold text-red-600">{workOrder.rejected_quantity}</div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2 flex-wrap">
        {workOrder.status === 'PLANNED' && onStart && (
          <LargeButton
            variant="success"
            onClick={() => onStart(workOrder.work_order_id)}
            className="flex-1"
          >
            START
          </LargeButton>
        )}
        
        {workOrder.status === 'RUNNING' && onPause && (
          <LargeButton
            variant="warning"
            onClick={() => onPause(workOrder.work_order_id)}
            className="flex-1"
          >
            PAUSE
          </LargeButton>
        )}
        
        {(workOrder.status === 'RUNNING' || workOrder.status === 'PAUSED') && onComplete && (
          <LargeButton
            variant="primary"
            onClick={() => onComplete(workOrder.work_order_id)}
            className="flex-1"
          >
            COMPLETE
          </LargeButton>
        )}
        
        {onViewDetails && (
          <LargeButton
            variant="secondary"
            onClick={() => onViewDetails(workOrder.work_order_id)}
            className="flex-1"
          >
            DETAILS
          </LargeButton>
        )}
      </div>
    </div>
  );
};

export default WorkOrderCard;
