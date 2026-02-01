/**
 * TypeScript type definitions for MES Execution
 */

export interface WorkOrder {
  work_order_id: number;
  work_order_no: string;
  product_id?: number;
  equipment_id?: number;
  line_id?: number;
  target_quantity: number;
  produced_quantity: number;
  scrap_quantity: number;
  rejected_quantity: number;
  status: 'PLANNED' | 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'CANCELLED';
  priority: number;
  planned_start_time?: string;
  planned_end_time?: string;
  actual_start_time?: string;
  actual_end_time?: string;
  shift_id?: number;
  erp_order_ref?: string;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

export interface OperationExecution {
  operation_execution_id: number;
  work_order_id: number;
  operation_id?: number;
  operation_sequence: number;
  operation_name?: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'SKIPPED';
  start_time?: string;
  end_time?: string;
  duration_minutes?: number;
  produced_quantity?: number;
  scrap_quantity?: number;
  operator_name?: string;
  operator_id?: string;
}

export interface WorkOrderWithOperations extends WorkOrder {
  operations: OperationExecution[];
}

export interface ProductionLog {
  log_id: number;
  work_order_id: number;
  operation_execution_id?: number;
  timestamp: string;
  produced_quantity?: number;
  scrap_quantity?: number;
  operator_name?: string;
  equipment_id?: number;
  batch_number?: string;
  created_at: string;
}

export interface MaterialConsumption {
  consumption_id: number;
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
  consumption_time: string;
  entered_by?: string;
}

export interface QualityInspection {
  inspection_id: number;
  work_order_id: number;
  operation_execution_id?: number;
  inspection_time: string;
  inspection_result: 'PASS' | 'FAIL';
  rejection_code_id?: number;
  rejected_quantity?: number;
  inspector_name?: string;
  remarks?: string;
}

export interface EquipmentState {
  state_id: number;
  equipment_id: number;
  state: 'RUNNING' | 'IDLE' | 'DOWN' | 'SETUP' | 'MAINTENANCE';
  state_start_time: string;
  state_end_time?: string;
  duration_minutes?: number;
  reason_code?: string;
  reason_description?: string;
  work_order_id?: number;
  operator_name?: string;
}

export interface OEEMetrics {
  equipment_id: number;
  period_start: string;
  period_end: string;
  availability: number;
  performance: number;
  quality: number;
  oee: number;
}

export interface OEEBreakdown extends OEEMetrics {
  equipment_name?: string;
  planned_production_time: number;
  actual_run_time: number;
  downtime_minutes: number;
  downtime_reasons: DowntimeReason[];
  total_pieces: number;
  good_pieces: number;
  rejected_pieces: number;
  ideal_cycle_time: number;
  actual_cycle_time?: number;
}

export interface DowntimeReason {
  reason_code: string;
  reason_description?: string;
  duration_minutes: number;
  percentage: number;
}

export interface ProductionSummary {
  work_order_id: number;
  work_order_no: string;
  total_produced: number;
  total_scrap: number;
  total_rejected: number;
  target_quantity: number;
  completion_percentage: number;
  status: string;
}

export type UserRole = 'OPERATOR' | 'SUPERVISOR' | 'ADMIN';
