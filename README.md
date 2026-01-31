 # Factory MES System

A comprehensive Manufacturing Execution System (MES) with OPC UA and Modbus TCP/IP support for industrial automation and data collection.

## Features

### Communication Protocols
- **OPC UA Server**: Expose factory data points with standard OPC UA information model
- **OPC UA Client**: Connect to PLCs, SCADA systems, and sensors
- **Modbus TCP/IP**: Support for all standard function codes (FC1-FC6, FC15-FC16)

### Core Capabilities
- Real-time data acquisition and monitoring
- Historical data storage with time-series support
- Device management and status tracking
- REST API for system integration
- WebSocket support for real-time data streaming
- Automatic reconnection and error handling
- Configurable polling intervals
- Data validation and quality checks

### Data Management
- SQLite support for development
- PostgreSQL support for production
- Efficient time-series data storage
- Configurable data retention policies
- Real-time and historical data queries

### API Endpoints
- `/api/devices` - Device management
- `/api/data/realtime` - Real-time data access
- `/api/data/history` - Historical data queries
- `/api/opcua/browse` - Browse OPC UA address space
- `/api/opcua/read` - Read OPC UA nodes
- `/api/opcua/write` - Write OPC UA nodes
- `/api/modbus/read` - Read Modbus registers
- `/api/modbus/write` - Write Modbus registers
- `/api/status` - System health and status

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hayrobin/MES.git
cd MES
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system:
Edit configuration files in the `config/` directory:
- `opcua_server.yaml` - OPC UA server nodes
- `opcua_clients.yaml` - OPC UA client connections
- `modbus_devices.yaml` - Modbus device configurations
- `mes_config.yaml` - General system settings

4. Run the application:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

5. Access the API:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/status/health

### Docker Deployment

1. Build and run with Docker Compose:
```bash
cd docker
docker-compose up -d
```

2. Access services:
- MES API: http://localhost:8000
- OPC UA Server: opc.tcp://localhost:4840
- PostgreSQL: localhost:5432
- pgAdmin: http://localhost:5050

## Architecture

The system follows a modular architecture:

```
┌─────────────────────────────────────────────────────┐
│                   REST API Layer                     │
│              (FastAPI + WebSocket)                   │
└─────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────┐
│            Data Acquisition Manager                  │
│         (Unified data normalization)                 │
└─────────────────────────────────────────────────────┘
          │                │               │
┌─────────────┐   ┌──────────────┐  ┌────────────┐
│  OPC UA     │   │  OPC UA      │  │  Modbus    │
│  Server     │   │  Clients     │  │  Drivers   │
└─────────────┘   └──────────────┘  └────────────┘
                         │
┌─────────────────────────────────────────────────────┐
│              Database Storage Layer                  │
│         (SQLAlchemy + SQLite/PostgreSQL)            │
└─────────────────────────────────────────────────────┘
```

## Configuration

### OPC UA Server
Define data points in `config/opcua_server.yaml`:
```yaml
endpoint: "opc.tcp://0.0.0.0:4840/freeopcua/server/"
nodes:
  - node_id: "Temperature1"
    browse_name: "Temperature1"
    data_type: "float"
    initial_value: 25.0
    writable: false
```

### OPC UA Clients
Configure client connections in `config/opcua_clients.yaml`:
```yaml
clients:
  - name: "PLC1"
    endpoint: "opc.tcp://192.168.1.100:4840"
    subscriptions:
      - node_id: "ns=2;s=Temperature"
        publishing_interval: 1000
```

### Modbus Devices
Configure Modbus devices in `config/modbus_devices.yaml`:
```yaml
devices:
  - name: "TempSensor1"
    host: "192.168.1.50"
    port: 502
    registers:
      - name: "Temperature"
        register_type: "input_register"
        address: 0
        data_type: "float32"
```

## API Examples

### Get Real-time Data
```bash
curl http://localhost:8000/api/data/realtime
```

### Query Historical Data
```bash
curl -X POST http://localhost:8000/api/data/history \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "data_point_name": "Temperature",
    "start_time": "2024-01-01T00:00:00",
    "end_time": "2024-01-02T00:00:00"
  }'
```

### Read Modbus Register
```bash
curl -X POST http://localhost:8000/api/modbus/read \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "TempSensor1",
    "register_name": "Temperature"
  }'
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/
```

### Type Checking
```bash
mypy src/
```

## Documentation

- [Setup Guide](docs/SETUP.md) - Detailed installation and configuration
- [API Documentation](docs/API.md) - Complete API reference
- [Configuration Guide](docs/CONFIGURATION.md) - Configuration file formats
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and architecture

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
