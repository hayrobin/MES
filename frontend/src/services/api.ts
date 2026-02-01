/**
 * API Service for MES Execution
 */

import axios from 'axios';
import type {
  WorkOrder,
  WorkOrderWithOperations,
  ProductionLog,
  ProductionSummary,
  MaterialConsumption,
  QualityInspection,
  EquipmentState,
  OEEMetrics,
  OEEBreakdown,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1/execution';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Work Orders API
export const workOrdersAPI = {
  list: async (params?: {
    status?: string;
    line_id?: number;
    equipment_id?: number;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get<WorkOrder[]>('/work-orders/', { params });
    return response.data;
  },

  get: async (workOrderId: number) => {
    const response = await api.get<WorkOrderWithOperations>(`/work-orders/${workOrderId}`);
    return response.data;
  },

  start: async (workOrderId: number, operatorName?: string) => {
    const response = await api.post<WorkOrder>(`/work-orders/${workOrderId}/start`, {
      operator_name: operatorName,
    });
    return response.data;
  },

  pause: async (workOrderId: number) => {
    const response = await api.post<WorkOrder>(`/work-orders/${workOrderId}/pause`);
    return response.data;
  },

  complete: async (workOrderId: number) => {
    const response = await api.post<WorkOrder>(`/work-orders/${workOrderId}/complete`);
    return response.data;
  },
};

// Production API
export const productionAPI = {
  log: async (data: {
    work_order_id: number;
    operation_execution_id?: number;
    produced_quantity?: number;
    scrap_quantity?: number;
    operator_name?: string;
    equipment_id?: number;
    batch_number?: string;
  }) => {
    const response = await api.post<ProductionLog>('/production/log', data);
    return response.data;
  },

  getSummary: async (workOrderId: number) => {
    const response = await api.get<ProductionSummary>('/production/summary', {
      params: { work_order_id: workOrderId },
    });
    return response.data;
  },

  getLogs: async (params?: {
    work_order_id?: number;
    equipment_id?: number;
    start_time?: string;
    end_time?: string;
    skip?: number;
    limit?: number;
  }) => {
    const response = await api.get<ProductionLog[]>('/production/logs', { params });
    return response.data;
  },
};

// Material API
export const materialAPI = {
  consume: async (data: {
    work_order_id: number;
    operation_execution_id?: number;
    material_id?: number;
    planned_quantity?: number;
    actual_quantity: number;
    uom?: string;
    batch_number?: string;
    heat_number?: string;
    lot_number?: string;
    serial_number?: string;
    entered_by?: string;
  }) => {
    const response = await api.post<MaterialConsumption>('/materials/consume', data);
    return response.data;
  },

  getConsumption: async (workOrderId: number) => {
    const response = await api.get<MaterialConsumption[]>('/materials/consumption', {
      params: { work_order_id: workOrderId },
    });
    return response.data;
  },
};

// Quality API
export const qualityAPI = {
  inspect: async (data: {
    work_order_id: number;
    operation_execution_id?: number;
    inspection_result: 'PASS' | 'FAIL';
    rejection_code_id?: number;
    rejected_quantity?: number;
    inspector_name?: string;
    remarks?: string;
  }) => {
    const response = await api.post<QualityInspection>('/quality/inspect', data);
    return response.data;
  },

  getRejections: async (workOrderId: number) => {
    const response = await api.get('/quality/rejections', {
      params: { work_order_id: workOrderId },
    });
    return response.data;
  },
};

// Equipment API
export const equipmentAPI = {
  getStatus: async (equipmentId: number) => {
    const response = await api.get(`/equipment/${equipmentId}/status`);
    return response.data;
  },

  updateState: async (equipmentId: number, data: {
    state: string;
    reason_code?: string;
    reason_description?: string;
    work_order_id?: number;
    operator_name?: string;
  }) => {
    const response = await api.post<EquipmentState>(`/equipment/${equipmentId}/state`, data);
    return response.data;
  },

  getTimeline: async (equipmentId: number, params?: {
    start_time?: string;
    end_time?: string;
  }) => {
    const response = await api.get<EquipmentState[]>(`/equipment/${equipmentId}/timeline`, { params });
    return response.data;
  },
};

// OEE API
export const oeeAPI = {
  getRealtime: async (params: {
    equipment_id: number;
    start_time?: string;
    end_time?: string;
    ideal_cycle_time?: number;
    planned_production_time?: number;
  }) => {
    const response = await api.get<OEEMetrics>('/oee/realtime', { params });
    return response.data;
  },

  getHistory: async (params: {
    equipment_id: number;
    period_type?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/oee/history', { params });
    return response.data;
  },

  getBreakdown: async (params: {
    equipment_id: number;
    date: string;
    ideal_cycle_time?: number;
  }) => {
    const response = await api.get<OEEBreakdown>('/oee/breakdown', { params });
    return response.data;
  },
};

export default api;
