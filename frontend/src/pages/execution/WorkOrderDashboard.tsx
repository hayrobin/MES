/**
 * Work Order Dashboard Page
 * Main dashboard for viewing and managing work orders
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { workOrdersAPI } from '../../services/api';
import WorkOrderCard from '../../components/execution/WorkOrderCard';
import LargeButton from '../../components/shared/LargeButton';

const WorkOrderDashboard: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const [statusFilter, setStatusFilter] = useState<string>('');
  
  const { data: workOrders, isLoading } = useQuery({
    queryKey: ['workOrders', statusFilter],
    queryFn: () => workOrdersAPI.list({ status: statusFilter || undefined }),
  });

  const startMutation = useMutation({
    mutationFn: (id: number) => workOrdersAPI.start(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workOrders'] });
    },
  });

  const pauseMutation = useMutation({
    mutationFn: (id: number) => workOrdersAPI.pause(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workOrders'] });
    },
  });

  const completeMutation = useMutation({
    mutationFn: (id: number) => workOrdersAPI.complete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workOrders'] });
    },
  });

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Work Order Dashboard</h1>
        
        {/* Filters */}
        <div className="flex gap-4 mb-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-lg"
          >
            <option value="">All Statuses</option>
            <option value="PLANNED">Planned</option>
            <option value="RUNNING">Running</option>
            <option value="PAUSED">Paused</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">Loading work orders...</div>
        </div>
      ) : !workOrders || workOrders.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">No work orders found</div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workOrders.map((workOrder) => (
            <WorkOrderCard
              key={workOrder.work_order_id}
              workOrder={workOrder}
              onStart={(id) => startMutation.mutate(id)}
              onPause={(id) => pauseMutation.mutate(id)}
              onComplete={(id) => completeMutation.mutate(id)}
              onViewDetails={(id) => navigate(`/execution/work-orders/${id}`)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default WorkOrderDashboard;
