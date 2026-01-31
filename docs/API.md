# API Documentation

Complete API reference for the Factory MES System.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production deployments, implement OAuth2 or API key authentication.

## Endpoints

### Health Check

#### GET /api/status/health

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### System Status

#### GET /api/status

Get detailed system health and status information.

**Response:**
```json
{
  "status": "running",
  "uptime": 3600.5,
  "devices": [
    {
      "name": "PLC1",
      "type": "opcua_client",
      "status": "connected",
      "last_seen": "2024-01-31T10:30:00"
    },
    {
      "name": "TempSensor1",
      "type": "modbus",
      "status": "connected",
      "last_seen": "2024-01-31T10:30:00"
    }
  ],
  "database_connected": true
}
```

## Device Management

### List Devices

#### GET /api/devices

Get list of all registered devices.

**Response:**
```json
[
  {
    "id": 1,
    "name": "PLC1",
    "device_type": "opcua_client",
    "connection_string": "opc.tcp://192.168.1.100:4840",
    "status": "connected",
    "last_seen": "2024-01-31T10:30:00",
    "created_at": "2024-01-31T08:00:00",
    "updated_at": "2024-01-31T10:30:00"
  }
]
```

### Create Device

#### POST /api/devices

Create a new device.

**Request Body:**
```json
{
  "name": "NewDevice",
  "device_type": "modbus",
  "connection_string": "192.168.1.50:502",
  "config": {
    "unit_id": 1,
    "polling_interval": 2
  }
}
```

**Response:**
```json
{
  "id": 2,
  "name": "NewDevice",
  "device_type": "modbus",
  "connection_string": "192.168.1.50:502",
  "status": "disconnected",
  "last_seen": null,
  "created_at": "2024-01-31T10:35:00",
  "updated_at": "2024-01-31T10:35:00"
}
```

### Get Device

#### GET /api/devices/{device_id}

Get device by ID.

**Parameters:**
- `device_id` (path, integer): Device ID

**Response:**
```json
{
  "id": 1,
  "name": "PLC1",
  "device_type": "opcua_client",
  "connection_string": "opc.tcp://192.168.1.100:4840",
  "status": "connected",
  "last_seen": "2024-01-31T10:30:00",
  "created_at": "2024-01-31T08:00:00",
  "updated_at": "2024-01-31T10:30:00"
}
```

## Data Access

### Get Real-time Data

#### GET /api/data/realtime

Get current real-time values for all or specific device.

**Parameters:**
- `device_id` (query, integer, optional): Filter by device ID

**Response:**
```json
[
  {
    "device_id": 1,
    "data_point_name": "Temperature",
    "value": "25.5",
    "quality": "good",
    "timestamp": "2024-01-31T10:30:00"
  },
  {
    "device_id": 1,
    "data_point_name": "Pressure",
    "value": "6.5",
    "quality": "good",
    "timestamp": "2024-01-31T10:30:00"
  }
]
```

### Query Historical Data

#### POST /api/data/history

Query historical time-series data.

**Request Body:**
```json
{
  "device_id": 1,
  "data_point_name": "Temperature",
  "start_time": "2024-01-31T00:00:00",
  "end_time": "2024-01-31T12:00:00"
}
```

**Response:**
```json
[
  {
    "device_id": 1,
    "data_point_name": "Temperature",
    "value": "25.5",
    "quality": "good",
    "timestamp": "2024-01-31T10:00:00"
  },
  {
    "device_id": 1,
    "data_point_name": "Temperature",
    "value": "25.6",
    "quality": "good",
    "timestamp": "2024-01-31T10:01:00"
  }
]
```

## OPC UA Operations

### Browse OPC UA Nodes

#### POST /api/opcua/browse

Browse OPC UA server address space.

**Request Body:**
```json
{
  "client_name": "PLC1",
  "node_id": "ns=2;i=1"
}
```

**Response:**
```json
[
  {
    "node_id": "ns=2;s=Temperature",
    "browse_name": "Temperature",
    "display_name": "Temperature Sensor",
    "node_class": "Variable"
  },
  {
    "node_id": "ns=2;s=Pressure",
    "browse_name": "Pressure",
    "display_name": "Pressure Sensor",
    "node_class": "Variable"
  }
]
```

### Read OPC UA Node

#### POST /api/opcua/read

Read value from an OPC UA node.

**Request Body:**
```json
{
  "client_name": "PLC1",
  "node_id": "ns=2;s=Temperature"
}
```

**Response:**
```json
{
  "node_id": "ns=2;s=Temperature",
  "value": 25.5
}
```

### Write OPC UA Node

#### POST /api/opcua/write

Write value to an OPC UA node.

**Request Body:**
```json
{
  "client_name": "PLC1",
  "node_id": "ns=2;s=Setpoint",
  "value": 30.0
}
```

**Response:**
```json
{
  "status": "success",
  "node_id": "ns=2;s=Setpoint",
  "value": 30.0
}
```

## Modbus Operations

### Read Modbus Register

#### POST /api/modbus/read

Read value from a Modbus register.

**Request Body:**
```json
{
  "device_name": "TempSensor1",
  "register_name": "Temperature"
}
```

**Response:**
```json
{
  "device": "TempSensor1",
  "register": "Temperature",
  "value": 25.5
}
```

### Write Modbus Register

#### POST /api/modbus/write

Write value to a Modbus register.

**Request Body:**
```json
{
  "device_name": "VFD1",
  "register_name": "SpeedSetpoint",
  "value": 1500
}
```

**Response:**
```json
{
  "status": "success",
  "device": "VFD1",
  "register": "SpeedSetpoint",
  "value": 1500
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK` - Request successful
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Interactive API Documentation

The system provides interactive API documentation via Swagger UI:

```
http://localhost:8000/docs
```

Alternative ReDoc documentation:

```
http://localhost:8000/redoc
```

## Code Examples

### Python

```python
import requests

# Get system status
response = requests.get("http://localhost:8000/api/status")
status = response.json()
print(f"System uptime: {status['uptime']} seconds")

# Get real-time data
response = requests.get("http://localhost:8000/api/data/realtime")
data = response.json()
for point in data:
    print(f"{point['data_point_name']}: {point['value']}")

# Read Modbus register
response = requests.post(
    "http://localhost:8000/api/modbus/read",
    json={
        "device_name": "TempSensor1",
        "register_name": "Temperature"
    }
)
result = response.json()
print(f"Temperature: {result['value']}")
```

### JavaScript

```javascript
// Get system status
fetch('http://localhost:8000/api/status')
  .then(response => response.json())
  .then(data => {
    console.log('System uptime:', data.uptime, 'seconds');
  });

// Get real-time data
fetch('http://localhost:8000/api/data/realtime')
  .then(response => response.json())
  .then(data => {
    data.forEach(point => {
      console.log(`${point.data_point_name}: ${point.value}`);
    });
  });

// Write OPC UA node
fetch('http://localhost:8000/api/opcua/write', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    client_name: 'PLC1',
    node_id: 'ns=2;s=Setpoint',
    value: 30.0
  })
})
  .then(response => response.json())
  .then(data => {
    console.log('Write successful:', data);
  });
```

### cURL

```bash
# Get system status
curl http://localhost:8000/api/status

# Get real-time data for device ID 1
curl "http://localhost:8000/api/data/realtime?device_id=1"

# Query historical data
curl -X POST http://localhost:8000/api/data/history \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "data_point_name": "Temperature",
    "start_time": "2024-01-31T00:00:00",
    "end_time": "2024-01-31T12:00:00"
  }'

# Read Modbus register
curl -X POST http://localhost:8000/api/modbus/read \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "TempSensor1",
    "register_name": "Temperature"
  }'

# Write Modbus register
curl -X POST http://localhost:8000/api/modbus/write \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "VFD1",
    "register_name": "SpeedSetpoint",
    "value": 1500
  }'
```

## Rate Limiting

Currently, no rate limiting is implemented. For production deployments, consider implementing rate limiting to prevent abuse.

## WebSocket Support

Future versions will include WebSocket endpoints for real-time data streaming.

Example endpoint (planned):
```
ws://localhost:8000/ws/realtime
```

## Versioning

The API is currently at version 1.0.0. Future versions will maintain backwards compatibility or use versioned endpoints (e.g., `/api/v2/devices`).
