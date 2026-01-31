# MES Architecture: Layered System Design

**PHASE_1_CONFIG_ONLY** - This document describes the complete MES architecture with emphasis on Phase 1 boundaries.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Layer Definitions](#layer-definitions)
3. [Layer 1: Connectivity & Data Acquisition](#layer-1-connectivity--data-acquisition)
4. [Layer 2: Configuration (Phase 1)](#layer-2-configuration-phase-1)
5. [Layer 3+: Future Layers](#layer-3-future-layers)
6. [Integration Patterns](#integration-patterns)
7. [Data Flow Rules](#data-flow-rules)
8. [Layer Boundaries](#layer-boundaries)
9. [Phase Isolation](#phase-isolation)
10. [Additive-Only Approach](#additive-only-approach)

---

## Architecture Overview

The MES system is built using a **layered architecture** where each layer has a specific responsibility and clear boundaries. Layers communicate through well-defined interfaces, and higher layers can read from lower layers, but NOT modify them.

### MES Layer Stack

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Analytics & Reporting (Future)                    │
│  - Dashboards, KPI calculations, trends, reports            │
└─────────────────────────────────────────────────────────────┘
                            ↑ Reads
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Execution & Scheduling (Future)                   │
│  - Work orders, production tracking, inventory, quality     │
└─────────────────────────────────────────────────────────────┘
                            ↑ Reads
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Configuration (Phase 1) ◄─ WE ARE HERE            │
│  - Master data, reference data, organizational structure    │
└─────────────────────────────────────────────────────────────┘
                            ↑ Symbolic Linkage (strings only)
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Connectivity & Data Acquisition (Existing)        │
│  - OPC UA, Modbus, SCADA, sensor data collection            │
│  - DO NOT TOUCH - Already deployed and operational          │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

✅ **Separation of Concerns** - Each layer has a single, well-defined responsibility  
✅ **Read-Only Dependencies** - Higher layers can read from lower layers but cannot modify them  
✅ **Symbolic Linkage** - Layers reference each other via string keys, not direct database connections  
✅ **Phase Isolation** - Each implementation phase is isolated; new phases add capabilities without changing existing layers  
✅ **Additive-Only** - New phases add new tables/fields but never modify existing ones  
✅ **No Cross-Phase Transactions** - Transactions are scoped to a single layer  

---

## Layer Definitions

### Layer Responsibility Matrix

| Layer | Responsibility | Data Type | Mutability | Phase |
|-------|---------------|-----------|------------|-------|
| **Layer 1** | Data acquisition from physical equipment | Live telemetry | High frequency | Existing (DO NOT TOUCH) |
| **Layer 2** | Master data & configuration | Reference data | Low frequency | **Phase 1 (Current)** |
| **Layer 3** | Execution & transactional data | Transactional | Medium frequency | Phase 2 (Future) |
| **Layer 4** | Analytics & aggregated metrics | Derived/calculated | Read-only | Phase 3+ (Future) |

---

## Layer 1: Connectivity & Data Acquisition

**Status:** Existing deployment - **DO NOT TOUCH**

### Responsibility
Collect real-time data from manufacturing equipment via industrial protocols.

### Technologies
- **OPC UA Servers** - Equipment connectivity
- **Modbus Gateways** - PLC communication
- **SCADA Systems** - Process monitoring
- **Sensor Networks** - Environmental/quality sensors

### Data Collected
- Equipment status (running, idle, down, alarmed)
- Process variables (temperature, pressure, flow, speed)
- Counter values (production counts, cycle counts)
- Alarm/event logs
- Quality measurements (dimensional, electrical, chemical)

### Storage
- **Time-series database** (e.g., InfluxDB, TimescaleDB)
- **High-frequency writes** (1-10 second intervals)
- **Tag-based data model** (OPC tag namespace)

### Example Data
```json
{
  "timestamp": "2025-02-01T10:30:45.123Z",
  "tag": "CNC.Mill001.Status",
  "value": "RUNNING",
  "quality": "GOOD"
}
```

### Integration with Phase 1 (Layer 2)

**CRITICAL:** Layer 1 and Layer 2 are **COMPLETELY INDEPENDENT**.

Phase 1 (Layer 2) **ONLY** stores symbolic references to Layer 1:

```sql
-- Layer 2 stores STRINGS ONLY (not active connections)
CREATE TABLE mes_config_equipment_master (
  equipment_id INTEGER PRIMARY KEY,
  equipment_code VARCHAR(50),
  opc_namespace VARCHAR(200),     -- e.g., "ns=2;s=CNC.Mill001"
  opc_node_id VARCHAR(200),        -- e.g., "ns=2;i=1001"
  modbus_tag_ref VARCHAR(100),     -- e.g., "40001-40010"
  scada_tag_ref VARCHAR(100)       -- e.g., "CNC_MILL_001"
);
```

### What Layer 2 CANNOT Do
❌ Subscribe to OPC UA tags  
❌ Read Modbus registers  
❌ Query time-series data  
❌ Receive real-time updates  
❌ Trigger based on equipment events  

### What Layer 2 CAN Do
✅ Store equipment definitions with symbolic OPC/Modbus references  
✅ Define which tags should be monitored (configuration for future phases)  
✅ Provide equipment metadata (manufacturer, model, location)  
✅ Define equipment hierarchy (parent-child relationships)  

### Future Integration (Phase 2+)
When execution tracking is implemented (Phase 2), a **separate integration service** will:
1. Read equipment definitions from Layer 2 (equipment_code, opc_namespace)
2. Use those references to subscribe to Layer 1 OPC UA tags
3. Write execution data to Layer 3 tables (NOT Layer 1 or Layer 2)

```
Layer 1 (OPC UA)  ──reads──>  Integration Service  ──writes──>  Layer 3 (Execution)
                                      ↑
                                   Reads config from Layer 2
```

---

## Layer 2: Configuration (Phase 1)

**Status:** **CURRENT IMPLEMENTATION** - Phase 1

### Responsibility
Store all master data and reference data required for manufacturing operations.

### Scope: 7 Modules, 33 Tables

#### Module 1: Enterprise & Organizational Configuration
**Tables:**
- `mes_config_enterprise` - Company master data
- `mes_config_site` - Manufacturing sites/plants
- `mes_config_area` - Production areas within sites
- `mes_config_line` - Production lines
- `mes_config_department` - Organizational departments
- `mes_config_shift_calendar` - Shift definitions (templates only)
- `mes_config_unit_of_measure` - UOM master data

**Purpose:** Define the organizational structure and operational parameters.

---

#### Module 2: Equipment & Capacity Definition
**Tables:**
- `mes_config_equipment_master` - Equipment hierarchy with **symbolic linkage**
- `mes_config_equipment_capacity` - Rated capacity (theoretical/design)

**Purpose:** Define equipment assets and their design capabilities.

**CRITICAL:** Equipment capacity is **RATED/DESIGN CAPACITY ONLY**, not actual performance monitoring.

---

#### Module 3: Material Master
**Tables:**
- `mes_config_material_category` - Hierarchical material categories
- `mes_config_material_master` - All materials with tracking configuration

**Purpose:** Define materials used in production and tracking requirements.

---

#### Module 4: Product & Production
**Tables:**
- `mes_config_product_family` - Product grouping/grades
- `mes_config_product_master` - Finished products
- `mes_config_product_equipment_compatibility` - Product-equipment mapping

**Purpose:** Define products and which equipment can produce them.

---

#### Module 5: Bill of Resources (BoR)
**Tables:**
- `mes_config_bill_of_resources` - Manufacturing routing
- `mes_config_bor_material` - Material consumption standards
- `mes_config_bor_tooling` - Tooling requirements
- `mes_config_bor_quality_checkpoint` - Quality checkpoint definitions

**Purpose:** Define standard routing, materials, tooling, and quality requirements per product.

---

#### Module 6: Quality & Rejection Codes
**Tables:**
- `mes_config_rejection_code_category` - Categories for rejection codes
- `mes_config_material_rejection_code` - Material-specific codes
- `mes_config_production_rejection_code` - Production defect codes

**Purpose:** Define possible rejection reasons and defect classifications.

---

#### Module 7: OEE Targets & KPI Configuration
**Tables:**
- `mes_config_oee_target` - Target configuration by product/line/machine/site
- `mes_config_kpi_definition` - KPI metadata and formulas (as text)

**Purpose:** Define performance targets and KPI calculation methods.

**CRITICAL:** This is **TARGET CONFIGURATION ONLY**, not actual KPI calculations or measurements.

---

### Governance Framework (All Modules)
**Tables:**
- `mes_config_audit_trail` - Complete change history
- `mes_config_user_role` - Role definitions
- `mes_config_role_permission` - Role-based access control

**Purpose:** Version control, approval workflows, and audit trails.

### Data Characteristics

| Characteristic | Value |
|---------------|-------|
| **Mutability** | Low frequency (daily/weekly updates) |
| **Volume** | Small to medium (thousands of records) |
| **Transactions** | CRUD operations only |
| **Real-time** | NO - all static configuration |
| **Dependencies** | Self-contained (no external system reads) |

### API Access
All Layer 2 data is accessible via REST API:
- **Base URL:** `/api/v1/mes-config`
- **Operations:** Full CRUD (Create, Read, Update, Delete)
- **Authentication:** Optional (configurable)
- **Pagination:** Supported (skip/limit parameters)
- **Filtering:** Supported (by status, type, active flag)

### Example API Calls
```bash
# List all sites
GET /api/v1/mes-config/sites?skip=0&limit=100

# Get specific equipment
GET /api/v1/mes-config/equipment/1

# Create new product
POST /api/v1/mes-config/products
{
  "product_code": "PROD-NEW-001",
  "product_name": "New Product",
  "base_uom": "EA",
  "created_by": "admin"
}

# Update OEE target
PUT /api/v1/mes-config/oee-targets/1
{
  "availability_target": 92.00,
  "updated_by": "manager"
}
```

---

## Layer 3+: Future Layers

### Layer 3: Execution & Scheduling (Phase 2 - Future)

**NOT IMPLEMENTED YET**

#### Planned Scope
- **Work Orders** - Production orders with scheduling
- **Production Tracking** - Actual production vs. planned
- **Inventory Management** - Material consumption, stock levels
- **Quality Execution** - Actual inspection records, test results
- **Genealogy** - Batch/lot traceability
- **Shop Floor Interface** - Operator job instructions

#### Planned Tables (Future)
- `mes_exec_work_order` - Production orders
- `mes_exec_production_record` - Actual production data
- `mes_exec_material_transaction` - Material movements
- `mes_exec_quality_inspection` - Inspection results
- `mes_exec_equipment_event` - Equipment events (downtime, changeover)
- `mes_exec_batch_genealogy` - Material traceability

#### Integration with Layer 2
Layer 3 will **READ** from Layer 2:

```sql
-- Work order references product from Layer 2
CREATE TABLE mes_exec_work_order (
  work_order_id INTEGER PRIMARY KEY,
  work_order_number VARCHAR(50) UNIQUE,
  product_code VARCHAR(50),  -- References Layer 2 product_code
  equipment_code VARCHAR(50), -- References Layer 2 equipment_code
  planned_quantity DECIMAL,
  status VARCHAR(20)  -- PLANNED, RELEASED, IN_PROGRESS, COMPLETED
);
```

#### Integration with Layer 1
Layer 3 will **READ** from Layer 1 via integration service:

```python
# Future integration service (Phase 2)
class ProductionTracker:
    def __init__(self):
        # Read equipment config from Layer 2
        equipment = layer2_api.get_equipment(code="CNC-MILL-001")
        opc_tag = equipment["opc_namespace"]
        
        # Subscribe to Layer 1 OPC UA
        self.opc_client.subscribe(opc_tag, callback=self.on_equipment_event)
    
    def on_equipment_event(self, tag, value):
        # Write to Layer 3 execution tables
        layer3_db.insert("mes_exec_equipment_event", {
            "equipment_code": "CNC-MILL-001",
            "event_type": "STATUS_CHANGE",
            "event_value": value,
            "timestamp": datetime.now()
        })
```

---

### Layer 4: Analytics & Reporting (Phase 3+ - Future)

**NOT IMPLEMENTED YET**

#### Planned Scope
- **KPI Calculations** - Actual OEE, yield, throughput, etc.
- **Dashboards** - Real-time manufacturing dashboards
- **Trends** - Historical performance analysis
- **Reports** - Production reports, quality reports, downtime analysis
- **Predictive Analytics** - Equipment health, quality predictions

#### Planned Tables (Future)
- `mes_analytics_kpi_value` - Calculated KPI values
- `mes_analytics_oee_measurement` - Actual OEE measurements
- `mes_analytics_equipment_performance` - Equipment performance metrics
- `mes_analytics_quality_metrics` - Quality performance metrics

#### Integration with Layer 2 & Layer 3
Layer 4 will **READ** from both:

```sql
-- OEE calculation references target from Layer 2 and actuals from Layer 3
CREATE VIEW v_oee_actual_vs_target AS
SELECT 
  -- Layer 2: Target configuration
  t.target_type,
  t.availability_target,
  t.performance_target,
  t.quality_target,
  t.oee_target,
  
  -- Layer 3: Actual production data (future)
  a.availability_actual,
  a.performance_actual,
  a.quality_actual,
  a.oee_actual,
  
  -- Layer 4: Variance calculation
  (a.oee_actual - t.oee_target) AS oee_variance
FROM mes_config_oee_target t
JOIN mes_exec_production_record p ON t.product_id = p.product_id
JOIN mes_analytics_oee_measurement a ON p.work_order_id = a.work_order_id;
```

---

## Integration Patterns

### Pattern 1: Symbolic Linkage (Layer 1 ↔ Layer 2)

**Description:** Layer 2 stores string references to Layer 1 entities, but does NOT connect directly.

**Example:**
```python
# Layer 2: Equipment definition
equipment = {
  "equipment_code": "CNC-MILL-001",
  "equipment_name": "CNC Milling Machine #1",
  "opc_namespace": "ns=2;s=CNC.Mill001",  # STRING ONLY
  "modbus_tag_ref": "40001-40010"          # STRING ONLY
}

# Future integration service reads this config
# and uses it to connect to Layer 1
integration_service = EquipmentConnector()
integration_service.connect_to_opc(equipment["opc_namespace"])
```

**Data Flow:**
```
Layer 2 (Config) ──symbolic reference──> Integration Service ──reads──> Layer 1 (Live Data)
```

---

### Pattern 2: Reference Lookup (Layer 3 → Layer 2)

**Description:** Layer 3 stores foreign key references to Layer 2 via string codes (not integer IDs).

**Example:**
```python
# Layer 3: Work order (future)
work_order = {
  "work_order_number": "WO-12345",
  "product_code": "PROD-BRK-001",      # References Layer 2 product_code
  "equipment_code": "CNC-MILL-001",    # References Layer 2 equipment_code
  "planned_quantity": 100
}

# To get full product details, query Layer 2
product = layer2_api.get("/api/v1/mes-config/products", params={"product_code": "PROD-BRK-001"})
print(f"Product Name: {product['product_name']}")
print(f"Standard Cycle Time: {product['standard_cycle_time']} seconds")
```

**Data Flow:**
```
Layer 3 (Execution) ──code reference──> Layer 2 (Config) [Read-Only]
```

---

### Pattern 3: Aggregation (Layer 4 → Layer 3 → Layer 2)

**Description:** Layer 4 aggregates data from Layer 3 and enriches with Layer 2 metadata.

**Example:**
```python
# Layer 4: KPI calculation (future)
def calculate_first_pass_yield(product_code, date_range):
    # Get KPI definition from Layer 2
    kpi_def = layer2_api.get("/api/v1/mes-config/kpi-definitions", 
                             params={"kpi_code": "FIRST_PASS_YIELD"})
    target = kpi_def["target_value"]
    
    # Get production records from Layer 3
    production = layer3_api.get("/api/v1/mes-exec/production-records",
                                params={
                                    "product_code": product_code,
                                    "date_from": date_range[0],
                                    "date_to": date_range[1]
                                })
    
    # Calculate actual yield
    total_produced = sum(p["quantity_produced"] for p in production)
    total_good = sum(p["quantity_good"] for p in production)
    actual_yield = (total_good / total_produced) * 100
    
    # Compare to target
    variance = actual_yield - target
    
    return {
        "kpi_code": "FIRST_PASS_YIELD",
        "product_code": product_code,
        "target_value": target,
        "actual_value": actual_yield,
        "variance": variance,
        "status": "ABOVE_TARGET" if variance >= 0 else "BELOW_TARGET"
    }
```

**Data Flow:**
```
Layer 4 (Analytics) ──reads──> Layer 3 (Execution) ──reads──> Layer 2 (Config)
```

---

## Data Flow Rules

### Rule 1: Unidirectional Reads
**Higher layers can READ from lower layers, but NOT write.**

```
Layer 4 ──READ──> Layer 3 ──READ──> Layer 2 ──READ──> Layer 1
         ✅                ✅                ✅

Layer 4 ──WRITE──X Layer 3
         ❌
Layer 3 ──WRITE──X Layer 2
         ❌
Layer 2 ──WRITE──X Layer 1
         ❌
```

### Rule 2: No Cross-Layer Transactions
**Database transactions are scoped to a single layer.**

```python
# ❌ WRONG - Cross-layer transaction
@transaction
def create_work_order_with_new_product():
    # Layer 2: Create product
    product = layer2_db.insert("mes_config_product_master", {...})
    
    # Layer 3: Create work order
    work_order = layer3_db.insert("mes_exec_work_order", {...})
    
    # If work order fails, product should NOT rollback
    # These are independent layers!

# ✅ CORRECT - Separate transactions
def create_work_order_with_new_product():
    # Layer 2: Create product (separate transaction)
    with layer2_db.transaction():
        product = layer2_db.insert("mes_config_product_master", {...})
    
    # Layer 3: Create work order (separate transaction)
    with layer3_db.transaction():
        work_order = layer3_db.insert("mes_exec_work_order", {
            "product_code": product["product_code"]  # Reference by code
        })
```

### Rule 3: Symbolic References (String Codes)
**Layers reference each other via string codes, not integer foreign keys.**

```sql
-- ❌ WRONG - Direct foreign key to another layer
CREATE TABLE mes_exec_work_order (
  work_order_id INTEGER PRIMARY KEY,
  product_id INTEGER REFERENCES mes_config_product_master(product_id)  -- Bad!
);

-- ✅ CORRECT - String code reference
CREATE TABLE mes_exec_work_order (
  work_order_id INTEGER PRIMARY KEY,
  product_code VARCHAR(50)  -- References mes_config_product_master.product_code
);
```

**Why?** This allows layers to be deployed independently and prevents cascade deletes across layers.

### Rule 4: No Direct Database Access Across Layers
**Layers communicate via APIs, not direct database queries.**

```python
# ❌ WRONG - Direct database query to another layer
def get_work_order_details(work_order_id):
    # Layer 3 query
    work_order = layer3_db.query("SELECT * FROM mes_exec_work_order WHERE id = ?", work_order_id)
    
    # Layer 2 direct query (BAD!)
    product = layer2_db.query("SELECT * FROM mes_config_product_master WHERE product_code = ?", 
                               work_order["product_code"])
    
    return {**work_order, "product_details": product}

# ✅ CORRECT - API calls
def get_work_order_details(work_order_id):
    # Layer 3 API
    work_order = layer3_api.get(f"/api/v1/mes-exec/work-orders/{work_order_id}")
    
    # Layer 2 API
    product = layer2_api.get(f"/api/v1/mes-config/products?product_code={work_order['product_code']}")
    
    return {**work_order, "product_details": product}
```

---

## Layer Boundaries

### What Each Layer CAN Do

| Layer | Can Read From | Can Write To | Can Modify | Can Delete |
|-------|--------------|--------------|------------|------------|
| **Layer 1** | Sensors, PLCs | Layer 1 only | Layer 1 only | Layer 1 only |
| **Layer 2** | Layer 2 only | Layer 2 only | Layer 2 only | Layer 2 only (soft delete) |
| **Layer 3** | Layer 1, Layer 2, Layer 3 | Layer 3 only | Layer 3 only | Layer 3 only (soft delete) |
| **Layer 4** | Layer 1, Layer 2, Layer 3, Layer 4 | Layer 4 only | Layer 4 only | Layer 4 only |

### Boundary Enforcement

#### Database Level
- Separate database schemas (or separate databases)
- No foreign key constraints across layers
- Layer-specific user accounts with restricted access

```sql
-- PostgreSQL example
CREATE SCHEMA mes_config;     -- Layer 2
CREATE SCHEMA mes_execution;  -- Layer 3
CREATE SCHEMA mes_analytics;  -- Layer 4

-- Layer 3 user can only access execution schema
GRANT SELECT ON mes_config.* TO layer3_user;      -- Read-only to Layer 2
GRANT ALL ON mes_execution.* TO layer3_user;      -- Full access to Layer 3
REVOKE ALL ON mes_analytics.* FROM layer3_user;   -- No access to Layer 4
```

#### API Level
- Separate API endpoints per layer
- Layer-specific authentication/authorization
- Rate limiting per layer

```
Layer 2 API: /api/v1/mes-config/*     (Public - low rate limit)
Layer 3 API: /api/v1/mes-exec/*       (Authenticated - medium rate limit)
Layer 4 API: /api/v1/mes-analytics/*  (Authenticated - high rate limit)
```

#### Application Level
- Separate microservices per layer
- Service-to-service authentication
- Circuit breakers for resilience

```
┌──────────────────┐
│ Layer 2 Service  │ :8000
└──────────────────┘
         ↑ HTTP API
┌──────────────────┐
│ Layer 3 Service  │ :8001
└──────────────────┘
         ↑ HTTP API
┌──────────────────┐
│ Layer 4 Service  │ :8002
└──────────────────┘
```

---

## Phase Isolation

### Phase 1: Configuration (Current)
**Scope:** Layer 2 only  
**Tables:** 33 tables (all prefixed `mes_config_*`)  
**API:** `/api/v1/mes-config/*`  
**Database:** `mes_config.db` (or schema `mes_config`)  

**Independence:**
- Can be deployed standalone
- Does NOT require Layer 3 or Layer 4
- Does NOT connect to Layer 1 (symbolic references only)
- Self-contained with own governance and audit trail

### Phase 2: Execution (Future)
**Scope:** Layer 3  
**Tables:** New tables (prefixed `mes_exec_*`)  
**API:** `/api/v1/mes-exec/*`  
**Database:** `mes_execution.db` (or schema `mes_execution`)  

**Dependencies:**
- Reads from Layer 2 (config)
- Reads from Layer 1 (live data via integration service)
- Does NOT modify Layer 1 or Layer 2

### Phase 3: Analytics (Future)
**Scope:** Layer 4  
**Tables:** New tables (prefixed `mes_analytics_*`)  
**API:** `/api/v1/mes-analytics/*`  
**Database:** `mes_analytics.db` (or schema `mes_analytics`)  

**Dependencies:**
- Reads from Layer 2 (config)
- Reads from Layer 3 (execution data)
- Does NOT modify Layer 1, Layer 2, or Layer 3

---

## Additive-Only Approach

### Principle
**New phases ADD capabilities without MODIFYING existing layers.**

### Rules

#### ✅ Allowed in New Phases
1. **Add new tables** in new schema/namespace
2. **Add new API endpoints** under new prefix
3. **Add new views** that join across layers (read-only)
4. **Add new integration services** that read from multiple layers
5. **Add new indexes** to existing tables (performance optimization)

#### ❌ NOT Allowed in New Phases
1. **Modify existing table schemas** (add/remove/rename columns)
2. **Delete existing tables**
3. **Change existing API endpoints** (breaking changes)
4. **Add foreign key constraints** to existing tables from new layers
5. **Modify existing stored procedures/functions**

### Example: Adding Execution Tracking (Phase 2)

#### ❌ WRONG Approach
```sql
-- Modifying Layer 2 table (BAD!)
ALTER TABLE mes_config_product_master 
  ADD COLUMN total_produced_quantity INTEGER DEFAULT 0;

-- This violates phase isolation!
```

#### ✅ CORRECT Approach
```sql
-- Add new Layer 3 table (GOOD!)
CREATE TABLE mes_exec_production_summary (
  summary_id INTEGER PRIMARY KEY,
  product_code VARCHAR(50),  -- References Layer 2 (string code, not FK)
  period_date DATE,
  total_produced_quantity INTEGER,
  total_good_quantity INTEGER,
  total_rejected_quantity INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index for performance
CREATE INDEX idx_prod_summary_product ON mes_exec_production_summary(product_code);

-- Add view that joins Layer 2 and Layer 3
CREATE VIEW v_product_with_production AS
SELECT 
  p.product_code,
  p.product_name,
  p.standard_output_rate,  -- Layer 2
  COALESCE(SUM(s.total_produced_quantity), 0) AS actual_produced  -- Layer 3
FROM mes_config_product_master p
LEFT JOIN mes_exec_production_summary s ON p.product_code = s.product_code
GROUP BY p.product_code, p.product_name, p.standard_output_rate;
```

### Migration Strategy

When deploying new phases:

1. **Deploy Layer 2 (Phase 1)** first
   ```bash
   # Deploy configuration layer
   python main.py
   # Load seed data
   python -m mes_config.services.seed_loader
   ```

2. **Verify Layer 2** is operational
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/mes-config/enterprise
   ```

3. **Deploy Layer 3 (Phase 2)** when ready
   ```bash
   # Deploy execution layer (future)
   python mes_execution/main.py  # Different service
   # Initialize execution tables
   python -m mes_execution.database.init_db
   ```

4. **Verify Layer 3** without affecting Layer 2
   ```bash
   curl http://localhost:8001/health
   curl http://localhost:8001/api/v1/mes-exec/work-orders
   ```

5. **Deploy Layer 4 (Phase 3)** when ready
   ```bash
   # Deploy analytics layer (future)
   python mes_analytics/main.py  # Yet another service
   ```

### Rollback Strategy

Because phases are isolated, you can roll back a phase without affecting others:

```bash
# If Layer 3 deployment fails, rollback
# Layer 2 continues to operate normally
docker-compose stop mes-execution-service
docker-compose start mes-config-service  # Still running

# Or rollback database schema only
psql -d mes < rollback_layer3.sql
# Layer 2 schema remains unchanged
```

---

## Summary: Key Takeaways

### Phase 1 (Current Implementation)
✅ **Layer 2: Configuration** is complete and operational  
✅ **33 tables** across 7 modules  
✅ **RESTful API** with full CRUD operations  
✅ **Governance framework** with versioning and audit trails  
✅ **Symbolic linkage** to Layer 1 (OPC/Modbus references as strings)  
✅ **No live connections** to equipment (configuration only)  

### Layer Boundaries
✅ **Layer 1** (Connectivity) - Existing, DO NOT TOUCH  
✅ **Layer 2** (Configuration) - Phase 1, current implementation  
🔜 **Layer 3** (Execution) - Phase 2, future  
🔜 **Layer 4** (Analytics) - Phase 3+, future  

### Integration Patterns
✅ **Symbolic Linkage** - Layer 2 stores string references to Layer 1  
✅ **Reference Lookup** - Layer 3 will store string codes to Layer 2  
✅ **Aggregation** - Layer 4 will aggregate Layer 3 data with Layer 2 metadata  

### Data Flow Rules
✅ **Unidirectional Reads** - Higher layers read from lower layers  
✅ **No Cross-Layer Transactions** - Each layer has independent transactions  
✅ **Symbolic References** - String codes, not foreign keys  
✅ **API Communication** - No direct database access across layers  

### Additive-Only Approach
✅ **New phases ADD tables/APIs** without modifying existing ones  
✅ **Phase isolation** allows independent deployment and rollback  
✅ **No breaking changes** to existing layers  

---

**END OF ARCHITECTURE DOCUMENTATION - PHASE_1_CONFIG_ONLY**
