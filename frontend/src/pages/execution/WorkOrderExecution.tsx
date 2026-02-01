/**
 * Work Order Execution Page
 * Detailed view and execution of a single work order
 */

import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { workOrdersAPI, productionAPI } from '../../services/api';

const WorkOrderExecution: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const workOrderId = parseInt(id || '0');

  const { data: workOrder, isLoading } = useQuery({
    queryKey: ['workOrder', workOrderId],
    queryFn: () => workOrdersAPI.get(workOrderId),
    enabled: workOrderId > 0,
  });

  const { data: summary } = useQuery({
    queryKey: ['productionSummary', workOrderId],
    queryFn: () => productionAPI.getSummary(workOrderId),
    enabled: workOrderId > 0,
  });

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="text-xl text-gray-600">Loading work order...</div>
      </div>
    );
  }

  if (!workOrder) {
    return (
      <div className="p-6">
        <div className="text-xl text-red-600">Work order not found</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{workOrder.work_order_no}</h1>
        <div className="text-lg text-gray-600">Work Order Execution</div>
      </div>

      {/* Work Order Header */}
      <div className="card mb-6">
        <h2 className="text-2xl font-bold mb-4">Work Order Details</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div className="text-sm text-gray-600">Status</div>
            <div className={`status-badge mt-1 inline-flex status-${workOrder.status.toLowerCase()}`}>
              {workOrder.status}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Target Quantity</div>
            <div className="text-xl font-bold">{workOrder.target_quantity}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Produced</div>
            <div className="text-xl font-bold text-green-600">{workOrder.produced_quantity}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Completion</div>
            <div className="text-xl font-bold">
              {summary?.completion_percentage.toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      {/* Operations Sequence */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Operations Sequence</h2>
        {workOrder.operations && workOrder.operations.length > 0 ? (
          <div className="space-y-4">
            {workOrder.operations.map((operation) => (
              <div key={operation.operation_execution_id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="text-lg font-semibold">
                      Step {operation.operation_sequence}: {operation.operation_name || 'Unnamed Operation'}
                    </div>
                    <div className="text-sm text-gray-600">{operation.operator_name || 'No operator assigned'}</div>
                  </div>
                  <span className={`status-badge status-${operation.status.toLowerCase()}`}>
                    {operation.status}
                  </span>
                </div>
                
                {operation.produced_quantity !== null && (
                  <div className="grid grid-cols-3 gap-4 mt-3">
                    <div>
                      <div className="text-sm text-gray-600">Produced</div>
                      <div className="text-lg font-semibold text-green-600">{operation.produced_quantity}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">Scrap</div>
                      <div className="text-lg font-semibold text-orange-600">{operation.scrap_quantity}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">Duration</div>
                      <div className="text-lg font-semibold">{operation.duration_minutes?.toFixed(1)} min</div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-gray-600">No operations defined for this work order</div>
        )}
      </div>
    </div>
  );
};

export default WorkOrderExecution;
