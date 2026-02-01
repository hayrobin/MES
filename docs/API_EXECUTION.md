# MES Execution API Documentation

## Base URL

```
http://localhost:8000/api/v1/execution
```

## Authentication

Currently, authentication is not implemented. In production, add JWT or OAuth2 authentication.

## Work Orders API

### List Work Orders

```http
GET /work-orders/
```

**Query Parameters:**
- `status` (optional) - Filter by status: PLANNED, RUNNING, PAUSED, COMPLETED, CANCELLED
- `line_id` (optional) - Filter by line ID
- `equipment_id` (optional) - Filter by equipment ID
- `skip` (optional) - Pagination offset (default: 0)
- `limit` (optional) - Results per page (default: 100, max: 1000)

**Response:** Array of Work Order objects

### Get Work Order Details

```http
GET /work-orders/{work_order_id}
```

**Response:** Work Order object with operations array

### Start Work Order

```http
POST /work-orders/{work_order_id}/start
```

**Request Body:**
```json
{
  "operator_name": "John Doe"
}
```

**Response:** Updated Work Order object

### Pause Work Order

```http
POST /work-orders/{work_order_id}/pause
```

**Response:** Updated Work Order object

### Complete Work Order

```http
POST /work-orders/{work_order_id}/complete
```

**Response:** Updated Work Order object

## Production API

### Log Production

```http
POST /production/log
```

**Request Body:**
```json
{
  "work_order_id": 1,
  "operation_execution_id": 5,
  "timestamp": "2026-02-01T10:30:00Z",
  "produced_quantity": 100,
  "scrap_quantity": 5,
  "operator_name": "John Doe",
  "equipment_id": 1,
  "batch_number": "BATCH-001"
}
```

**Response:** Production Log object

### Get Production Summary

```http
GET /production/summary?work_order_id=1
```

**Response:**
```json
{
  "work_order_id": 1,
  "work_order_no": "WO-2026-001",
  "total_produced": 500,
  "total_scrap": 25,
  "total_rejected": 10,
  "target_quantity": 1000,
  "completion_percentage": 50.0,
  "status": "RUNNING"
}
```

## Materials API

### Record Material Consumption

```http
POST /materials/consume
```

**Request Body:**
```json
{
  "work_order_id": 1,
  "operation_execution_id": 5,
  "material_id": 10,
  "planned_quantity": 100.5,
  "actual_quantity": 102.3,
  "uom": "KG",
  "batch_number": "BATCH-2026-001",
  "heat_number": "HEAT-12345",
  "lot_number": "LOT-67890",
  "entered_by": "John Doe"
}
```

**Response:** Material Consumption object

### Get Material Consumption History

```http
GET /materials/consumption?work_order_id=1
```

**Response:** Array of Material Consumption objects

## Quality API

### Record Quality Inspection

```http
POST /quality/inspect
```

**Request Body:**
```json
{
  "work_order_id": 1,
  "operation_execution_id": 5,
  "inspection_time": "2026-02-01T10:30:00Z",
  "inspection_result": "FAIL",
  "rejection_code_id": 3,
  "rejected_quantity": 10,
  "inspector_name": "Jane Smith",
  "remarks": "Dimension out of tolerance"
}
```

**Response:** Quality Inspection object

### Get Rejection Summary

```http
GET /quality/rejections?work_order_id=1
```

**Response:** Array of rejection summaries grouped by rejection code

## Equipment API

### Get Current Equipment Status

```http
GET /equipment/{equipment_id}/status
```

**Response:**
```json
{
  "equipment_id": 1,
  "current_state": "RUNNING",
  "state_start_time": "2026-02-01T08:00:00Z",
  "duration_minutes": 150.5,
  "work_order_id": 1
}
```

### Update Equipment State

```http
POST /equipment/{equipment_id}/state
```

**Request Body:**
```json
{
  "state": "DOWN",
  "reason_code": "BREAKDOWN",
  "reason_description": "Hydraulic pump failure",
  "work_order_id": null,
  "operator_name": "John Doe"
}
```

**Response:** Equipment State object

### Get Equipment State Timeline

```http
GET /equipment/{equipment_id}/timeline
```

**Query Parameters:**
- `start_time` (optional) - Filter start time
- `end_time` (optional) - Filter end time

**Response:** Array of Equipment State objects

## OEE API

### Get Real-time OEE

```http
GET /oee/realtime?equipment_id=1&ideal_cycle_time=1.5
```

**Query Parameters:**
- `equipment_id` (required) - Equipment ID
- `start_time` (optional) - Period start (default: 8 hours ago)
- `end_time` (optional) - Period end (default: now)
- `ideal_cycle_time` (optional) - Ideal cycle time in minutes
- `planned_production_time` (optional) - Planned production time in minutes

**Response:**
```json
{
  "equipment_id": 1,
  "period_start": "2026-02-01T00:00:00Z",
  "period_end": "2026-02-01T08:00:00Z",
  "availability": 87.5,
  "performance": 92.3,
  "quality": 95.0,
  "oee": 76.8
}
```

### Get OEE History

```http
GET /oee/history?equipment_id=1&period_type=SHIFT
```

**Query Parameters:**
- `equipment_id` (required)
- `period_type` (optional) - SHIFT, HOUR, DAY (default: SHIFT)
- `start_date` (optional)
- `end_date` (optional)

**Response:** Array of OEE Snapshot objects

### Get OEE Breakdown

```http
GET /oee/breakdown?equipment_id=1&date=2026-02-01&ideal_cycle_time=1.5
```

**Response:**
```json
{
  "equipment_id": 1,
  "equipment_name": "Equipment_1",
  "period_start": "2026-02-01T00:00:00Z",
  "period_end": "2026-02-02T00:00:00Z",
  "availability": 87.5,
  "performance": 92.3,
  "quality": 95.0,
  "oee": 76.8,
  "planned_production_time": 480.0,
  "actual_run_time": 420.0,
  "downtime_minutes": 60.0,
  "downtime_reasons": [
    {
      "reason_code": "BREAKDOWN",
      "reason_description": "Equipment failure",
      "duration_minutes": 45.0,
      "percentage": 75.0
    },
    {
      "reason_code": "SETUP",
      "reason_description": "Tool change",
      "duration_minutes": 15.0,
      "percentage": 25.0
    }
  ],
  "total_pieces": 1000,
  "good_pieces": 950,
  "rejected_pieces": 50,
  "ideal_cycle_time": 1.5,
  "actual_cycle_time": 0.42
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

## Data Models

### Work Order

```typescript
{
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
  created_at: string;
  updated_at: string;
}
```

## Rate Limiting

Currently not implemented. Consider adding rate limiting for production deployments.

## Versioning

API version is included in the URL path: `/api/v1/execution/`

Future versions will use `/api/v2/execution/` etc.
