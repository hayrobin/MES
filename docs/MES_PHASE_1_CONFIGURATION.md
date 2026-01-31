# MES Phase 1: Configuration Layer - Complete Documentation

**PHASE_1_CONFIG_ONLY** - This documentation covers the Master Data & Configuration layer only.  
NO execution logic, NO live telemetry, NO OPC/Modbus integration, NO real-time monitoring.

---

## Table of Contents
1. [Overview](#overview)
2. [What's Included in Phase 1](#whats-included-in-phase-1)
3. [What's NOT in Phase 1](#whats-not-in-phase-1)
4. [Database Schema](#database-schema)
5. [Module Details](#module-details)
6. [Seed Data](#seed-data)
7. [Configuration Options](#configuration-options)
8. [Migration Guide](#migration-guide)
9. [Troubleshooting](#troubleshooting)

---

## Overview

**MES Phase 1: Configuration Layer** establishes the foundational master data and reference data required for manufacturing operations. This phase focuses exclusively on **static configuration data** and provides a robust API for managing organizational structures, equipment definitions, materials, products, and quality standards.

### Key Principles

✅ **Configuration Only** - All data is static master/reference data  
✅ **Symbolic Linkage** - Integration fields (OPC UA, Modbus) are strings for future use, not active connections  
✅ **Governance Framework** - Built-in versioning, approval workflows, and audit trails  
✅ **Additive Architecture** - Phase 1 is the foundation; future phases add capabilities without modifying existing tables  
✅ **RESTful API** - Full CRUD operations via FastAPI with automatic OpenAPI documentation  

### Architecture Position

Phase 1 sits at **Layer 2: Configuration** in the MES architecture:
- **Layer 1**: Connectivity & Data Acquisition (existing - not modified)
- **Layer 2**: Configuration ← **Phase 1 is here**
- **Layer 3+**: Execution, Scheduling, Analytics (future phases)

---

## What's Included in Phase 1

### 7 Modules, 33 Tables, 247 Master Data Records

#### **Module 1: Enterprise & Organizational Configuration** (7 tables)
- Enterprise (company master data)
- Site (manufacturing plants/facilities)
- Area (production areas within sites)
- Line (production lines)
- Department (organizational departments)
- Shift Calendar (shift definitions/templates)
- Unit of Measure (UOM master data)

#### **Module 2: Equipment & Capacity** (2 tables)
- Equipment Master (equipment hierarchy with symbolic linkage)
- Equipment Capacity (rated capacity definitions)

#### **Module 3: Material Master** (2 tables)
- Material Category (hierarchical categories)
- Material Master (all materials with tracking configuration)

#### **Module 4: Product & Production** (3 tables)
- Product Family (product grouping/grades)
- Product Master (finished products)
- Product Equipment Compatibility (product-equipment mapping)

#### **Module 5: Bill of Resources** (4 tables)
- Bill of Resources (manufacturing routing)
- BOR Material (material consumption standards)
- BOR Tooling (tooling requirements)
- BOR Quality Checkpoint (quality checkpoint definitions)

#### **Module 6: Quality & Rejection Codes** (3 tables)
- Rejection Code Category (categories for rejection codes)
- Material Rejection Code (material-specific codes)
- Production Rejection Code (production defect codes)

#### **Module 7: OEE Targets & KPI Configuration** (2 tables)
- OEE Target (target configuration by product/line/machine/site)
- KPI Definition (KPI metadata and formulas)

#### **Governance Framework** (3 tables)
- Audit Trail (complete change history)
- User Role (role definitions)
- Role Permission (role-based access control)

### Features

✅ **RESTful API** - 60+ endpoints via FastAPI  
✅ **Governance** - Version control, approval workflows (DRAFT → APPROVED → ARCHIVED)  
✅ **Audit Trail** - Complete change history for all master data  
✅ **Validation** - Unique code enforcement, referential integrity checks  
✅ **Seed Data** - 247 pre-configured master data records (116K JSON)  
✅ **Documentation** - Auto-generated OpenAPI/Swagger UI at `/api/docs`  

---

## What's NOT in Phase 1

❌ **NO Execution Logic** - No work orders, production orders, or job tracking  
❌ **NO Live Telemetry** - No real-time equipment monitoring or OPC UA/Modbus connections  
❌ **NO Inventory Tracking** - Material consumption, stock levels, or warehouse management  
❌ **NO Scheduling** - Production scheduling or capacity planning algorithms  
❌ **NO Quality Execution** - Actual inspection records or test results  
❌ **NO KPI Calculations** - KPI values, OEE measurements, or analytics  
❌ **NO Shop Floor Execution** - Operator interfaces or job instructions  
❌ **NO Genealogy** - Batch/lot traceability or material genealogy  

### Important Notes

- **OPC UA/Modbus fields** are symbolic references (strings) only - NOT live connections
- **Equipment Capacity** is rated/design capacity - NOT actual monitoring
- **Shift Calendar** defines shift templates - NOT actual shift instances or attendance
- **Quality Checkpoints** are definitions only - NOT inspection records
- **KPI Definitions** contain formulas as text - NOT executable calculations
- **BOR Material** shows standard consumption - NOT actual consumption tracking

---

## Database Schema

### Schema Naming Convention
All tables use prefix `mes_config_*` to indicate Phase 1 Configuration layer.

### Governance Fields (All Tables)
Every configuration table inherits from `GovernanceMixin`:

| Field | Type | Description |
|-------|------|-------------|
| `version` | Integer | Record version number (starts at 1, increments on changes) |
| `effective_from` | DateTime | When this record becomes effective |
| `effective_to` | DateTime | When this record expires (NULL = still active) |
| `approval_status` | Enum | DRAFT, APPROVED, ARCHIVED |
| `created_by` | String(100) | User who created the record |
| `created_at` | DateTime | Creation timestamp |
| `updated_by` | String(100) | User who last updated |
| `updated_at` | DateTime | Last update timestamp |
| `approved_by` | String(100) | User who approved |
| `approved_at` | DateTime | Approval timestamp |

### Approval Workflow
```
DRAFT → APPROVED → ARCHIVED
  ↑         ↓
  └─────────┘ (can revert to DRAFT for editing)
```

---

## Module Details

### Module 1: Enterprise & Organizational Configuration

#### 1.1 Enterprise
**Table:** `mes_config_enterprise`

Company-level master data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `enterprise_id` | Integer | PK, Index | Unique enterprise identifier |
| `enterprise_code` | String(50) | Unique, Not Null, Index | Unique enterprise code |
| `enterprise_name` | String(200) | Not Null | Enterprise name |
| `erp_reference` | String(100) | Nullable | ERP system reference |
| `address` | String(500) | Nullable | Company address |
| `contact_email` | String(200) | Nullable | Contact email |
| `contact_phone` | String(50) | Nullable | Contact phone |
| `is_active` | Integer | Default: 1 | Active flag (1=active, 0=inactive) |

**Relationships:**
- `sites` → One-to-Many with Site

**Example:**
```json
{
  "enterprise_code": "ENT-001",
  "enterprise_name": "ABC Manufacturing Corp",
  "erp_reference": "SAP-ENT-001",
  "address": "123 Industrial Blvd, Detroit, MI 48201",
  "contact_email": "corporate@abcmfg.com",
  "contact_phone": "+1-313-555-0100",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

#### 1.2 Site
**Table:** `mes_config_site`

Manufacturing sites/plants within an enterprise.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `site_id` | Integer | PK, Index | Unique site identifier |
| `site_code` | String(50) | Unique, Not Null, Index | Unique site code |
| `site_name` | String(200) | Not Null | Site name |
| `enterprise_id` | Integer | FK (Enterprise), Not Null, Index | Parent enterprise |
| `erp_reference` | String(100) | Nullable | ERP system reference |
| `timezone` | String(50) | Nullable | Site timezone (e.g., "America/Detroit") |
| `location` | String(500) | Nullable | Site location/address |
| `contact_name` | String(200) | Nullable | Site contact person |
| `contact_email` | String(200) | Nullable | Site contact email |
| `contact_phone` | String(50) | Nullable | Site contact phone |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `enterprise` → Many-to-One with Enterprise
- `areas` → One-to-Many with Area

**Example:**
```json
{
  "site_code": "SITE-DET-01",
  "site_name": "Detroit Manufacturing Plant",
  "enterprise_id": 1,
  "erp_reference": "SAP-PLANT-1000",
  "timezone": "America/Detroit",
  "location": "500 Factory Rd, Detroit, MI 48210",
  "contact_name": "John Smith",
  "contact_email": "john.smith@abcmfg.com",
  "contact_phone": "+1-313-555-0200"
}
```

---

#### 1.3 Area
**Table:** `mes_config_area`

Production areas within a site (e.g., Assembly, Machining, Packaging).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `area_id` | Integer | PK, Index | Unique area identifier |
| `area_code` | String(50) | Unique, Not Null, Index | Unique area code |
| `area_name` | String(200) | Not Null | Area name |
| `site_id` | Integer | FK (Site), Not Null, Index | Parent site |
| `description` | String(500) | Nullable | Area description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `site` → Many-to-One with Site
- `lines` → One-to-Many with Line

---

#### 1.4 Line
**Table:** `mes_config_line`

Production lines within an area.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `line_id` | Integer | PK, Index | Unique line identifier |
| `line_code` | String(50) | Unique, Not Null, Index | Unique line code |
| `line_name` | String(200) | Not Null | Line name |
| `area_id` | Integer | FK (Area), Not Null, Index | Parent area |
| `site_id` | Integer | FK (Site), Not Null, Index | Parent site (denormalized) |
| `description` | String(500) | Nullable | Line description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `area` → Many-to-One with Area
- `site` → Many-to-One with Site

**Hierarchy:**
```
Enterprise
  └─ Site
      └─ Area
          └─ Line
```

---

#### 1.5 Department
**Table:** `mes_config_department`

Organizational departments (can be hierarchical).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `department_id` | Integer | PK, Index | Unique department identifier |
| `department_code` | String(50) | Unique, Not Null, Index | Unique department code |
| `department_name` | String(200) | Not Null | Department name |
| `site_id` | Integer | FK (Site), Not Null, Index | Parent site |
| `parent_department_id` | Integer | FK (Department), Nullable, Index | Parent department (for hierarchy) |
| `manager_name` | String(200) | Nullable | Department manager |
| `cost_center` | String(50) | Nullable | Cost center code |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `site` → Many-to-One with Site
- `parent_department` → Self-referencing (hierarchical)

---

#### 1.6 Shift Calendar
**Table:** `mes_config_shift_calendar`

Shift definitions (templates only - NO execution tracking).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `shift_id` | Integer | PK, Index | Unique shift identifier |
| `shift_code` | String(50) | Unique, Not Null, Index | Unique shift code |
| `shift_name` | String(100) | Not Null | Shift name |
| `site_id` | Integer | FK (Site), Not Null, Index | Parent site |
| `start_time` | Time | Not Null | Shift start time |
| `end_time` | Time | Not Null | Shift end time |
| `duration_minutes` | Integer | Not Null | Shift duration in minutes |
| `days_of_week` | String(50) | Not Null | Days (e.g., "MON,TUE,WED,THU,FRI") |
| `description` | String(500) | Nullable | Shift description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** This defines shift **templates**, not actual shift instances or attendance.

**Example:**
```json
{
  "shift_code": "DAY-SHIFT-1",
  "shift_name": "Day Shift",
  "site_id": 1,
  "start_time": "06:00:00",
  "end_time": "14:00:00",
  "duration_minutes": 480,
  "days_of_week": "MON,TUE,WED,THU,FRI"
}
```

---

#### 1.7 Unit of Measure (UOM)
**Table:** `mes_config_unit_of_measure`

UOM master data with conversion factors.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `uom_id` | Integer | PK, Index | Unique UOM identifier |
| `uom_code` | String(20) | Unique, Not Null, Index | Unique UOM code (e.g., "KG", "LB", "EA") |
| `uom_name` | String(100) | Not Null | UOM name |
| `uom_type` | String(50) | Not Null | Type: WEIGHT, LENGTH, VOLUME, QUANTITY, TIME |
| `conversion_factor` | String(20) | Nullable | Conversion to base unit (e.g., "0.453592" for LB to KG) |
| `base_uom_code` | String(20) | Nullable | Reference to base unit |
| `is_active` | Integer | Default: 1 | Active flag |

**Example:**
```json
{
  "uom_code": "LB",
  "uom_name": "Pound",
  "uom_type": "WEIGHT",
  "conversion_factor": "0.453592",
  "base_uom_code": "KG"
}
```

---

### Module 2: Equipment & Capacity Definition

#### 2.1 Equipment Master
**Table:** `mes_config_equipment_master`

Equipment hierarchy and master data with **symbolic linkage** to external systems.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `equipment_id` | Integer | PK, Index | Unique equipment identifier |
| `equipment_code` | String(50) | Unique, Not Null, Index | Unique equipment code |
| `equipment_name` | String(200) | Not Null | Equipment name |
| `equipment_type` | String(50) | Not Null | Type: MACHINE, LINE, CELL, TOOL |
| `parent_equipment_id` | Integer | FK (EquipmentMaster), Nullable, Index | Parent equipment (for hierarchy) |
| `site_id` | Integer | Nullable, Index | Location: site |
| `area_id` | Integer | Nullable, Index | Location: area |
| `line_id` | Integer | Nullable, Index | Location: line |
| `manufacturer` | String(200) | Nullable | Equipment manufacturer |
| `model` | String(100) | Nullable | Equipment model |
| `serial_number` | String(100) | Nullable | Serial number |
| `installation_date` | String(20) | Nullable | Installation date (ISO format) |
| `is_bottleneck` | Integer | Default: 0 | Bottleneck flag (1=yes, 0=no) |
| `criticality_level` | String(20) | Default: "Medium" | Criticality: Low, Medium, High, Critical |
| `external_asset_ref` | String(100) | Nullable, Index | External asset management system reference |
| `opc_namespace` | String(200) | Nullable | **OPC UA namespace (STRING ONLY - not active connection)** |
| `opc_node_id` | String(200) | Nullable | **OPC UA node ID (STRING ONLY - not active connection)** |
| `modbus_tag_ref` | String(100) | Nullable | **Modbus tag reference (STRING ONLY - not active connection)** |
| `scada_tag_ref` | String(100) | Nullable | **SCADA tag reference (STRING ONLY)** |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `parent_equipment` → Self-referencing (hierarchical)
- `capacities` → One-to-Many with EquipmentCapacity

**CRITICAL:** The fields `opc_namespace`, `opc_node_id`, `modbus_tag_ref`, and `scada_tag_ref` are **STRING REFERENCES ONLY** for future integration. Phase 1 does NOT establish live connections.

**Example:**
```json
{
  "equipment_code": "CNC-MILL-001",
  "equipment_name": "CNC Milling Machine #1",
  "equipment_type": "MACHINE",
  "site_id": 1,
  "area_id": 1,
  "line_id": 1,
  "manufacturer": "HAAS Automation",
  "model": "VF-4SS",
  "serial_number": "1234567",
  "installation_date": "2020-01-15",
  "is_bottleneck": 1,
  "criticality_level": "High",
  "opc_namespace": "ns=2;s=CNC.Mill001",
  "modbus_tag_ref": "40001-40010",
  "scada_tag_ref": "CNC_MILL_001"
}
```

---

#### 2.2 Equipment Capacity
**Table:** `mes_config_equipment_capacity`

Equipment capacity configuration (**RATED CAPACITY ONLY** - NO live monitoring).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `capacity_id` | Integer | PK, Index | Unique capacity identifier |
| `equipment_id` | Integer | FK (EquipmentMaster), Not Null, Index | Equipment reference |
| `product_id` | Integer | Nullable, Index | Product-specific capacity (NULL = default) |
| `rated_capacity_value` | Numeric(18,4) | Not Null | Rated capacity value |
| `rated_capacity_uom` | String(50) | Not Null | Capacity UOM (e.g., "units/hour", "tons/hour") |
| `available_time_per_shift` | Integer | Nullable | Available time (minutes) |
| `setup_time` | Integer | Nullable | Setup time (minutes) |
| `description` | String(500) | Nullable | Capacity description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `equipment` → Many-to-One with EquipmentMaster

**Important:** This defines theoretical/design capacity, NOT actual performance or utilization.

---

### Module 3: Material Master

#### 3.1 Material Category
**Table:** `mes_config_material_category`

Hierarchical material categories.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `category_id` | Integer | PK, Index | Unique category identifier |
| `category_code` | String(50) | Unique, Not Null, Index | Unique category code |
| `category_name` | String(200) | Not Null | Category name |
| `parent_category_id` | Integer | FK (MaterialCategory), Nullable, Index | Parent category (for hierarchy) |
| `description` | String(500) | Nullable | Category description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `parent_category` → Self-referencing (hierarchical)
- `materials` → One-to-Many with MaterialMaster

---

#### 3.2 Material Master
**Table:** `mes_config_material_master`

All materials master data (raw, semi-finished, finished goods, consumables).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `material_id` | Integer | PK, Index | Unique material identifier |
| `material_code` | String(50) | Unique, Not Null, Index | Unique material code |
| `material_name` | String(200) | Not Null | Material name |
| `material_category_id` | Integer | FK (MaterialCategory), Not Null, Index | Material category |
| `material_type` | String(50) | Not Null | Type: RAW, SEMI_FINISHED, FINISHED_GOOD, CONSUMABLE |
| `base_uom` | String(20) | Not Null | Base unit of measure |
| `batch_tracking_required` | Integer | Default: 0 | Batch tracking flag (1=required, 0=not required) |
| `lot_tracking_required` | Integer | Default: 0 | Lot tracking flag |
| `serial_tracking_required` | Integer | Default: 0 | Serial tracking flag |
| `shelf_life_days` | Integer | Nullable | Shelf life in days |
| `expiry_tracking_required` | Integer | Default: 0 | Expiry tracking flag |
| `erp_material_code` | String(100) | Nullable, Index | ERP material code |
| `supplier_reference` | String(100) | Nullable | Supplier reference |
| `cost_center` | String(50) | Nullable | Cost center |
| `description` | String(500) | Nullable | Material description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `category` → Many-to-One with MaterialCategory

**Important:** Tracking flags define what **should** be tracked, not actual tracking data.

---

### Module 4: Product & Production Definitions

#### 4.1 Product Family
**Table:** `mes_config_product_family`

Product families/grades for grouping products.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `family_id` | Integer | PK, Index | Unique family identifier |
| `family_code` | String(50) | Unique, Not Null, Index | Unique family code |
| `family_name` | String(200) | Not Null | Family name |
| `description` | String(500) | Nullable | Family description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `products` → One-to-Many with ProductMaster

---

#### 4.2 Product Master
**Table:** `mes_config_product_master`

Finished products master data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `product_id` | Integer | PK, Index | Unique product identifier |
| `product_code` | String(50) | Unique, Not Null, Index | Unique product code |
| `product_name` | String(200) | Not Null | Product name |
| `product_family_id` | Integer | FK (ProductFamily), Nullable, Index | Product family |
| `standard_cycle_time` | Integer | Nullable | Standard cycle time (seconds/unit) |
| `standard_output_rate` | Numeric(18,4) | Nullable | Standard output rate (units/hour) |
| `base_uom` | String(20) | Not Null | Base unit of measure |
| `erp_product_code` | String(100) | Nullable, Index | ERP product code |
| `description` | String(500) | Nullable | Product description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `family` → Many-to-One with ProductFamily
- `equipment_compatibility` → One-to-Many with ProductEquipmentCompatibility

**Important:** Standard times are **configuration values**, not actual production times.

---

#### 4.3 Product Equipment Compatibility
**Table:** `mes_config_product_equipment_compatibility`

Defines which products can be produced on which equipment (CONFIGURATION - not scheduling).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `compatibility_id` | Integer | PK, Index | Unique compatibility identifier |
| `product_id` | Integer | FK (ProductMaster), Not Null, Index | Product reference |
| `equipment_id` | Integer | Not Null, Index | Equipment reference |
| `is_preferred_equipment` | Integer | Default: 0 | Preferred equipment flag |
| `setup_time` | Integer | Nullable | Setup time (minutes) |
| `capacity_constraint` | Numeric(18,4) | Nullable | Max capacity on this equipment (units/hour) |
| `description` | String(500) | Nullable | Compatibility description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `product` → Many-to-One with ProductMaster

---

### Module 5: Bill of Resources (BoR)

#### 5.1 Bill of Resources
**Table:** `mes_config_bill_of_resources`

Product → Equipment mapping with operation sequences (manufacturing routing).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `bor_id` | Integer | PK, Index | Unique BOR identifier |
| `product_id` | Integer | Not Null, Index | Product reference |
| `equipment_id` | Integer | Not Null, Index | Equipment reference |
| `operation_sequence` | Integer | Not Null | Operation sequence number |
| `operation_name` | String(200) | Nullable | Operation name |
| `standard_time` | Integer | Nullable | Standard time (minutes) |
| `setup_time` | Integer | Nullable | Setup time (minutes) |
| `description` | String(500) | Nullable | Operation description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** This is routing **configuration**, not work orders or job tracking.

---

#### 5.2 BOR Material
**Table:** `mes_config_bor_material`

Product → Material requirements (material consumption standards).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `bor_material_id` | Integer | PK, Index | Unique identifier |
| `product_id` | Integer | Not Null, Index | Product reference |
| `material_id` | Integer | Not Null, Index | Material reference |
| `standard_quantity` | Numeric(18,4) | Not Null | Standard consumption quantity |
| `uom` | String(20) | Not Null | Unit of measure |
| `scrap_factor` | Numeric(5,2) | Default: 0 | Scrap factor (percentage) |
| `operation_sequence` | Integer | Nullable | Linked operation sequence |
| `description` | String(500) | Nullable | Material requirement description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** This defines **standard** consumption, NOT actual material usage tracking.

---

#### 5.3 BOR Tooling
**Table:** `mes_config_bor_tooling`

Product → Tooling references (required tooling definitions).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `bor_tooling_id` | Integer | PK, Index | Unique identifier |
| `product_id` | Integer | Not Null, Index | Product reference |
| `tooling_code` | String(50) | Not Null, Index | Tooling code |
| `tooling_name` | String(200) | Not Null | Tooling name |
| `operation_sequence` | Integer | Nullable | Linked operation sequence |
| `quantity_required` | Integer | Default: 1 | Quantity required |
| `description` | String(500) | Nullable | Tooling description |
| `is_active` | Integer | Default: 1 | Active flag |

---

#### 5.4 BOR Quality Checkpoint
**Table:** `mes_config_bor_quality_checkpoint`

Product → Quality checkpoint definitions (DEFINITION ONLY - NO inspection records).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `checkpoint_id` | Integer | PK, Index | Unique checkpoint identifier |
| `product_id` | Integer | Not Null, Index | Product reference |
| `checkpoint_code` | String(50) | Not Null, Index | Checkpoint code |
| `checkpoint_name` | String(200) | Not Null | Checkpoint name |
| `checkpoint_type` | String(50) | Not Null | Type: INCOMING, IN_PROCESS, FINAL |
| `operation_sequence` | Integer | Nullable | Linked operation sequence |
| `required` | Integer | Default: 1 | Required flag |
| `description` | String(500) | Nullable | Checkpoint description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** This defines what checkpoints **exist**, NOT inspection results.

---

### Module 6: Quality & Rejection Codes

#### 6.1 Rejection Code Category
**Table:** `mes_config_rejection_code_category`

Categories for rejection codes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `category_id` | Integer | PK, Index | Unique category identifier |
| `category_code` | String(50) | Unique, Not Null, Index | Unique category code |
| `category_name` | String(200) | Not Null | Category name |
| `rejection_type` | String(50) | Not Null | Type: MATERIAL, PRODUCTION |
| `description` | String(500) | Nullable | Category description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `material_rejections` → One-to-Many with MaterialRejectionCode
- `production_rejections` → One-to-Many with ProductionRejectionCode

---

#### 6.2 Material Rejection Code
**Table:** `mes_config_material_rejection_code`

Material-specific rejection codes (CONFIGURATION - not actual rejections).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `rejection_code_id` | Integer | PK, Index | Unique identifier |
| `rejection_code` | String(50) | Unique, Not Null, Index | Unique rejection code |
| `rejection_name` | String(200) | Not Null | Rejection name |
| `category_id` | Integer | FK (RejectionCodeCategory), Not Null, Index | Category reference |
| `rejection_source` | String(100) | Nullable | Source: INCOMING_INSPECTION, STORAGE_HANDLING, SUPPLIER_RELATED |
| `classification` | String(50) | Not Null | Classification: SCRAP, REWORK, DOWNGRADE, HOLD |
| `severity_level` | Integer | Default: 3 | Severity (1-5 scale) |
| `cost_impact_indicator` | String(20) | Default: "Medium" | Impact: LOW, MEDIUM, HIGH |
| `root_cause_description` | String(1000) | Nullable | Root cause description |
| `description` | String(500) | Nullable | Rejection description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `category` → Many-to-One with RejectionCodeCategory

---

#### 6.3 Production Rejection Code
**Table:** `mes_config_production_rejection_code`

Production-specific rejection/defect codes (CONFIGURATION - not actual defects).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `rejection_code_id` | Integer | PK, Index | Unique identifier |
| `rejection_code` | String(50) | Unique, Not Null, Index | Unique rejection code |
| `rejection_name` | String(200) | Not Null | Rejection name |
| `category_id` | Integer | FK (RejectionCodeCategory), Not Null, Index | Category reference |
| `defect_type` | String(100) | Nullable | Type: PROCESS, DIMENSIONAL, SURFACE, ASSEMBLY, OTHER |
| `defect_source` | String(100) | Nullable | 5M Source: OPERATOR, MACHINE, MATERIAL, METHOD, ENVIRONMENT |
| `classification` | String(50) | Not Null | Classification: SCRAP, REWORK, DOWNGRADE |
| `severity_level` | Integer | Default: 3 | Severity (1-5 scale) |
| `cost_impact_indicator` | String(20) | Default: "Medium" | Impact: LOW, MEDIUM, HIGH |
| `corrective_action_required` | Integer | Default: 0 | Corrective action flag |
| `root_cause_description` | String(1000) | Nullable | Root cause description |
| `description` | String(500) | Nullable | Rejection description |
| `is_active` | Integer | Default: 1 | Active flag |

**Relationships:**
- `category` → Many-to-One with RejectionCodeCategory

---

### Module 7: OEE Targets & KPI Configuration

#### 7.1 OEE Target
**Table:** `mes_config_oee_target`

OEE targets by product/line/machine/site (CONFIGURATION - not measurements).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `target_id` | Integer | PK, Index | Unique target identifier |
| `target_type` | String(50) | Not Null, Index | Type: PRODUCT, LINE, MACHINE, SITE |
| `product_id` | Integer | Nullable, Index | Product reference (if target_type=PRODUCT) |
| `line_id` | Integer | Nullable, Index | Line reference (if target_type=LINE) |
| `equipment_id` | Integer | Nullable, Index | Equipment reference (if target_type=MACHINE) |
| `site_id` | Integer | Nullable, Index | Site reference (if target_type=SITE) |
| `availability_target` | Numeric(5,2) | Not Null | Availability target (%) |
| `performance_target` | Numeric(5,2) | Not Null | Performance target (%) |
| `quality_target` | Numeric(5,2) | Not Null | Quality target (%) |
| `oee_target` | Numeric(5,2) | Not Null | Overall OEE target (%) |
| `description` | String(500) | Nullable | Target description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** This defines **target values**, NOT actual OEE measurements.

**Example:**
```json
{
  "target_type": "PRODUCT",
  "product_id": 1,
  "availability_target": 90.00,
  "performance_target": 85.00,
  "quality_target": 95.00,
  "oee_target": 72.68,
  "description": "OEE target for Brake Assembly"
}
```

OEE Target = Availability × Performance × Quality  
72.68% = 90% × 85% × 95%

---

#### 7.2 KPI Definition
**Table:** `mes_config_kpi_definition`

KPI definitions and thresholds (CONFIGURATION ONLY - NO calculations).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `kpi_id` | Integer | PK, Index | Unique KPI identifier |
| `kpi_code` | String(50) | Unique, Not Null, Index | Unique KPI code |
| `kpi_name` | String(200) | Not Null | KPI name |
| `kpi_category` | String(50) | Not Null | Category: QUALITY, PRODUCTIVITY, EFFICIENCY, COST |
| `kpi_type` | String(100) | Not Null | Type: YIELD, SCRAP_RATE, REWORK_RATE, THROUGHPUT, etc. |
| `unit_of_measure` | String(50) | Nullable | KPI UOM (e.g., "%", "units/hour") |
| `target_value` | Numeric(18,4) | Nullable | Target value |
| `warning_threshold` | Numeric(18,4) | Nullable | Warning threshold |
| `critical_threshold` | Numeric(18,4) | Nullable | Critical threshold |
| `calculation_formula_description` | Text | Nullable | Formula as TEXT (not executable) |
| `aggregation_level` | String(50) | Nullable | Level: PRODUCT, LINE, SITE, ENTERPRISE |
| `measurement_frequency` | String(50) | Nullable | Frequency: HOURLY, SHIFT, DAILY, WEEKLY |
| `description` | String(500) | Nullable | KPI description |
| `is_active` | Integer | Default: 1 | Active flag |

**Important:** Formulas are stored as **text documentation**, NOT executable code.

**Example:**
```json
{
  "kpi_code": "FIRST_PASS_YIELD",
  "kpi_name": "First Pass Yield",
  "kpi_category": "QUALITY",
  "kpi_type": "YIELD",
  "unit_of_measure": "%",
  "target_value": 95.00,
  "warning_threshold": 90.00,
  "critical_threshold": 85.00,
  "calculation_formula_description": "(Good Units / Total Units Produced) × 100",
  "aggregation_level": "PRODUCT",
  "measurement_frequency": "SHIFT"
}
```

---

## Seed Data

Phase 1 includes **247 pre-configured master data records** (116K JSON) across 7 modules.

### Loading Seed Data

#### Method 1: Via API (Recommended)
```bash
# Start the API server
python main.py

# Load seed data via API endpoints
curl -X POST http://localhost:8000/api/v1/mes-config/seed/load \
  -H "Content-Type: application/json"
```

#### Method 2: Direct Database Load
```bash
# Use the seed_loader service
python -m mes_config.services.seed_loader
```

#### Method 3: Manual API Calls
```bash
# Load enterprises
cat mes_config/seed_data/enterprise.json | jq '.enterprises[]' | while read -r enterprise; do
  curl -X POST http://localhost:8000/api/v1/mes-config/enterprise \
    -H "Content-Type: application/json" \
    -d "$enterprise"
done

# Repeat for sites, areas, lines, equipment, materials, products, etc.
```

### Seed Data Files

Located in `/mes_config/seed_data/`:

| File | Records | Description |
|------|---------|-------------|
| `enterprise.json` | 29 | 2 enterprises, 2 sites, 6 areas, 12 lines, 4 departments, 3 shifts |
| `equipment.json` | 15 | Equipment units with OPC UA/Modbus references |
| `materials.json` | 17 | Materials (5 raw, 3 semi-finished, 5 finished goods, 4 consumables) |
| `products.json` | 19 | 5 products with families, equipment compatibility |
| `bill_of_resources.json` | 48 | 5 BORs, 18 operations, 14 materials, 5 tooling, 11 checkpoints |
| `rejection_codes.json` | 31 | 25 rejection codes across 6 categories |
| `oee_targets.json` | 28 | 16 OEE targets, 12 KPI definitions |

### Sample Data Structure

#### Enterprise Structure
- **ABC Manufacturing Corp** (ENT-001)
  - Detroit Manufacturing Plant (SITE-DET-01)
    - Machining Area (AREA-MACH-01)
      - CNC Line 1 (LINE-CNC-01)
      - CNC Line 2 (LINE-CNC-02)
    - Assembly Area (AREA-ASSY-01)
      - Assembly Line 1 (LINE-ASSY-01)
      - Assembly Line 2 (LINE-ASSY-02)
    - Packaging Area (AREA-PKG-01)
      - Packaging Line 1 (LINE-PKG-01)
  - Chicago Distribution Center (SITE-CHI-01)
    - Warehouse Area (AREA-WH-01)

#### Products
1. Brake Assembly (PROD-BRK-001) - 30 sec cycle time, 120 units/hour
2. Steering Component (PROD-STR-001) - 25 sec cycle time, 144 units/hour
3. Precision Bearing (PROD-BRG-001) - 15 sec cycle time, 240 units/hour
4. Transmission Gear (PROD-GEAR-001) - 40 sec cycle time, 90 units/hour
5. Drive Shaft (PROD-SHAFT-001) - 35 sec cycle time, 102.86 units/hour

#### Equipment
- CNC machines (HAAS VF-4SS, DMG MORI, Mazak)
- Grinding machines (Studer S33)
- Assembly robots (ABB IRB 6700, KUKA KR AGILUS, Universal Robots UR10e)
- Packaging lines (Ishida CCW-RV, Ishida IX-GA-4075)

---

## Configuration Options

### Application Settings
**File:** `mes_config/config.py`

```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./mes_config.db"
    
    # API
    API_V1_PREFIX: str = "/api/v1/mes-config"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Application
    APP_NAME: str = "MES Configuration Layer - Phase 1"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

### Environment Variables
Create `.env` file in project root:

```bash
# Database
DATABASE_URL=sqlite:///./mes_config.db
# Or use PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/mes_config

# API
API_V1_PREFIX=/api/v1/mes-config
HOST=0.0.0.0
PORT=8000

# Application
APP_NAME=MES Configuration Layer - Phase 1
DEBUG=true

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Configuration

#### SQLite (Default)
```python
DATABASE_URL = "sqlite:///./mes_config.db"
```

#### PostgreSQL (Production)
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/mes_config"
```

#### MySQL
```python
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/mes_config"
```

---

## Migration Guide

### From Existing Systems

#### Step 1: Export Master Data
Export master data from your current system (ERP, MES, CMMS):
- Organizational structure (sites, areas, lines)
- Equipment master data
- Material master data
- Product definitions
- BOMs/routing (convert to BOR format)

#### Step 2: Map to Schema
Map your data to Phase 1 schema:

| Your System | Phase 1 Table | Notes |
|-------------|---------------|-------|
| Plant/Factory | `mes_config_site` | Map plant codes to site_code |
| Work Center | `mes_config_area` or `mes_config_line` | Depends on hierarchy |
| Equipment | `mes_config_equipment_master` | Include OPC/Modbus refs if available |
| Material | `mes_config_material_master` | Set tracking flags based on requirements |
| Product/Item | `mes_config_product_master` | Products only (not materials) |
| BOM | `mes_config_bor_material` | Convert to material requirements |
| Routing | `mes_config_bill_of_resources` | Convert to operation sequences |

#### Step 3: Transform Data
Convert to JSON format matching seed data structure:

```json
{
  "enterprises": [
    {
      "enterprise_code": "YOUR-CODE",
      "enterprise_name": "Your Company",
      "created_by": "migration",
      "approval_status": "APPROVED"
    }
  ],
  "sites": [
    {
      "site_code": "YOUR-SITE-01",
      "site_name": "Your Plant 1",
      "enterprise_id": 1,
      "timezone": "America/New_York",
      "created_by": "migration",
      "approval_status": "APPROVED"
    }
  ]
}
```

#### Step 4: Load Data
Use API endpoints to load data:

```bash
# Load enterprises
curl -X POST http://localhost:8000/api/v1/mes-config/enterprise \
  -H "Content-Type: application/json" \
  -d @your_enterprises.json

# Load sites
curl -X POST http://localhost:8000/api/v1/mes-config/sites \
  -H "Content-Type: application/json" \
  -d @your_sites.json

# Continue for all modules...
```

#### Step 5: Validate
```bash
# Check loaded data
curl http://localhost:8000/api/v1/mes-config/enterprise
curl http://localhost:8000/api/v1/mes-config/sites
curl http://localhost:8000/api/v1/mes-config/equipment

# Verify counts
sqlite3 mes_config.db "SELECT COUNT(*) FROM mes_config_enterprise;"
sqlite3 mes_config.db "SELECT COUNT(*) FROM mes_config_site;"
sqlite3 mes_config.db "SELECT COUNT(*) FROM mes_config_equipment_master;"
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
**Error:** `sqlite3.OperationalError: unable to open database file`

**Solution:**
```bash
# Check database path
ls -la mes_config.db

# Create database directory if missing
mkdir -p ./

# Initialize database
python -c "from mes_config.database import init_db; init_db()"
```

---

#### 2. Unique Constraint Violations
**Error:** `IntegrityError: UNIQUE constraint failed: mes_config_enterprise.enterprise_code`

**Solution:**
```bash
# Check existing codes
sqlite3 mes_config.db "SELECT enterprise_code FROM mes_config_enterprise;"

# Use unique codes or update existing records
curl -X PUT http://localhost:8000/api/v1/mes-config/enterprise/1 \
  -H "Content-Type: application/json" \
  -d '{"enterprise_name": "Updated Name", "updated_by": "admin"}'
```

---

#### 3. Foreign Key Violations
**Error:** `IntegrityError: FOREIGN KEY constraint failed`

**Solution:**
```bash
# Ensure parent records exist first
# Example: Create enterprise before site

# Create enterprise first
curl -X POST http://localhost:8000/api/v1/mes-config/enterprise \
  -d '{"enterprise_code": "ENT-001", "enterprise_name": "ABC Corp", "created_by": "admin"}'

# Then create site with valid enterprise_id
curl -X POST http://localhost:8000/api/v1/mes-config/sites \
  -d '{"site_code": "SITE-01", "site_name": "Plant 1", "enterprise_id": 1, "created_by": "admin"}'
```

---

#### 4. API Server Won't Start
**Error:** `Address already in use`

**Solution:**
```bash
# Check port usage
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

#### 5. Import Errors
**Error:** `ModuleNotFoundError: No module named 'mes_config'`

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure you're in project root
cd /path/to/MES

# Run with Python module syntax
python -m main
```

---

#### 6. Validation Errors
**Error:** `422 Unprocessable Entity: validation error for EnterpriseCreate`

**Solution:**
```bash
# Check required fields in schema
# Example: EnterpriseCreate requires:
# - enterprise_code (required)
# - enterprise_name (required)
# - created_by (from GovernanceBase)

# Correct request
curl -X POST http://localhost:8000/api/v1/mes-config/enterprise \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_code": "ENT-001",
    "enterprise_name": "ABC Manufacturing",
    "created_by": "admin",
    "approval_status": "DRAFT"
  }'
```

---

#### 7. Approval Status Issues
**Error:** Records stuck in DRAFT status

**Solution:**
```bash
# Update approval status
curl -X PUT http://localhost:8000/api/v1/mes-config/enterprise/1 \
  -H "Content-Type: application/json" \
  -d '{
    "approval_status": "APPROVED",
    "approved_by": "manager",
    "updated_by": "admin"
  }'
```

---

#### 8. Seed Data Load Failures
**Error:** Seed data not loading correctly

**Solution:**
```bash
# Check JSON format
cat mes_config/seed_data/enterprise.json | jq .

# Load manually one entity at a time
# Check each response for errors

# Clear database and reload
rm mes_config.db
python -c "from mes_config.database import init_db; init_db()"
python -m mes_config.services.seed_loader
```

---

#### 9. Performance Issues
**Issue:** Slow API responses with large datasets

**Solution:**
```bash
# Use pagination
curl "http://localhost:8000/api/v1/mes-config/enterprise?skip=0&limit=50"

# Add indexes (already included in schema)
# Check query performance
sqlite3 mes_config.db "EXPLAIN QUERY PLAN SELECT * FROM mes_config_enterprise WHERE enterprise_code = 'ENT-001';"

# For PostgreSQL, use EXPLAIN ANALYZE
```

---

#### 10. CORS Issues
**Error:** Cross-origin requests blocked

**Solution:**
```python
# Already configured in main.py
# If you need to restrict origins, update:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

### Debugging Tips

#### Enable SQL Logging
```python
# In database.py, add:
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Logs all SQL statements
)
```

#### Check Database Contents
```bash
# SQLite CLI
sqlite3 mes_config.db

# List tables
.tables

# Describe table
.schema mes_config_enterprise

# Query data
SELECT * FROM mes_config_enterprise;

# Exit
.quit
```

#### Verify API Endpoints
```bash
# Check health
curl http://localhost:8000/health

# View OpenAPI docs
open http://localhost:8000/api/docs

# List all endpoints
curl http://localhost:8000/openapi.json | jq '.paths | keys'
```

---

## Support & Resources

### Documentation
- **API Documentation:** http://localhost:8000/api/docs (Swagger UI)
- **Alternative Docs:** http://localhost:8000/api/redoc (ReDoc)
- **OpenAPI Spec:** http://localhost:8000/openapi.json

### Code Structure
```
/home/runner/work/MES/MES/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── mes_config/
│   ├── __init__.py
│   ├── config.py             # Application settings
│   ├── database.py           # Database connection
│   ├── models/               # SQLAlchemy models (7 modules)
│   ├── schemas/              # Pydantic schemas
│   ├── api/                  # API routes (7 routers)
│   ├── services/             # CRUD and validation services
│   └── seed_data/            # Seed data JSON files
└── docs/                     # Documentation
```

### Next Steps

After completing Phase 1 setup:
1. ✅ Verify all seed data loaded correctly
2. ✅ Test API endpoints with sample data
3. ✅ Configure ERP integration (symbolic references)
4. ✅ Set up user roles and permissions
5. ⏳ Await Phase 2: Execution Layer (work orders, production tracking)

---

**END OF PHASE_1_CONFIG_ONLY DOCUMENTATION**
