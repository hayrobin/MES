# MES Configuration API - Complete Reference

**PHASE_1_CONFIG_ONLY** - Configuration Layer API Reference

---

## Table of Contents
1. [API Overview](#api-overview)
2. [Base URL & Authentication](#base-url--authentication)
3. [Common Patterns](#common-patterns)
4. [Enterprise Module](#enterprise-module)
5. [Equipment Module](#equipment-module)
6. [Material Module](#material-module)
7. [Product Module](#product-module)
8. [Bill of Resources Module](#bill-of-resources-module)
9. [Quality Module](#quality-module)
10. [KPI Targets Module](#kpi-targets-module)
11. [Error Responses](#error-responses)
12. [Pagination](#pagination)
13. [Approval Workflow](#approval-workflow)

---

## API Overview

The MES Configuration API provides RESTful endpoints for managing master data and configuration across 7 modules.

### Technology Stack
- **Framework:** FastAPI 0.110+
- **Database:** SQLite (default) / PostgreSQL / MySQL
- **ORM:** SQLAlchemy 2.0+
- **Validation:** Pydantic 2.0+
- **Documentation:** OpenAPI 3.0 (Swagger UI, ReDoc)

### Features
✅ **Full CRUD** - Create, Read, Update, Delete operations  
✅ **Pagination** - Skip/limit parameters on list endpoints  
✅ **Filtering** - Filter by status, type, active flag, and foreign keys  
✅ **Validation** - Automatic validation via Pydantic schemas  
✅ **Governance** - Built-in versioning, approval workflows, audit trails  
✅ **Soft Deletes** - Archive records instead of hard deletes  

---

## Base URL & Authentication

### Base URL
```
Development: http://localhost:8000/api/v1/mes-config
Production:  https://your-domain.com/api/v1/mes-config
```

### API Documentation
```
Swagger UI: http://localhost:8000/api/docs
ReDoc:      http://localhost:8000/api/redoc
OpenAPI:    http://localhost:8000/openapi.json
```

### Authentication
**Phase 1:** Authentication is optional (configurable).

**Future Phases:** Will support:
- JWT Bearer tokens
- API keys
- OAuth 2.0
- Role-based access control (RBAC)

### Headers
```http
Content-Type: application/json
Accept: application/json
# Authorization: Bearer <token>  (future)
```

---

## Common Patterns

### Governance Fields (All Entities)
Every entity includes governance fields for version control and audit trails:

```json
{
  "version": 1,
  "effective_from": "2025-02-01T00:00:00",
  "effective_to": null,
  "approval_status": "APPROVED",
  "created_by": "admin",
  "created_at": "2025-02-01T10:30:00",
  "updated_by": "manager",
  "updated_at": "2025-02-01T15:45:00",
  "approved_by": "director",
  "approved_at": "2025-02-01T16:00:00"
}
```

**Approval Status Values:**
- `DRAFT` - Record is in draft state
- `APPROVED` - Record is approved and active
- `ARCHIVED` - Record is archived (soft delete)

### Standard CRUD Pattern

#### **List** - GET /entity
```bash
GET /api/v1/mes-config/entity?skip=0&limit=100&is_active=1
```

#### **Get by ID** - GET /entity/{id}
```bash
GET /api/v1/mes-config/entity/1
```

#### **Create** - POST /entity
```bash
POST /api/v1/mes-config/entity
Content-Type: application/json

{
  "code": "ENT-001",
  "name": "Example Entity",
  "created_by": "admin",
  "approval_status": "DRAFT"
}
```

#### **Update** - PUT /entity/{id}
```bash
PUT /api/v1/mes-config/entity/1
Content-Type: application/json

{
  "name": "Updated Name",
  "updated_by": "admin"
}
```

#### **Delete** - DELETE /entity/{id}
Performs soft delete (archives the record):
```bash
DELETE /api/v1/mes-config/entity/1
```

---

## Enterprise Module

**Tag:** `Enterprise & Organizational Configuration`

### 1. Enterprises

#### List Enterprises
```http
GET /api/v1/mes-config/enterprise
```

**Query Parameters:**
- `skip` (integer, default: 0) - Pagination offset
- `limit` (integer, default: 100, max: 100) - Results per page
- `is_active` (integer, 0 or 1) - Filter by active status
- `approval_status` (string) - Filter by approval status (DRAFT, APPROVED, ARCHIVED)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise?skip=0&limit=10&is_active=1&approval_status=APPROVED"
```

**Example Response:**
```json
[
  {
    "enterprise_id": 1,
    "enterprise_code": "ENT-001",
    "enterprise_name": "ABC Manufacturing Corp",
    "erp_reference": "SAP-ENT-001",
    "address": "123 Industrial Blvd, Detroit, MI 48201",
    "contact_email": "corporate@abcmfg.com",
    "contact_phone": "+1-313-555-0100",
    "is_active": 1,
    "version": 1,
    "effective_from": "2025-01-01T00:00:00",
    "effective_to": null,
    "approval_status": "APPROVED",
    "created_by": "admin",
    "created_at": "2025-01-01T10:00:00",
    "updated_by": null,
    "updated_at": null,
    "approved_by": "director",
    "approved_at": "2025-01-01T12:00:00"
  }
]
```

---

#### Get Enterprise by ID
```http
GET /api/v1/mes-config/enterprise/{enterprise_id}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise/1"
```

---

#### Create Enterprise
```http
POST /api/v1/mes-config/enterprise
```

**Request Body:**
```json
{
  "enterprise_code": "ENT-002",
  "enterprise_name": "XYZ Industries",
  "erp_reference": "SAP-ENT-002",
  "address": "456 Factory Lane, Chicago, IL 60601",
  "contact_email": "info@xyzind.com",
  "contact_phone": "+1-312-555-0200",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "DRAFT",
  "effective_from": "2025-02-01T00:00:00"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/mes-config/enterprise" \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_code": "ENT-002",
    "enterprise_name": "XYZ Industries",
    "created_by": "admin",
    "approval_status": "DRAFT"
  }'
```

**Response:** `201 Created` with created entity

---

#### Update Enterprise
```http
PUT /api/v1/mes-config/enterprise/{enterprise_id}
```

**Request Body:**
```json
{
  "enterprise_name": "XYZ Industries Inc.",
  "contact_email": "corporate@xyzind.com",
  "updated_by": "admin"
}
```

**Example Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/mes-config/enterprise/2" \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_name": "XYZ Industries Inc.",
    "updated_by": "admin"
  }'
```

---

#### Delete Enterprise (Archive)
```http
DELETE /api/v1/mes-config/enterprise/{enterprise_id}
```

**Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/mes-config/enterprise/2"
```

**Response:** Archived enterprise with `approval_status: "ARCHIVED"` and `is_active: 0`

---

### 2. Sites

#### List Sites
```http
GET /api/v1/mes-config/sites
```

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 100)
- `enterprise_id` (integer) - Filter by enterprise
- `is_active` (integer, 0 or 1)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/sites?enterprise_id=1&is_active=1"
```

**Example Response:**
```json
[
  {
    "site_id": 1,
    "site_code": "SITE-DET-01",
    "site_name": "Detroit Manufacturing Plant",
    "enterprise_id": 1,
    "erp_reference": "SAP-PLANT-1000",
    "timezone": "America/Detroit",
    "location": "500 Factory Rd, Detroit, MI 48210",
    "contact_name": "John Smith",
    "contact_email": "john.smith@abcmfg.com",
    "contact_phone": "+1-313-555-0200",
    "is_active": 1,
    "version": 1,
    "effective_from": "2025-01-01T00:00:00",
    "approval_status": "APPROVED",
    "created_by": "admin",
    "created_at": "2025-01-01T10:15:00"
  }
]
```

---

#### Create Site
```http
POST /api/v1/mes-config/sites
```

**Request Body:**
```json
{
  "site_code": "SITE-CHI-01",
  "site_name": "Chicago Distribution Center",
  "enterprise_id": 1,
  "timezone": "America/Chicago",
  "location": "789 Warehouse Ave, Chicago, IL 60605",
  "contact_name": "Jane Doe",
  "contact_email": "jane.doe@abcmfg.com",
  "contact_phone": "+1-312-555-0300",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "DRAFT"
}
```

---

### 3. Areas

#### List Areas
```http
GET /api/v1/mes-config/areas
```

**Query Parameters:**
- `skip`, `limit`, `is_active` (standard pagination)
- `site_id` (integer) - Filter by site

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/areas?site_id=1"
```

---

#### Create Area
```http
POST /api/v1/mes-config/areas
```

**Request Body:**
```json
{
  "area_code": "AREA-MACH-01",
  "area_name": "Machining Area",
  "site_id": 1,
  "description": "CNC machining and grinding operations",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 4. Lines

#### List Lines
```http
GET /api/v1/mes-config/lines
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `area_id` (integer) - Filter by area
- `site_id` (integer) - Filter by site

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/lines?area_id=1&site_id=1"
```

---

#### Create Line
```http
POST /api/v1/mes-config/lines
```

**Request Body:**
```json
{
  "line_code": "LINE-CNC-01",
  "line_name": "CNC Line 1",
  "area_id": 1,
  "site_id": 1,
  "description": "CNC milling and turning operations",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 5. Departments

#### List Departments
```http
GET /api/v1/mes-config/departments
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `site_id` (integer)

---

#### Create Department
```http
POST /api/v1/mes-config/departments
```

**Request Body:**
```json
{
  "department_code": "DEPT-PROD-01",
  "department_name": "Production Department",
  "site_id": 1,
  "parent_department_id": null,
  "manager_name": "Mike Johnson",
  "cost_center": "CC-1001",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 6. Shift Calendars

#### List Shift Calendars
```http
GET /api/v1/mes-config/shift-calendars
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `site_id` (integer)

---

#### Create Shift Calendar
```http
POST /api/v1/mes-config/shift-calendars
```

**Request Body:**
```json
{
  "shift_code": "DAY-SHIFT-1",
  "shift_name": "Day Shift",
  "site_id": 1,
  "start_time": "06:00:00",
  "end_time": "14:00:00",
  "duration_minutes": 480,
  "days_of_week": "MON,TUE,WED,THU,FRI",
  "description": "Standard day shift - 8 hours",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 7. Units of Measure

#### List UOMs
```http
GET /api/v1/mes-config/unit-of-measures
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `uom_type` (string) - Filter by type (WEIGHT, LENGTH, VOLUME, QUANTITY, TIME)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/unit-of-measures?uom_type=WEIGHT"
```

---

#### Create UOM
```http
POST /api/v1/mes-config/unit-of-measures
```

**Request Body:**
```json
{
  "uom_code": "KG",
  "uom_name": "Kilogram",
  "uom_type": "WEIGHT",
  "conversion_factor": "1.0",
  "base_uom_code": "KG",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## Equipment Module

**Tag:** `Equipment & Capacity`

### 1. Equipment Master

#### List Equipment
```http
GET /api/v1/mes-config/equipment
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `equipment_type` (string) - Filter by type (MACHINE, LINE, CELL, TOOL)
- `site_id` (integer)
- `area_id` (integer)
- `line_id` (integer)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/equipment?equipment_type=MACHINE&site_id=1"
```

**Example Response:**
```json
[
  {
    "equipment_id": 1,
    "equipment_code": "CNC-MILL-001",
    "equipment_name": "CNC Milling Machine #1",
    "equipment_type": "MACHINE",
    "parent_equipment_id": null,
    "site_id": 1,
    "area_id": 1,
    "line_id": 1,
    "manufacturer": "HAAS Automation",
    "model": "VF-4SS",
    "serial_number": "1234567",
    "installation_date": "2020-01-15",
    "is_bottleneck": 1,
    "criticality_level": "High",
    "external_asset_ref": "CMMS-ASSET-001",
    "opc_namespace": "ns=2;s=CNC.Mill001",
    "opc_node_id": "ns=2;i=1001",
    "modbus_tag_ref": "40001-40010",
    "scada_tag_ref": "CNC_MILL_001",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create Equipment
```http
POST /api/v1/mes-config/equipment
```

**Request Body:**
```json
{
  "equipment_code": "CNC-MILL-002",
  "equipment_name": "CNC Milling Machine #2",
  "equipment_type": "MACHINE",
  "site_id": 1,
  "area_id": 1,
  "line_id": 1,
  "manufacturer": "DMG MORI",
  "model": "NHX 5000",
  "serial_number": "DMG987654",
  "installation_date": "2021-03-20",
  "is_bottleneck": 0,
  "criticality_level": "Medium",
  "opc_namespace": "ns=2;s=CNC.Mill002",
  "modbus_tag_ref": "40011-40020",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "DRAFT"
}
```

---

### 2. Equipment Capacity

#### List Equipment Capacities
```http
GET /api/v1/mes-config/equipment-capacity
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `equipment_id` (integer)
- `product_id` (integer)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/equipment-capacity?equipment_id=1"
```

**Example Response:**
```json
[
  {
    "capacity_id": 1,
    "equipment_id": 1,
    "product_id": null,
    "rated_capacity_value": "30.0000",
    "rated_capacity_uom": "units/hour",
    "available_time_per_shift": 420,
    "setup_time": 30,
    "description": "Default capacity for all products",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create Equipment Capacity
```http
POST /api/v1/mes-config/equipment-capacity
```

**Request Body:**
```json
{
  "equipment_id": 1,
  "product_id": 1,
  "rated_capacity_value": "25.0000",
  "rated_capacity_uom": "units/hour",
  "available_time_per_shift": 420,
  "setup_time": 45,
  "description": "Capacity for Brake Assembly production",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## Material Module

**Tag:** `Material Master`

### 1. Material Categories

#### List Material Categories
```http
GET /api/v1/mes-config/material-categories
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `parent_category_id` (integer) - Filter by parent category

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/material-categories"
```

---

#### Create Material Category
```http
POST /api/v1/mes-config/material-categories
```

**Request Body:**
```json
{
  "category_code": "CAT-METALS",
  "category_name": "Metals",
  "parent_category_id": null,
  "description": "Metallic raw materials",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 2. Materials

#### List Materials
```http
GET /api/v1/mes-config/materials
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `material_category_id` (integer)
- `material_type` (string) - RAW, SEMI_FINISHED, FINISHED_GOOD, CONSUMABLE

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/materials?material_type=RAW"
```

**Example Response:**
```json
[
  {
    "material_id": 1,
    "material_code": "MAT-STL-001",
    "material_name": "Steel Alloy 4140",
    "material_category_id": 1,
    "material_type": "RAW",
    "base_uom": "KG",
    "batch_tracking_required": 1,
    "lot_tracking_required": 1,
    "serial_tracking_required": 0,
    "shelf_life_days": null,
    "expiry_tracking_required": 0,
    "erp_material_code": "SAP-MAT-STL-4140",
    "supplier_reference": "SUPPLIER-001",
    "cost_center": "CC-1001",
    "description": "High-strength steel alloy for machining",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create Material
```http
POST /api/v1/mes-config/materials
```

**Request Body:**
```json
{
  "material_code": "MAT-ALU-001",
  "material_name": "Aluminum 6061-T6",
  "material_category_id": 1,
  "material_type": "RAW",
  "base_uom": "KG",
  "batch_tracking_required": 1,
  "lot_tracking_required": 0,
  "serial_tracking_required": 0,
  "shelf_life_days": null,
  "expiry_tracking_required": 0,
  "erp_material_code": "SAP-MAT-ALU-6061",
  "description": "Aluminum alloy for machining",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "DRAFT"
}
```

---

## Product Module

**Tag:** `Product & Production`

### 1. Product Families

#### List Product Families
```http
GET /api/v1/mes-config/product-families
```

**Query Parameters:**
- `skip`, `limit`, `is_active`

---

#### Create Product Family
```http
POST /api/v1/mes-config/product-families
```

**Request Body:**
```json
{
  "family_code": "FAMILY-AUTO",
  "family_name": "Automotive Components",
  "description": "Components for automotive industry",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 2. Products

#### List Products
```http
GET /api/v1/mes-config/products
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `family_id` (integer)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/products?family_id=1"
```

**Example Response:**
```json
[
  {
    "product_id": 1,
    "product_code": "PROD-BRK-001",
    "product_name": "Brake Assembly",
    "product_family_id": 1,
    "standard_cycle_time": 30,
    "standard_output_rate": "120.0000",
    "base_uom": "EA",
    "erp_product_code": "SAP-PROD-BRK-001",
    "description": "Complete brake assembly for automotive",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create Product
```http
POST /api/v1/mes-config/products
```

**Request Body:**
```json
{
  "product_code": "PROD-STR-001",
  "product_name": "Steering Component",
  "product_family_id": 1,
  "standard_cycle_time": 25,
  "standard_output_rate": "144.0000",
  "base_uom": "EA",
  "erp_product_code": "SAP-PROD-STR-001",
  "description": "Steering component for automotive",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "DRAFT"
}
```

---

### 3. Product Equipment Compatibility

#### List Compatibilities
```http
GET /api/v1/mes-config/product-equipment-compatibility
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `product_id` (integer)
- `equipment_id` (integer)

---

#### Create Compatibility
```http
POST /api/v1/mes-config/product-equipment-compatibility
```

**Request Body:**
```json
{
  "product_id": 1,
  "equipment_id": 1,
  "is_preferred_equipment": 1,
  "setup_time": 30,
  "capacity_constraint": "25.0000",
  "description": "Preferred equipment for Brake Assembly",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## Bill of Resources Module

**Tag:** `Bill of Resources`

### 1. Bill of Resources

#### List BORs
```http
GET /api/v1/mes-config/bill-of-resources
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `product_id` (integer)
- `equipment_id` (integer)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/bill-of-resources?product_id=1"
```

**Example Response:**
```json
[
  {
    "bor_id": 1,
    "product_id": 1,
    "equipment_id": 1,
    "operation_sequence": 10,
    "operation_name": "Machining - Rough Cut",
    "standard_time": 15,
    "setup_time": 30,
    "description": "Initial rough cutting operation",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create BOR
```http
POST /api/v1/mes-config/bill-of-resources
```

**Request Body:**
```json
{
  "product_id": 1,
  "equipment_id": 2,
  "operation_sequence": 20,
  "operation_name": "Machining - Finish Cut",
  "standard_time": 20,
  "setup_time": 15,
  "description": "Finish cutting operation",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 2. BOR Materials

#### List BOR Materials
```http
GET /api/v1/mes-config/bor-materials
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `product_id` (integer)
- `material_id` (integer)

**Example Response:**
```json
[
  {
    "bor_material_id": 1,
    "product_id": 1,
    "material_id": 1,
    "standard_quantity": "2.5000",
    "uom": "KG",
    "scrap_factor": "5.00",
    "operation_sequence": 10,
    "description": "Steel alloy for machining",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED"
  }
]
```

---

#### Create BOR Material
```http
POST /api/v1/mes-config/bor-materials
```

**Request Body:**
```json
{
  "product_id": 1,
  "material_id": 2,
  "standard_quantity": "1.0000",
  "uom": "EA",
  "scrap_factor": "2.00",
  "operation_sequence": 20,
  "description": "Bearing for assembly",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 3. BOR Tooling

#### List BOR Tooling
```http
GET /api/v1/mes-config/bor-tooling
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `product_id` (integer)

---

#### Create BOR Tooling
```http
POST /api/v1/mes-config/bor-tooling
```

**Request Body:**
```json
{
  "product_id": 1,
  "tooling_code": "TOOL-DRILL-001",
  "tooling_name": "Carbide Drill 10mm",
  "operation_sequence": 10,
  "quantity_required": 1,
  "description": "Drill bit for initial operation",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 4. BOR Quality Checkpoints

#### List BOR Quality Checkpoints
```http
GET /api/v1/mes-config/bor-quality-checkpoints
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `product_id` (integer)
- `checkpoint_type` (string) - INCOMING, IN_PROCESS, FINAL

---

#### Create BOR Quality Checkpoint
```http
POST /api/v1/mes-config/bor-quality-checkpoints
```

**Request Body:**
```json
{
  "product_id": 1,
  "checkpoint_code": "QC-DIM-001",
  "checkpoint_name": "Dimensional Check - Post Machining",
  "checkpoint_type": "IN_PROCESS",
  "operation_sequence": 10,
  "required": 1,
  "description": "Verify dimensions after rough cut",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## Quality Module

**Tag:** `Quality & Rejection Codes`

### 1. Rejection Code Categories

#### List Rejection Code Categories
```http
GET /api/v1/mes-config/rejection-code-categories
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `rejection_type` (string) - MATERIAL, PRODUCTION

---

#### Create Rejection Code Category
```http
POST /api/v1/mes-config/rejection-code-categories
```

**Request Body:**
```json
{
  "category_code": "CAT-MAT-DEFECT",
  "category_name": "Material Defects",
  "rejection_type": "MATERIAL",
  "description": "Material quality defects",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 2. Material Rejection Codes

#### List Material Rejection Codes
```http
GET /api/v1/mes-config/material-rejection-codes
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `category_id` (integer)
- `classification` (string) - SCRAP, REWORK, DOWNGRADE, HOLD

**Example Response:**
```json
[
  {
    "rejection_code_id": 1,
    "rejection_code": "MAT-DEFECT-001",
    "rejection_name": "Surface Contamination",
    "category_id": 1,
    "rejection_source": "INCOMING_INSPECTION",
    "classification": "HOLD",
    "severity_level": 4,
    "cost_impact_indicator": "HIGH",
    "root_cause_description": "Surface contamination from supplier handling",
    "description": "Material surface has contamination requiring cleaning",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED"
  }
]
```

---

#### Create Material Rejection Code
```http
POST /api/v1/mes-config/material-rejection-codes
```

**Request Body:**
```json
{
  "rejection_code": "MAT-DEFECT-002",
  "rejection_name": "Dimensional Out of Spec",
  "category_id": 1,
  "rejection_source": "INCOMING_INSPECTION",
  "classification": "SCRAP",
  "severity_level": 5,
  "cost_impact_indicator": "HIGH",
  "root_cause_description": "Material dimensions exceed tolerance",
  "description": "Material received with out-of-spec dimensions",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

### 3. Production Rejection Codes

#### List Production Rejection Codes
```http
GET /api/v1/mes-config/production-rejection-codes
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `category_id` (integer)
- `defect_type` (string) - PROCESS, DIMENSIONAL, SURFACE, ASSEMBLY, OTHER
- `defect_source` (string) - OPERATOR, MACHINE, MATERIAL, METHOD, ENVIRONMENT (5M)

**Example Response:**
```json
[
  {
    "rejection_code_id": 1,
    "rejection_code": "PROD-DEFECT-001",
    "rejection_name": "Dimensional - Oversize",
    "category_id": 2,
    "defect_type": "DIMENSIONAL",
    "defect_source": "MACHINE",
    "classification": "REWORK",
    "severity_level": 3,
    "cost_impact_indicator": "MEDIUM",
    "corrective_action_required": 1,
    "root_cause_description": "CNC tool wear causing oversized parts",
    "description": "Part dimension exceeds upper tolerance limit",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED"
  }
]
```

---

#### Create Production Rejection Code
```http
POST /api/v1/mes-config/production-rejection-codes
```

**Request Body:**
```json
{
  "rejection_code": "PROD-DEFECT-002",
  "rejection_name": "Surface Finish - Rough",
  "category_id": 2,
  "defect_type": "SURFACE",
  "defect_source": "OPERATOR",
  "classification": "REWORK",
  "severity_level": 2,
  "cost_impact_indicator": "LOW",
  "corrective_action_required": 0,
  "root_cause_description": "Incorrect feed rate setting",
  "description": "Surface finish rougher than specification",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## KPI Targets Module

**Tag:** `OEE Targets & KPI Configuration`

### 1. OEE Targets

#### List OEE Targets
```http
GET /api/v1/mes-config/oee-targets
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `target_type` (string) - PRODUCT, LINE, MACHINE, SITE
- `product_id` (integer)
- `line_id` (integer)
- `equipment_id` (integer)
- `site_id` (integer)

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/oee-targets?target_type=PRODUCT&product_id=1"
```

**Example Response:**
```json
[
  {
    "target_id": 1,
    "target_type": "PRODUCT",
    "product_id": 1,
    "line_id": null,
    "equipment_id": null,
    "site_id": null,
    "availability_target": "90.00",
    "performance_target": "85.00",
    "quality_target": "95.00",
    "oee_target": "72.68",
    "description": "OEE target for Brake Assembly",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create OEE Target
```http
POST /api/v1/mes-config/oee-targets
```

**Request Body:**
```json
{
  "target_type": "LINE",
  "product_id": null,
  "line_id": 1,
  "equipment_id": null,
  "site_id": null,
  "availability_target": "92.00",
  "performance_target": "88.00",
  "quality_target": "96.00",
  "oee_target": "77.76",
  "description": "OEE target for CNC Line 1",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

**Note:** OEE Target = Availability × Performance × Quality  
Example: 77.76% = 92% × 88% × 96%

---

### 2. KPI Definitions

#### List KPI Definitions
```http
GET /api/v1/mes-config/kpi-definitions
```

**Query Parameters:**
- `skip`, `limit`, `is_active`
- `kpi_category` (string) - QUALITY, PRODUCTIVITY, EFFICIENCY, COST
- `kpi_type` (string) - YIELD, SCRAP_RATE, REWORK_RATE, THROUGHPUT, CAPACITY_UTILIZATION, OEE, DOWNTIME

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/kpi-definitions?kpi_category=QUALITY"
```

**Example Response:**
```json
[
  {
    "kpi_id": 1,
    "kpi_code": "FIRST_PASS_YIELD",
    "kpi_name": "First Pass Yield",
    "kpi_category": "QUALITY",
    "kpi_type": "YIELD",
    "unit_of_measure": "%",
    "target_value": "95.0000",
    "warning_threshold": "90.0000",
    "critical_threshold": "85.0000",
    "calculation_formula_description": "(Good Units / Total Units Produced) × 100",
    "aggregation_level": "PRODUCT",
    "measurement_frequency": "SHIFT",
    "description": "Percentage of units passing inspection on first attempt",
    "is_active": 1,
    "version": 1,
    "approval_status": "APPROVED",
    "created_by": "admin"
  }
]
```

---

#### Create KPI Definition
```http
POST /api/v1/mes-config/kpi-definitions
```

**Request Body:**
```json
{
  "kpi_code": "SCRAP_RATE",
  "kpi_name": "Scrap Rate",
  "kpi_category": "QUALITY",
  "kpi_type": "SCRAP_RATE",
  "unit_of_measure": "%",
  "target_value": "2.0000",
  "warning_threshold": "3.0000",
  "critical_threshold": "5.0000",
  "calculation_formula_description": "(Scrapped Units / Total Units Produced) × 100",
  "aggregation_level": "LINE",
  "measurement_frequency": "SHIFT",
  "description": "Percentage of units scrapped during production",
  "is_active": 1,
  "created_by": "admin",
  "approval_status": "APPROVED"
}
```

---

## Error Responses

### Standard HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

#### 404 Not Found
```json
{
  "detail": "Enterprise not found"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise/999"
```

---

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "enterprise_code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example:** Missing required field
```bash
curl -X POST "http://localhost:8000/api/v1/mes-config/enterprise" \
  -H "Content-Type: application/json" \
  -d '{"enterprise_name": "ABC Corp"}'  # Missing enterprise_code
```

---

#### 400 Bad Request - Unique Constraint Violation
```json
{
  "detail": "Code 'ENT-001' already exists"
}
```

**Example:** Duplicate code
```bash
curl -X POST "http://localhost:8000/api/v1/mes-config/enterprise" \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_code": "ENT-001",
    "enterprise_name": "Duplicate Corp",
    "created_by": "admin"
  }'
```

---

#### 400 Bad Request - Foreign Key Violation
```json
{
  "detail": "Enterprise with ID 999 not found"
}
```

**Example:** Invalid foreign key
```bash
curl -X POST "http://localhost:8000/api/v1/mes-config/sites" \
  -H "Content-Type: application/json" \
  -d '{
    "site_code": "SITE-NEW-01",
    "site_name": "New Site",
    "enterprise_id": 999,
    "created_by": "admin"
  }'
```

---

## Pagination

All list endpoints support pagination via `skip` and `limit` parameters.

### Parameters

- **skip** (integer, default: 0, min: 0) - Number of records to skip
- **limit** (integer, default: 100, min: 1, max: 100) - Number of records to return

### Example: Page 1 (first 50 records)
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/equipment?skip=0&limit=50"
```

### Example: Page 2 (next 50 records)
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/equipment?skip=50&limit=50"
```

### Example: Page 3 (next 50 records)
```bash
curl -X GET "http://localhost:8000/api/v1/mes-config/equipment?skip=100&limit=50"
```

### Response Format
List endpoints return an **array** of entities (not a wrapper object):

```json
[
  {"equipment_id": 1, ...},
  {"equipment_id": 2, ...},
  ...
]
```

**Note:** To get the total count, you need to query without filters and count the results, or use a separate count endpoint (future enhancement).

---

## Approval Workflow

### Approval Status Flow

```
DRAFT → APPROVED → ARCHIVED
  ↑         ↓
  └─────────┘ (can revert to DRAFT for editing)
```

### Approval Status Values

| Status | Description |
|--------|-------------|
| `DRAFT` | Record is in draft state, pending approval |
| `APPROVED` | Record is approved and active for use |
| `ARCHIVED` | Record is archived (soft deleted) |

### Creating a Record in DRAFT State

```bash
curl -X POST "http://localhost:8000/api/v1/mes-config/enterprise" \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_code": "ENT-NEW-01",
    "enterprise_name": "New Enterprise",
    "created_by": "admin",
    "approval_status": "DRAFT"
  }'
```

### Approving a Record

```bash
curl -X PUT "http://localhost:8000/api/v1/mes-config/enterprise/10" \
  -H "Content-Type: application/json" \
  -d '{
    "approval_status": "APPROVED",
    "approved_by": "manager",
    "approved_at": "2025-02-01T16:00:00",
    "updated_by": "admin"
  }'
```

### Archiving a Record (Soft Delete)

```bash
curl -X DELETE "http://localhost:8000/api/v1/mes-config/enterprise/10"
```

**Response:**
```json
{
  "enterprise_id": 10,
  "enterprise_code": "ENT-NEW-01",
  "enterprise_name": "New Enterprise",
  "approval_status": "ARCHIVED",
  "is_active": 0,
  ...
}
```

### Filtering by Approval Status

```bash
# Get only approved enterprises
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise?approval_status=APPROVED"

# Get only draft enterprises
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise?approval_status=DRAFT"

# Get only active enterprises
curl -X GET "http://localhost:8000/api/v1/mes-config/enterprise?is_active=1"
```

---

## Complete Endpoint Summary

### Enterprise Module (18 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/enterprise` | List enterprises |
| GET | `/enterprise/{id}` | Get enterprise by ID |
| POST | `/enterprise` | Create enterprise |
| PUT | `/enterprise/{id}` | Update enterprise |
| DELETE | `/enterprise/{id}` | Archive enterprise |
| GET | `/sites` | List sites |
| GET | `/sites/{id}` | Get site by ID |
| POST | `/sites` | Create site |
| PUT | `/sites/{id}` | Update site |
| DELETE | `/sites/{id}` | Archive site |
| GET | `/areas` | List areas |
| POST | `/areas` | Create area |
| GET | `/lines` | List lines |
| POST | `/lines` | Create line |
| GET | `/departments` | List departments |
| POST | `/departments` | Create department |
| GET | `/shift-calendars` | List shift calendars |
| POST | `/shift-calendars` | Create shift calendar |
| GET | `/unit-of-measures` | List UOMs |
| POST | `/unit-of-measures` | Create UOM |

### Equipment Module (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/equipment` | List equipment |
| GET | `/equipment/{id}` | Get equipment by ID |
| POST | `/equipment` | Create equipment |
| PUT | `/equipment/{id}` | Update equipment |
| DELETE | `/equipment/{id}` | Archive equipment |
| GET | `/equipment-capacity` | List capacities |
| GET | `/equipment-capacity/{id}` | Get capacity by ID |
| POST | `/equipment-capacity` | Create capacity |
| PUT | `/equipment-capacity/{id}` | Update capacity |
| DELETE | `/equipment-capacity/{id}` | Archive capacity |

### Material Module (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/material-categories` | List categories |
| GET | `/material-categories/{id}` | Get category by ID |
| POST | `/material-categories` | Create category |
| PUT | `/material-categories/{id}` | Update category |
| DELETE | `/material-categories/{id}` | Archive category |
| GET | `/materials` | List materials |
| GET | `/materials/{id}` | Get material by ID |
| POST | `/materials` | Create material |
| PUT | `/materials/{id}` | Update material |
| DELETE | `/materials/{id}` | Archive material |

### Product Module (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/product-families` | List families |
| GET | `/product-families/{id}` | Get family by ID |
| POST | `/product-families` | Create family |
| PUT | `/product-families/{id}` | Update family |
| DELETE | `/product-families/{id}` | Archive family |
| GET | `/products` | List products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/products` | Create product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Archive product |
| GET | `/product-equipment-compatibility` | List compatibilities |
| POST | `/product-equipment-compatibility` | Create compatibility |

### Bill of Resources Module (20 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bill-of-resources` | List BORs |
| GET | `/bill-of-resources/{id}` | Get BOR by ID |
| POST | `/bill-of-resources` | Create BOR |
| PUT | `/bill-of-resources/{id}` | Update BOR |
| DELETE | `/bill-of-resources/{id}` | Archive BOR |
| GET | `/bor-materials` | List BOR materials |
| GET | `/bor-materials/{id}` | Get BOR material by ID |
| POST | `/bor-materials` | Create BOR material |
| PUT | `/bor-materials/{id}` | Update BOR material |
| DELETE | `/bor-materials/{id}` | Archive BOR material |
| GET | `/bor-tooling` | List BOR tooling |
| GET | `/bor-tooling/{id}` | Get BOR tooling by ID |
| POST | `/bor-tooling` | Create BOR tooling |
| PUT | `/bor-tooling/{id}` | Update BOR tooling |
| DELETE | `/bor-tooling/{id}` | Archive BOR tooling |
| GET | `/bor-quality-checkpoints` | List checkpoints |
| GET | `/bor-quality-checkpoints/{id}` | Get checkpoint by ID |
| POST | `/bor-quality-checkpoints` | Create checkpoint |
| PUT | `/bor-quality-checkpoints/{id}` | Update checkpoint |
| DELETE | `/bor-quality-checkpoints/{id}` | Archive checkpoint |

### Quality Module (15 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rejection-code-categories` | List categories |
| GET | `/rejection-code-categories/{id}` | Get category by ID |
| POST | `/rejection-code-categories` | Create category |
| PUT | `/rejection-code-categories/{id}` | Update category |
| DELETE | `/rejection-code-categories/{id}` | Archive category |
| GET | `/material-rejection-codes` | List material codes |
| GET | `/material-rejection-codes/{id}` | Get material code by ID |
| POST | `/material-rejection-codes` | Create material code |
| PUT | `/material-rejection-codes/{id}` | Update material code |
| DELETE | `/material-rejection-codes/{id}` | Archive material code |
| GET | `/production-rejection-codes` | List production codes |
| GET | `/production-rejection-codes/{id}` | Get production code by ID |
| POST | `/production-rejection-codes` | Create production code |
| PUT | `/production-rejection-codes/{id}` | Update production code |
| DELETE | `/production-rejection-codes/{id}` | Archive production code |

### KPI Targets Module (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/oee-targets` | List OEE targets |
| GET | `/oee-targets/{id}` | Get OEE target by ID |
| POST | `/oee-targets` | Create OEE target |
| PUT | `/oee-targets/{id}` | Update OEE target |
| DELETE | `/oee-targets/{id}` | Archive OEE target |
| GET | `/kpi-definitions` | List KPI definitions |
| GET | `/kpi-definitions/{id}` | Get KPI definition by ID |
| POST | `/kpi-definitions` | Create KPI definition |
| PUT | `/kpi-definitions/{id}` | Update KPI definition |
| DELETE | `/kpi-definitions/{id}` | Archive KPI definition |

---

**Total: 93 API Endpoints** across 7 modules

---

**END OF API REFERENCE - PHASE_1_CONFIG_ONLY**
