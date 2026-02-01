# MES PHASE 2 – EXECUTION & TRACKING

## Overview

Phase 2 of the Manufacturing Execution System (MES) implements the **Execution & Tracking Layer**, enabling shop-floor operators to:

- Execute work orders and track production in real-time
- Capture material consumption with full traceability
- Record quality inspections and rejections
- Monitor equipment states and downtime
- View real-time OEE (Overall Equipment Effectiveness) metrics
- Interact with an AI assistant for production queries

## Architecture

### Backend (`/mes_execution/`)

**Technology Stack:**
- FastAPI for REST APIs
- SQLAlchemy ORM for database operations
- PostgreSQL/SQLite for data persistence
- Pydantic for data validation

**Components:**
1. **Models** - 7 database tables for execution data
2. **Schemas** - Pydantic models for API request/response
3. **Services** - Business logic layer
4. **APIs** - RESTful endpoints

### Frontend (`/frontend/`)

**Technology Stack:**
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- React Query for data fetching
- React Router for navigation
- Recharts for data visualization

**Design Philosophy:**
- **Shop-floor optimized** - Large buttons (60x60px minimum), high contrast colors
- **Card-based layouts** - Easy visual scanning
- **Mobile-first** - Responsive design for tablets and mobile devices
- **Touch-friendly** - Optimized for touch screens

## Key Features

### 1. Work Order Execution

**Dashboard View:**
- Card grid layout showing all work orders
- Status badges with color coding (green=running, orange=paused, etc.)
- Progress bars showing completion percentage
- Large action buttons: START, PAUSE, COMPLETE

**Detail View:**
- Operation sequence tracking
- Per-operation production capture
- Real-time progress updates

### 2. Material Consumption Tracking

- Capture actual material usage
- Full traceability: Batch, Heat, Lot, Serial numbers
- Compare planned vs. actual consumption
- Link to operations and work orders

### 3. Quality Management

- Pass/Fail inspection recording
- Rejection code tracking
- Quantity rejected logging
- Inspector identification
- Remarks and comments

### 4. Equipment State Monitoring

- Real-time equipment state display
- State changes: RUNNING, IDLE, DOWN, SETUP, MAINTENANCE
- Downtime reason tracking
- Equipment timeline visualization

### 5. OEE Dashboard

**Metrics Displayed:**
- **Availability** - Planned vs. actual run time
- **Performance** - Ideal vs. actual cycle time
- **Quality** - Good pieces vs. total pieces
- **Overall OEE** - Combined metric (color-coded)

**Breakdown:**
- Shift-wise production charts
- Actual vs. target comparison
- Downtime reason analysis
- Equipment comparison

### 6. AI Assistant

**Features:**
- Floating chat interface (bottom-right)
- Natural language queries
- Quick question buttons
- Role-based data filtering

**Example Queries:**
- "What is running now?"
- "Which orders are delayed?"
- "Show today's OEE"

## Database Schema

### Tables Created

1. **mes_execution_work_order** - Work order execution state
2. **mes_execution_operation** - Operation execution log
3. **mes_execution_production_log** - Time-series production data
4. **mes_execution_material_consumption** - Material usage tracking
5. **mes_execution_quality_inspection** - Quality and rejection data
6. **mes_execution_equipment_state** - Equipment state timeline
7. **mes_execution_oee_snapshot** - Pre-calculated OEE metrics

## API Endpoints

See [API_EXECUTION.md](./API_EXECUTION.md) for complete API documentation.

**Base URL:** `/api/v1/execution`

**Main Endpoints:**
- `/work-orders/` - Work order management
- `/production/` - Production logging
- `/materials/` - Material consumption
- `/quality/` - Quality inspections
- `/equipment/` - Equipment status
- `/oee/` - OEE calculations

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL or SQLite

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python -c "from mes_execution.database import create_tables; create_tables()"

# Start the FastAPI server
python main.py
```

Server runs on: http://localhost:8000

API documentation: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: http://localhost:5173

### Production Build

```bash
# Build frontend
cd frontend
npm run build

# The built files will be in frontend/dist/
```

## User Roles

- **OPERATOR** - Execute work orders, enter production data
- **SUPERVISOR** - View all data, monitor operations (read-only)
- **ADMIN** - Full access to all features

## Integration Points

### Layer 1 (OPC UA/Modbus) - Read-Only
- Equipment master data
- Equipment capacity and cycle times
- Real-time equipment signals

### Layer 2 (Configuration) - Read-Only
- Product master
- Material master
- Bill of Resources (BoR)
- Rejection codes
- Shift calendar
- Line configuration

## Performance Considerations

- **Production logging** - Indexed by timestamp and work order
- **OEE calculations** - Cached in snapshot table
- **Real-time queries** - Optimized with database indexes
- **Frontend** - React Query caching reduces API calls

## Security

- Role-based access control on API endpoints
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend integration

## Future Enhancements

- WebSocket support for real-time updates
- Mobile app for operators
- Advanced analytics and predictive maintenance
- Integration with ERP systems
- Barcode/RFID scanning for material tracking

## Support

For issues or questions, refer to:
- [User Guide for Operators](./USER_GUIDE_OPERATORS.md)
- [OEE Methodology](./OEE_METHODOLOGY.md)
- [API Documentation](./API_EXECUTION.md)
