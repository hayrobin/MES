 # README - MES Phase 2: Execution & Tracking

## Overview

This is **Phase 2** of the Manufacturing Execution System (MES), implementing the **Execution & Tracking Layer** for shop-floor production management.

## What's New in Phase 2

### Backend (`/mes_execution/`)
- ✅ 7 database tables for execution tracking
- ✅ RESTful API endpoints for work orders, production, materials, quality, equipment, and OEE
- ✅ OEE calculation engine with availability, performance, and quality metrics
- ✅ AI assistant service for natural language queries
- ✅ Comprehensive business logic layer

### Frontend (`/frontend/`)
- ✅ React 18 + TypeScript + Vite
- ✅ Shop-floor optimized UI (large buttons, high contrast, touch-friendly)
- ✅ Work Order Dashboard with card-based layout
- ✅ Real-time OEE Dashboard
- ✅ Floating AI Assistant
- ✅ Tailwind CSS styling

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start both backend and frontend
docker-compose up

# Access the applications:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
# Install dependencies
pip install -r requirements.txt

# Create database tables
python -c "from mes_execution.database import create_tables; create_tables()"

# Run server
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Architecture

```
MES/
├── mes_execution/           # Phase 2: Execution Layer (NEW)
│   ├── models/             # 7 database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── api/                # REST endpoints
│   └── database.py         # Database config
├── frontend/               # React + TypeScript UI (NEW)
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Application pages
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── package.json
├── docs/                   # Documentation (NEW)
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
└── docker-compose.yml      # Container orchestration
```

## Key Features

1. **Work Order Execution** - Track work orders from planned to completed
2. **Production Logging** - Real-time production data capture
3. **Material Traceability** - Batch, heat, lot, serial number tracking
4. **Quality Management** - Inspection and rejection logging
5. **Equipment Monitoring** - State tracking and downtime analysis
6. **OEE Dashboard** - Real-time Overall Equipment Effectiveness metrics
7. **AI Assistant** - Natural language production queries

## Documentation

- 📘 [Phase 2 Overview](docs/MES_PHASE_2_EXECUTION.md)
- 📗 [API Documentation](docs/API_EXECUTION.md)

## API Examples

```bash
# List work orders
curl http://localhost:8000/api/v1/execution/work-orders/

# Get OEE metrics
curl "http://localhost:8000/api/v1/execution/oee/realtime?equipment_id=1&ideal_cycle_time=1.5"

# Log production
curl -X POST http://localhost:8000/api/v1/execution/production/log \
  -H "Content-Type: application/json" \
  -d '{"work_order_id": 1, "produced_quantity": 100, "scrap_quantity": 5}'
```

## Technology Stack

**Backend:**
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite/PostgreSQL

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Query
- React Router

## Design Principles

### Shop-Floor Optimization
- ✅ **Large touch targets** - Minimum 60x60px buttons
- ✅ **High contrast** - Easy readability in industrial environments
- ✅ **Card-based layouts** - Visual clarity over tables
- ✅ **Mobile-first** - Responsive design for tablets
- ✅ **Touch-friendly** - Optimized for touch screens

## Development

```bash
# Backend hot reload
uvicorn main:app --reload

# Frontend hot reload
cd frontend && npm run dev

# Build frontend for production
cd frontend && npm run build
```

## Testing

```bash
# Backend (when tests are added)
pytest

# Frontend (when tests are added)
cd frontend && npm test
```

## Deployment

### Production Build

```bash
# Build frontend
cd frontend
npm run build

# Deploy backend with production WSGI server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

This is Phase 2 of a multi-phase MES implementation:
- ✅ **Phase 1** - OPC UA & Modbus connectivity
- ✅ **Phase 2** - Execution & Tracking (Current)
- 🔜 **Phase 3** - Advanced Analytics
- 🔜 **Phase 4** - Mobile Applications

## License

Copyright © 2026 - Manufacturing Execution System

## Support

For questions or issues:
1. Check the [documentation](docs/)
2. Review the [API docs](http://localhost:8000/docs)
3. Open an issue on GitHub
