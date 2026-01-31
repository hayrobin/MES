# Configuration Guide

This guide explains all configuration options for the Factory MES system.

## Configuration Files

The system uses YAML configuration files located in the `config/` directory:

- `opcua_server.yaml` - OPC UA server configuration
- `opcua_clients.yaml` - OPC UA client connections
- `modbus_devices.yaml` - Modbus device configurations
- `mes_config.yaml` - General system settings

## General Settings (mes_config.yaml)

### Application Settings

```yaml
MES_APP_NAME: Factory MES
MES_APP_VERSION: 1.0.0
MES_DEBUG: false
```

- `MES_APP_NAME`: Application display name
- `MES_APP_VERSION`: Version number
- `MES_DEBUG`: Enable debug mode (verbose logging, auto-reload)

### Logging Configuration

```yaml
MES_LOG_LEVEL: INFO
MES_JSON_LOGGING: false
```

- `MES_LOG_LEVEL`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `MES_JSON_LOGGING`: Use JSON format for structured logging

### Database Configuration

#### SQLite (Development)

```yaml
MES_DATABASE__TYPE: sqlite
MES_DATABASE__DATABASE: mes.db
```

#### PostgreSQL (Production)

```yaml
MES_DATABASE__TYPE: postgresql
MES_DATABASE__HOST: localhost
MES_DATABASE__PORT: 5432
MES_DATABASE__DATABASE: mes_db
MES_DATABASE__USERNAME: mes_user
MES_DATABASE__PASSWORD: mes_password
MES_DATABASE__POOL_SIZE: 5
MES_DATABASE__MAX_OVERFLOW: 10
```

- `TYPE`: Database type (sqlite or postgresql)
- `HOST`: Database server hostname
- `PORT`: Database server port
- `DATABASE`: Database name or file path
- `USERNAME`: Database username
- `PASSWORD`: Database password
- `POOL_SIZE`: Connection pool size
- `MAX_OVERFLOW`: Maximum pool overflow

### API Server Configuration

```yaml
MES_API__HOST: 0.0.0.0
MES_API__PORT: 8000
MES_API__RELOAD: false
MES_API__WORKERS: 1
MES_API__LOG_LEVEL: info
```

- `HOST`: Bind address (0.0.0.0 for all interfaces)
- `PORT`: API server port
- `RELOAD`: Enable auto-reload on code changes (development only)
- `WORKERS`: Number of worker processes
- `LOG_LEVEL`: API server log level

### Configuration File Paths

```yaml
MES_OPCUA_SERVER_CONFIG: config/opcua_server.yaml
MES_OPCUA_CLIENTS_CONFIG: config/opcua_clients.yaml
MES_MODBUS_DEVICES_CONFIG: config/modbus_devices.yaml
```

### Data Retention

```yaml
MES_HISTORICAL_DATA_RETENTION_DAYS: 30
```

- `HISTORICAL_DATA_RETENTION_DAYS`: Number of days to keep historical data

## OPC UA Server Configuration (opcua_server.yaml)

### Basic Settings

```yaml
endpoint: "opc.tcp://0.0.0.0:4840/freeopcua/server/"
server_name: "Factory MES OPC UA Server"
namespace: "http://factory.mes"
security_enabled: false
```

- `endpoint`: Server endpoint URL
- `server_name`: Server display name
- `namespace`: OPC UA namespace URI
- `security_enabled`: Enable security features

### Security Settings (Optional)

```yaml
security_enabled: true
certificate_path: "/path/to/certificate.pem"
private_key_path: "/path/to/private_key.pem"
```

### Node Configuration

Define nodes to expose via OPC UA:

```yaml
nodes:
  - node_id: "Temperature1"
    browse_name: "Temperature1"
    display_name: "Zone 1 Temperature"
    data_type: "float"
    initial_value: 25.0
    writable: false
    description: "Temperature sensor in zone 1 (°C)"
```

**Node Fields:**
- `node_id`: Unique identifier for the node
- `browse_name`: Name used for browsing
- `display_name`: Human-readable display name
- `data_type`: Data type (bool, int, float, double, string)
- `initial_value`: Initial value when server starts
- `writable`: Whether the node can be written to
- `description`: Node description

### Supported Data Types

- `bool` - Boolean (True/False)
- `int` - 32-bit integer
- `float` - 32-bit floating point
- `double` - 64-bit floating point
- `string` - Text string

## OPC UA Client Configuration (opcua_clients.yaml)

### Client Connection

```yaml
clients:
  - name: "PLC1"
    endpoint: "opc.tcp://192.168.1.100:4840"
    namespace_index: 2
    reconnect_interval: 5
    timeout: 10
    security_enabled: false
```

**Client Fields:**
- `name`: Unique client name
- `endpoint`: Server endpoint URL
- `namespace_index`: Default namespace index
- `reconnect_interval`: Seconds between reconnection attempts
- `timeout`: Connection timeout in seconds
- `security_enabled`: Enable security

### Subscriptions

Configure data change subscriptions:

```yaml
subscriptions:
  - node_id: "ns=2;s=Temperature"
    publishing_interval: 1000
  - node_id: "ns=2;s=Pressure"
    publishing_interval: 1000
```

**Subscription Fields:**
- `node_id`: Node ID to subscribe to
- `publishing_interval`: Update interval in milliseconds

### Node ID Formats

OPC UA supports different node ID formats:

- `ns=2;i=1234` - Numeric ID
- `ns=2;s=Temperature` - String ID
- `ns=2;g=12345678-1234-1234-1234-123456789012` - GUID
- `ns=2;b=AA==` - Opaque (base64)

## Modbus Configuration (modbus_devices.yaml)

### Device Connection

```yaml
devices:
  - name: "TempSensor1"
    host: "192.168.1.50"
    port: 502
    unit_id: 1
    polling_interval: 2
    timeout: 5
    reconnect_interval: 5
```

**Device Fields:**
- `name`: Unique device name
- `host`: Device IP address or hostname
- `port`: Modbus TCP port (default: 502)
- `unit_id`: Modbus unit/slave ID
- `polling_interval`: Polling interval in seconds
- `timeout`: Communication timeout in seconds
- `reconnect_interval`: Reconnection interval in seconds

### Register Configuration

```yaml
registers:
  - name: "Temperature"
    register_type: "input_register"
    address: 0
    count: 2
    data_type: "float32"
    scale: 1.0
    offset: 0.0
    unit: "°C"
```

**Register Fields:**
- `name`: Unique register name
- `register_type`: Type of register (see below)
- `address`: Register address (0-based)
- `count`: Number of registers to read
- `data_type`: Data type for decoding
- `scale`: Scale factor (value = raw * scale + offset)
- `offset`: Offset value
- `unit`: Engineering unit (optional)

### Register Types

- `coil` - Coil (read/write bit, FC1/FC5/FC15)
- `discrete_input` - Discrete input (read-only bit, FC2)
- `holding_register` - Holding register (read/write 16-bit, FC3/FC6/FC16)
- `input_register` - Input register (read-only 16-bit, FC4)

### Data Types

**Single Register (16-bit):**
- `uint16` - Unsigned 16-bit integer (0 to 65535)
- `int16` - Signed 16-bit integer (-32768 to 32767)
- `bool` - Boolean (coils and discrete inputs)

**Two Registers (32-bit):**
- `uint32` - Unsigned 32-bit integer
- `int32` - Signed 32-bit integer
- `float32` - 32-bit floating point (IEEE 754)

### Data Scaling Example

If a sensor outputs 0-32767 representing 0-100°C:

```yaml
- name: "Temperature"
  register_type: "input_register"
  address: 0
  count: 1
  data_type: "int16"
  scale: 0.00305  # 100 / 32767
  offset: 0.0
  unit: "°C"
```

## Environment Variables

All configuration can be overridden using environment variables:

```bash
# Application
export MES_APP_NAME="Factory MES"
export MES_DEBUG=true

# Database
export MES_DATABASE__TYPE=postgresql
export MES_DATABASE__HOST=db.example.com
export MES_DATABASE__PORT=5432

# API
export MES_API__PORT=8080
export MES_API__WORKERS=4
```

Environment variable format:
- Prefix: `MES_`
- Nested settings: Use double underscore `__`
- Example: `MES_DATABASE__HOST` sets `database.host`

## Docker Environment Variables

When using Docker, set environment variables in `docker-compose.yml`:

```yaml
services:
  mes:
    environment:
      - MES_DATABASE__TYPE=postgresql
      - MES_DATABASE__HOST=postgres
      - MES_DATABASE__DATABASE=mes_db
      - MES_LOG_LEVEL=INFO
```

Or use a `.env` file:

```bash
# .env file
MES_DATABASE__TYPE=postgresql
MES_DATABASE__HOST=postgres
MES_DATABASE__DATABASE=mes_db
```

Then reference in `docker-compose.yml`:

```yaml
services:
  mes:
    env_file:
      - .env
```

## Configuration Best Practices

### Security

1. **Never commit passwords** - Use environment variables
2. **Enable OPC UA security** in production
3. **Use strong database passwords**
4. **Restrict network access** with firewall rules

### Performance

1. **Adjust polling intervals** based on data change frequency
2. **Optimize database pool** size for concurrent connections
3. **Use appropriate worker count** (typically number of CPU cores)
4. **Configure data retention** to prevent database bloat

### Reliability

1. **Set appropriate timeouts** based on network conditions
2. **Configure reconnection intervals** to balance responsiveness and load
3. **Enable structured logging** for production debugging
4. **Monitor system status** regularly

## Configuration Validation

The system validates configuration on startup. Check logs for errors:

```
ERROR - Failed to load configuration from config/opcua_server.yaml: Invalid data type
```

Common configuration errors:
- Invalid YAML syntax
- Missing required fields
- Invalid data types
- Unreachable endpoints
- Invalid port numbers

## Hot Configuration Reload

Currently, configuration changes require application restart:

```bash
# Systemd
sudo systemctl restart mes

# Docker
docker-compose restart mes

# Development
# Stop with Ctrl+C and restart
python -m uvicorn src.api.main:app --reload
```

Future versions may support hot reload for certain configuration changes.

## Example Configurations

### Small Factory Setup

Single PLC and a few sensors:

```yaml
# opcua_clients.yaml
clients:
  - name: "MainPLC"
    endpoint: "opc.tcp://192.168.1.10:4840"
    subscriptions:
      - node_id: "ns=2;s=ProductionCount"
        publishing_interval: 2000

# modbus_devices.yaml
devices:
  - name: "TempSensor"
    host: "192.168.1.20"
    port: 502
    polling_interval: 5
    registers:
      - name: "Temperature"
        register_type: "input_register"
        address: 0
        data_type: "float32"
```

### Large Production Line

Multiple PLCs and many I/O modules:

```yaml
# opcua_clients.yaml
clients:
  - name: "PLC_Station1"
    endpoint: "opc.tcp://192.168.1.10:4840"
  - name: "PLC_Station2"
    endpoint: "opc.tcp://192.168.1.11:4840"
  - name: "PLC_Station3"
    endpoint: "opc.tcp://192.168.1.12:4840"

# modbus_devices.yaml with many devices...
```

Adjust system resources:
```yaml
MES_API__WORKERS: 8
MES_DATABASE__POOL_SIZE: 20
MES_DATABASE__MAX_OVERFLOW: 20
```
