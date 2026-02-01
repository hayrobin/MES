"""
Migrations README
"""

# MES Execution - Database Migrations

This directory contains database migration scripts for the MES Execution Layer.

## Schema Creation

The database schema is defined in the SQLAlchemy models in `mes_execution/models/`.

To create the database tables, use the `create_tables()` function from `mes_execution/database.py`:

```python
from mes_execution.database import create_tables

create_tables()
```

## Tables Created

1. `mes_execution_work_order` - Work Order Execution State
2. `mes_execution_operation` - Operation Execution Log
3. `mes_execution_production_log` - Production Log (Time-series)
4. `mes_execution_material_consumption` - Material Consumption Log
5. `mes_execution_quality_inspection` - Quality Inspection & Rejection Log
6. `mes_execution_equipment_state` - Equipment State Tracking
7. `mes_execution_oee_snapshot` - OEE Calculation Cache

## Migration Strategy

For production environments, consider using Alembic for versioned migrations:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Development

For development, the tables can be created automatically when starting the application.
