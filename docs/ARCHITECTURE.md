# Architecture Documentation

This document describes the architecture and design decisions of the Factory MES system.

## System Overview

The Factory MES system is a modular, asynchronous Manufacturing Execution System designed for industrial environments. It provides a unified platform for data acquisition, storage, and access across multiple industrial protocols.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│              (Web Apps, Mobile, SCADA, Analytics)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │   REST API      │
                    │   (FastAPI)     │
                    └────────┬────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Devices    │  │     Data     │  │    Status    │          │
│  │   Routes     │  │    Routes    │  │   Routes     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                   Data Acquisition Layer                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         Data Acquisition Manager                      │       │
│  │  • Data normalization  • Validation  • Callbacks     │       │
│  └───────────────────────┬──────────────────────────────┘       │
└──────────────────────────┼──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼───────┐  ┌───────▼────────┐  ┌─────▼────────┐
│   OPC UA      │  │   OPC UA       │  │   Modbus     │
│   Server      │  │   Clients      │  │   Drivers    │
│               │  │                │  │              │
│ • Expose data │  │ • Connect PLCs │  │ • Poll I/O   │
│ • Handle      │  │ • Subscribe    │  │ • Read/Write │
│   requests    │  │ • Auto-recon.  │  │ • FC1-FC16   │
└───────┬───────┘  └───────┬────────┘  └─────┬────────┘
        │                  │                  │
        │                  │                  │
┌───────▼──────────────────▼──────────────────▼────────┐
│              Database Storage Layer                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │
│  │  Devices   │  │  Realtime  │  │ Historical │     │
│  │  Registry  │  │    Data    │  │    Data    │     │
│  └────────────┘  └────────────┘  └────────────┘     │
│         SQLite (Dev) / PostgreSQL (Prod)             │
└──────────────────────────────────────────────────────┘
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Industrial Devices    │
              │  PLCs, Sensors, VFDs,   │
              │  I/O Modules, SCADA     │
              └─────────────────────────┘
```

## Layer Architecture

### 1. Protocol Layer

The protocol layer handles communication with industrial devices using standard protocols.

#### OPC UA Server
- **Purpose**: Expose factory data to external OPC UA clients
- **Technology**: asyncua library
- **Features**:
  - Configurable address space
  - Read/write access control
  - Standard OPC UA information model
  - Asynchronous operation

#### OPC UA Client
- **Purpose**: Connect to PLCs and SCADA systems
- **Technology**: asyncua library
- **Features**:
  - Multi-server connections
  - Data change subscriptions
  - Automatic reconnection
  - Browse address space
  - Batch read operations

#### Modbus TCP/IP Driver
- **Purpose**: Communicate with Modbus devices
- **Technology**: pymodbus library
- **Features**:
  - All standard function codes (FC1-FC16)
  - Configurable polling
  - Data type conversion
  - Scale and offset support
  - Connection management

### 2. Data Acquisition Layer

Central data management and normalization layer.

**Responsibilities:**
- Unified data interface for all protocols
- Data validation and type conversion
- Quality checking
- Timestamp synchronization
- Callback management

**Design Pattern**: Observer pattern for data updates

### 3. Storage Layer

Persistent data storage with time-series support.

**Database Schema:**

```
┌─────────────┐
│   Devices   │  (Device registry)
├─────────────┤
│ id          │
│ name        │
│ device_type │
│ status      │
│ config      │
└──────┬──────┘
       │
       ├──────┐
       │      │
┌──────▼──────────┐    ┌──────────────────┐
│   Data Points   │    │  Realtime Data   │
├─────────────────┤    ├──────────────────┤
│ id              │    │ device_id        │
│ device_id       │    │ data_point_name  │
│ name            │    │ value            │
│ address         │    │ quality          │
│ data_type       │    │ timestamp        │
└─────────────────┘    └──────────────────┘
                              │
                       ┌──────▼───────────┐
                       │ Historical Data  │
                       ├──────────────────┤
                       │ device_id        │
                       │ data_point_name  │
                       │ value            │
                       │ quality          │
                       │ timestamp        │
                       └──────────────────┘
```

**Features:**
- Dual storage: Real-time (latest values) + Historical (time-series)
- Efficient indexing for time-series queries
- Data retention policies
- Support for SQLite and PostgreSQL

### 4. API Layer

RESTful API for system integration and control.

**Technology:**
- FastAPI framework
- Pydantic for data validation
- Async route handlers
- Auto-generated documentation

**Endpoints:**
- Device management
- Data access (realtime/historical)
- Protocol operations (OPC UA, Modbus)
- System status and health

## Design Patterns

### 1. Asynchronous Architecture

**Pattern**: Async/await with asyncio

**Benefits:**
- Non-blocking I/O
- High concurrency
- Efficient resource usage

**Implementation:**
```python
async def poll_device():
    while running:
        data = await device.read()
        await process_data(data)
        await asyncio.sleep(interval)
```

### 2. Dependency Injection

**Pattern**: FastAPI dependency injection

**Benefits:**
- Loose coupling
- Testability
- Shared resources

**Implementation:**
```python
def get_storage() -> DatabaseStorage:
    return app_state.storage

@router.get("/devices")
async def list_devices(storage: DatabaseStorage = Depends(get_storage)):
    return await storage.get_all_devices()
```

### 3. Configuration as Code

**Pattern**: YAML configuration with Pydantic models

**Benefits:**
- Type safety
- Validation
- Documentation
- Version control

### 4. Repository Pattern

**Pattern**: Database abstraction layer

**Benefits:**
- Separation of concerns
- Easy testing
- Database portability

## Concurrency Model

### Background Tasks

The system runs multiple concurrent tasks:

```python
# OPC UA Server
server_task = asyncio.create_task(opcua_server.start())

# OPC UA Clients (one per client)
for client in opcua_clients:
    client_task = asyncio.create_task(client.run())

# Modbus Drivers (one per device)
for driver in modbus_drivers:
    await driver.start()  # Creates internal polling task
```

### Task Lifecycle

```
┌─────────────┐
│  Application │
│    Start     │
└──────┬───────┘
       │
       ├─────► Initialize database
       │
       ├─────► Start data manager
       │
       ├─────► Start protocol tasks
       │       (OPC UA server, clients, Modbus drivers)
       │
       ├─────► Run API server
       │
       │       [Application Running]
       │
       ├─────► Shutdown signal
       │
       ├─────► Stop protocol tasks
       │
       ├─────► Stop data manager
       │
       └─────► Close database
```

## Data Flow

### Write Path (Device → Database)

```
Device Data
    │
    ▼
Protocol Driver (OPC UA/Modbus)
    │
    ▼
Data Point Creation
    │
    ▼
Data Acquisition Manager
    │
    ├─► Validation
    ├─► Normalization
    └─► Quality Check
         │
         ▼
   Callbacks
         │
         ├─► Update Realtime Data (upsert)
         │
         └─► Insert Historical Data (append)
              │
              ▼
         Database
```

### Read Path (API → Client)

```
API Request
    │
    ▼
Route Handler
    │
    ▼
Database Query
    │
    ▼
Data Serialization
    │
    ▼
API Response
```

## Error Handling

### Hierarchical Exception Model

```
MESException (base)
    │
    ├─► OPCUAException
    │     ├─► OPCUAConnectionError
    │     ├─► OPCUAReadError
    │     └─► OPCUAWriteError
    │
    ├─► ModbusException
    │     ├─► ModbusConnectionError
    │     ├─► ModbusReadError
    │     └─► ModbusWriteError
    │
    ├─► ConfigurationError
    ├─► DataAcquisitionError
    └─► StorageError
```

### Error Recovery Strategies

**Connection Errors:**
- Automatic reconnection with exponential backoff
- Continue operation with degraded functionality
- Log errors for monitoring

**Data Errors:**
- Mark data quality as "bad"
- Continue collecting other data points
- Alert operators

**Configuration Errors:**
- Fail fast on startup
- Clear error messages
- Validation before application

## Performance Considerations

### Database Optimization

1. **Indexing Strategy:**
   - Primary keys for all tables
   - Composite indexes for frequent queries
   - Time-based indexes for historical data

2. **Connection Pooling:**
   - Configurable pool size
   - Async-friendly connection management

3. **Batch Operations:**
   - Bulk inserts for historical data
   - Upsert operations for real-time data

### Protocol Optimization

1. **OPC UA:**
   - Subscriptions instead of polling
   - Batch read operations
   - Efficient data change notifications

2. **Modbus:**
   - Configurable polling intervals
   - Read multiple registers in single request
   - Connection reuse

### API Optimization

1. **Async Handlers:**
   - Non-blocking database operations
   - Concurrent request handling

2. **Response Caching:**
   - (Future) Cache frequently accessed data
   - Configurable TTL

## Security Architecture

### Current Implementation

- No authentication (suitable for isolated networks)
- Database credentials in environment variables
- CORS enabled for development

### Production Recommendations

1. **API Security:**
   - OAuth2 or API key authentication
   - Rate limiting
   - HTTPS/TLS encryption

2. **OPC UA Security:**
   - Certificate-based authentication
   - Message signing and encryption
   - User access control

3. **Network Security:**
   - Firewall rules
   - VPN for remote access
   - Network segmentation

4. **Database Security:**
   - Strong passwords
   - Encrypted connections
   - Regular backups
   - Principle of least privilege

## Scalability

### Vertical Scaling

- Increase worker processes
- Increase database connection pool
- More CPU cores for concurrent tasks

### Horizontal Scaling

**Current Limitations:**
- Shared state (in-memory)
- Single database instance

**Future Enhancements:**
- Stateless API servers (load balanced)
- Message queue for data ingestion
- Database replication
- Distributed caching (Redis)

## Monitoring and Observability

### Logging

- Structured logging (JSON format option)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Context information in logs

### Metrics (Planned)

- Data points collected per second
- API request latency
- Database query performance
- Protocol connection status
- Error rates

### Health Checks

- `/api/status/health` - Simple health check
- `/api/status` - Detailed system status
- Docker health check support

## Future Architecture Enhancements

### Planned Features

1. **Message Queue:**
   - Decouple data ingestion from storage
   - Buffer for high-volume data
   - Retry mechanism

2. **Event System:**
   - Alarm management
   - Production events
   - Audit trail

3. **WebSocket Support:**
   - Real-time data streaming
   - Push notifications

4. **Analytics:**
   - Statistical process control
   - Trend analysis
   - Predictive maintenance

5. **Additional Protocols:**
   - MQTT
   - EtherNet/IP
   - Profinet

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API | FastAPI | REST API framework |
| OPC UA | asyncua | OPC UA protocol |
| Modbus | pymodbus | Modbus TCP protocol |
| Database | SQLAlchemy | ORM and query builder |
| DB Engine | SQLite/PostgreSQL | Data storage |
| Async | asyncio | Concurrency |
| Config | Pydantic | Settings management |
| Validation | Pydantic | Data validation |
| Container | Docker | Deployment |
| Server | Uvicorn | ASGI server |

## Design Principles

1. **Modularity**: Each protocol driver is independent
2. **Asynchronous**: Non-blocking I/O throughout
3. **Configurability**: Behavior controlled by config files
4. **Reliability**: Auto-reconnection and error handling
5. **Observability**: Comprehensive logging and status
6. **Testability**: Dependency injection and mocking
7. **Production-Ready**: Docker support, health checks
8. **Standards-Compliant**: Standard protocols and patterns
