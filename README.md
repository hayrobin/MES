 # Factory MES System

Manufacturing Execution System - Phase 1: Master Data & Configuration Layer

## Overview

This repository contains a comprehensive Manufacturing Execution System (MES) implementation with a layered architecture. **Phase 1** focuses on the Master Data & Configuration Layer - a foundation for future execution and analytics capabilities.

### 🎯 Phase 1: Configuration Layer (CURRENT)

**PHASE_1_CONFIG_ONLY** - This phase provides:
- ✅ Complete master data management for manufacturing configuration
- ✅ 8 core configuration modules (Enterprise, Equipment, Materials, Products, BoR, Quality, OEE/KPIs, Governance)
- ✅ REST APIs for all configuration entities (93 endpoints)
- ✅ Database models with audit trails and versioning
- ✅ Comprehensive seed data (247 sample records)
- ✅ Docker deployment ready

**What's NOT included in Phase 1:**
- ❌ Live telemetry integration
- ❌ Production execution tracking
- ❌ Real-time OEE calculations
- ❌ Work order management
- ❌ Scheduling and planning

## Architecture

### Layered Design

```
┌─────────────────────────────────────────────────┐
│  Layer 3+: Execution & Analytics (FUTURE)      │
│  - Production tracking, scheduling, real-time   │
│    monitoring, OEE calculations                 │
└─────────────────────────────────────────────────┘
                      ▲
                      │ Symbolic References
                      │
┌─────────────────────────────────────────────────┐
│  Layer 2: Configuration (PHASE 1 - CURRENT)     │
│  - Master data, definitions, targets            │
│  - Equipment, materials, products, BoR          │
│  - Quality codes, KPI definitions               │
└─────────────────────────────────────────────────┘
                      ▲
                      │ Reference Lookup
                      │
┌─────────────────────────────────────────────────┐
│  Layer 1: Connectivity (EXISTING - DO NOT TOUCH)│
│  - Modbus TCP/IP, OPC UA, REST APIs             │
│  - Telemetry database                           │
└─────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hayrobin/MES.git
cd MES
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Initialize database and load seed data**
```bash
python -m mes_config.services.seed_loader
```

5. **Run the application**
```bash
python main.py
```

The API will be available at: http://localhost:8000

- API Documentation: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

### Docker Deployment

**Using SQLite (Development):**
```bash
docker-compose -f docker-compose.sqlite.yml up -d
```

**Using PostgreSQL (Production):**
```bash
docker-compose up -d
```

## Phase 1 Modules

### Module 1: Enterprise & Organizational Configuration
- Enterprise, Sites, Areas, Lines
- Departments, Shift Calendars
- Units of Measure

### Module 2: Equipment & Capacity
- Equipment master with hierarchy
- Capacity definitions
- Symbolic linkage fields (OPC UA, Modbus references)

### Module 3: Material Master
- Material categories and hierarchy
- Material master with tracking requirements
- ERP integration references

### Module 4: Product & Production
- Product families and products
- Production standards
- Product-equipment compatibility

### Module 5: Bill of Resources
- Equipment routing
- Material requirements
- Tooling definitions
- Quality checkpoints

### Module 6: Quality Codes
- Rejection code categories
- Material rejection codes
- Production defect codes

### Module 7: OEE Targets & KPIs
- OEE targets by level
- KPI definitions and thresholds

### Module 8: Governance & Control
- Audit trails
- Versioning
- Approval workflows
- Role-based access control

## API Usage

All APIs follow RESTful conventions with consistent patterns:

```bash
# List all enterprises
curl http://localhost:8000/api/v1/mes-config/enterprise

# Get specific enterprise
curl http://localhost:8000/api/v1/mes-config/enterprise/1

# Create new enterprise
curl -X POST http://localhost:8000/api/v1/mes-config/enterprise \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_code": "ABC",
    "enterprise_name": "ABC Corp",
    "effective_from": "2024-01-01T00:00:00Z",
    "approval_status": "DRAFT",
    "created_by": "admin",
    "is_active": 1
  }'
```

See [API_MES_CONFIG.md](docs/API_MES_CONFIG.md) for complete API reference.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mes_config tests/

# Run specific test file
pytest tests/mes_config/test_models.py
```

## Documentation

- [MES Phase 1 Configuration Guide](docs/MES_PHASE_1_CONFIGURATION.md) - Complete module documentation
- [Architecture Layers](docs/ARCHITECTURE_LAYERS.md) - System layering and integration patterns
- [API Reference](docs/API_MES_CONFIG.md) - Complete API documentation

## Data Model Summary

Phase 1 includes **33 database tables** across all modules:

- Enterprise: 7 tables
- Equipment: 2 tables
- Materials: 2 tables
- Products: 3 tables
- Bill of Resources: 4 tables
- Quality: 3 tables
- OEE/KPIs: 2 tables
- Governance: 3 tables
- Audit: 1 table

See [database schema documentation](docs/MES_PHASE_1_CONFIGURATION.md#database-schema) for details.

## Project Structure

```
MES/
├── mes_config/              # Main configuration layer package
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── api/                 # FastAPI route handlers
│   ├── services/            # Business logic and utilities
│   └── seed_data/           # Sample master data
├── docs/                    # Documentation
├── tests/                   # Test suite
├── main.py                  # FastAPI application
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # PostgreSQL deployment
└── requirements.txt         # Python dependencies
```

## Development

### Code Style

All code includes `PHASE_1_CONFIG_ONLY` markers to clearly identify configuration-only functionality.

### Adding New Configuration Entities

1. Create model in `mes_config/models/`
2. Create schemas in `mes_config/schemas/`
3. Create API routes in `mes_config/api/`
4. Add seed data in `mes_config/seed_data/`
5. Update tests in `tests/mes_config/`

## License

Copyright © 2024 MES Development Team

## Contact

For questions or support, please open an issue on GitHub
