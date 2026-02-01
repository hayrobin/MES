/**
 * Production & OEE Dashboard Page
 * Real-time OEE metrics and production monitoring
 */

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { oeeAPI } from '../../services/api';
import OEECard from '../../components/dashboards/OEECard';

const ProductionOEE: React.FC = () => {
  const [equipmentId, setEquipmentId] = useState(1);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  const { data: oeeData, isLoading } = useQuery({
    queryKey: ['oeeBreakdown', equipmentId, date],
    queryFn: () => oeeAPI.getBreakdown({
      equipment_id: equipmentId,
      date: date,
      ideal_cycle_time: 1.0,
    }),
  });

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Production & OEE Dashboard</h1>
        
        {/* Filters */}
        <div className="flex gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Equipment</label>
            <select
              value={equipmentId}
              onChange={(e) => setEquipmentId(parseInt(e.target.value))}
              className="px-4 py-2 border border-gray-300 rounded-lg"
            >
              <option value="1">Equipment 1</option>
              <option value="2">Equipment 2</option>
              <option value="3">Equipment 3</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">Loading OEE data...</div>
        </div>
      ) : !oeeData ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">No OEE data available</div>
        </div>
      ) : (
        <>
          {/* Top Row: 4 KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <OEECard label="Availability" value={oeeData.availability} />
            <OEECard label="Performance" value={oeeData.performance} />
            <OEECard label="Quality" value={oeeData.quality} />
            <OEECard label="Overall OEE" value={oeeData.oee} large />
          </div>

          {/* Second Row: Production Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="card">
              <div className="kpi-label">Total Pieces</div>
              <div className="kpi-value text-blue-600">{oeeData.total_pieces}</div>
            </div>
            <div className="card">
              <div className="kpi-label">Good Pieces</div>
              <div className="kpi-value text-green-600">{oeeData.good_pieces}</div>
            </div>
            <div className="card">
              <div className="kpi-label">Rejected Pieces</div>
              <div className="kpi-value text-red-600">{oeeData.rejected_pieces}</div>
            </div>
          </div>

          {/* Third Row: Time Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="card">
              <div className="kpi-label">Planned Time</div>
              <div className="kpi-value text-gray-700">{oeeData.planned_production_time.toFixed(0)} min</div>
            </div>
            <div className="card">
              <div className="kpi-label">Run Time</div>
              <div className="kpi-value text-blue-600">{oeeData.actual_run_time.toFixed(0)} min</div>
            </div>
            <div className="card">
              <div className="kpi-label">Downtime</div>
              <div className="kpi-value text-red-600">{oeeData.downtime_minutes.toFixed(0)} min</div>
            </div>
          </div>

          {/* Downtime Reasons */}
          {oeeData.downtime_reasons && oeeData.downtime_reasons.length > 0 && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">Downtime Breakdown</h2>
              <div className="space-y-3">
                {oeeData.downtime_reasons.map((reason, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold">{reason.reason_code}</div>
                      <div className="text-sm text-gray-600">{reason.reason_description || 'No description'}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-lg">{reason.duration_minutes.toFixed(0)} min</div>
                      <div className="text-sm text-gray-600">{reason.percentage.toFixed(1)}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ProductionOEE;
