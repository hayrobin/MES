# MES Configuration Layer - Seed Data

This directory contains comprehensive seed data JSON files for the MES Configuration Layer.

## Overview

The seed data represents a realistic automotive parts manufacturing environment for **ABC Manufacturing Corp** with two plants and multiple production lines.

## File Descriptions

### 1. enterprise.json (511 lines)
Enterprise structure and organizational hierarchy:
- **1 Enterprise**: ABC Manufacturing Corp
- **2 Sites**: 
  - Plant North (Detroit, MI - America/New_York timezone)
  - Plant South (Chicago, IL - America/Chicago timezone)
- **6 Areas**: 3 per site (Assembly, Machining, Packaging)
- **12 Lines**: 2 per area (6 lines per site)
- **4 Departments**: Production, Quality, Maintenance, Planning
- **2 Shift Calendars**: 3-shift weekday operation (Morning 06:00-14:00, Afternoon 14:00-22:00, Night 22:00-06:00)
- **8 Units of Measure**: pieces, kg, liter, meter, hour, minute, ton, cycle

### 2. equipment.json (543 lines)
Equipment hierarchy and data sources:
- **15 Equipment items** across both sites
  - 5 CNC machines (milling, turning)
  - 1 surface grinder
  - 3 assembly cells/robots
  - 2 packaging lines
  - 1 hydraulic press
  - 1 blister packaging machine
  - 1 labeling system
  - 1 tooling/fixture set
- **Equipment types**: MACHINE, LINE, CELL, TOOL
- **Criticality levels**: Low, Medium, High, Critical
- **4 Bottleneck machines** marked
- **9 OPC UA / Modbus data sources** with realistic connection strings
- **11 Equipment capacity** definitions with rated throughput

### 3. materials.json (464 lines)
Material master data:
- **4 Material categories**: Raw Materials, Semi-Finished, Finished Goods, Consumables
- **5 Raw materials**: Steel sheet, aluminum coil, plastic pellets, rubber compound, brass rod
- **3 Semi-finished materials**: Machined bracket, turned shaft, cast housing
- **5 Finished goods**: Brake assembly, steering component, precision bearing, transmission gear, drive shaft
- **4 Consumables**: Cutting oil, grease, labels, corrugated boxes
- **Tracking types**: LOT, SERIAL, BATCH, NONE
- **Shelf life specifications** for time-sensitive materials
- **8 Material specifications** for critical quality parameters

### 4. products.json (381 lines)
Product definitions and routing:
- **2 Product families**: Product Line A (brake/steering), Product Line B (transmission/drivetrain)
- **5 Products** with standard cycle times and output rates:
  - PROD-A100: Brake Assembly (180s cycle, 20/hr)
  - PROD-B200: Steering Component (240s cycle, 15/hr)
  - PROD-C300: Precision Bearing (300s cycle, 12/hr)
  - PROD-D400: Transmission Gear (420s cycle, 8.5/hr)
  - PROD-E500: Drive Shaft (360s cycle, 10/hr)
- **13 Product-equipment compatibility** mappings with setup/changeover times
- **5 Product capacity constraints** at line level
- **5 Product versions** tracking design changes

### 5. bill_of_resources.json (705 lines)
Manufacturing process definitions:
- **5 Bill of Resources** (one per product)
- **18 Operations** across all products with:
  - Machining operations (milling, turning, grinding, drilling)
  - Heat treatment (external process)
  - Assembly operations
  - Testing and inspection
  - Packaging
- **14 Material requirements** with quantities and scrap factors
- **5 Tooling requirements** with tool life specifications
- **11 Quality checkpoints** (INCOMING, IN_PROCESS, FINAL)
  - Inspection frequencies: FIRST_PIECE, EVERY_UNIT, PERIODIC
  - Sample sizes defined

### 6. rejection_codes.json (485 lines)
Quality rejection and defect codes:
- **6 Rejection categories**: Material, Production, Dimensional, Surface, Assembly, Functional defects
- **25 Rejection codes** with detailed classifications:
  - **10 Material defects**: Supplier defects, contamination, wrong grade, moisture damage, physical damage, expired, packaging damage, certification issues, dimensional non-conformance, color variation
  - **15 Production defects**: Over/under tolerance, surface scratches/roughness, tool marks, burrs, porosity, cracks, hardness issues, incomplete operations, wrong part number, assembly errors, functional test failures
- **Severity levels**: LOW, MEDIUM, HIGH, CRITICAL
- **Classifications**: SUPPLIER, STORAGE, HANDLING, MACHINING, GRINDING, FINISHING, CASTING, HEAT_TREATMENT, PROCESS, ASSEMBLY, TESTING
- **Disposition requirements** and auto-scrap flags

### 7. oee_targets.json (554 lines)
OEE targets and KPI definitions:
- **16 OEE targets** at multiple levels:
  - **5 Product-level targets** (OEE: 71.8% - 84.3%)
  - **6 Line-level targets** (OEE: 69.2% - 88.0%)
  - **2 Site-level targets** (OEE: 78.5% - 80.7%)
  - **3 Equipment-level targets** for bottleneck machines
- **12 KPI definitions**:
  - **Quality KPIs**: Yield %, Scrap Rate %, Rework Rate %, First Time Through %
  - **Productivity KPIs**: OEE %, Throughput, Capacity Utilization %, Actual Cycle Time
  - **Maintenance KPIs**: Downtime, MTBF, MTTR
  - **Delivery KPIs**: On-Time Delivery %
- Each KPI includes calculation formula, target values, and threshold ranges

## Data Relationships

The seed data is fully interconnected with proper foreign key relationships:

```
Enterprise (1)
  └─ Sites (2)
      ├─ Areas (6)
      │   └─ Lines (12)
      │       └─ Equipment (15)
      └─ Shift Calendars (2)
          └─ Shifts (6)

Products (5)
  ├─ Product Families (2)
  ├─ Product-Equipment Compatibility (13)
  ├─ Product Capacity Constraints (5)
  ├─ Product Versions (5)
  └─ Bill of Resources (5)
      ├─ Operations (18)
      │   ├─ Material Requirements (14)
      │   ├─ Tooling Requirements (5)
      │   └─ Quality Checkpoints (11)
      └─ Equipment Linkages

Materials (17)
  ├─ Material Categories (4)
  └─ Material Specifications (8)

Equipment (15)
  ├─ Data Sources (9)
  └─ Capacities (11)

Rejection Codes (25)
  └─ Categories (6)

OEE Targets (16)
  └─ KPI Definitions (12)
```

## Key Statistics

- **Total entities**: 200+ master data records
- **Lines of JSON**: 3,643
- **Total size**: ~116 KB
- **Approval status**: Most records APPROVED, some DRAFT for testing
- **Date range**: Effective from 2024-01-01
- **ID strategy**: Sequential integers starting from 1 per entity type

## Data Quality Features

- ✅ All JSON files validated for proper syntax
- ✅ ISO 8601 datetime format used throughout
- ✅ Realistic manufacturing values based on industry standards
- ✅ Proper foreign key references maintained
- ✅ Required fields populated for all records
- ✅ Metadata tracking (created_by, created_at, updated_by, updated_at)
- ✅ Approval workflow status fields included
- ✅ Active/inactive flags for soft deletes

## Usage

These seed data files can be used to:
1. Initialize a new MES database
2. Test MES application functionality
3. Demonstrate system capabilities
4. Train users on realistic manufacturing scenarios
5. Benchmark performance with realistic data volumes

## Notes

- OPC UA and Modbus connection strings are symbolic (fake but realistic format)
- External processes (heat treatment) have null equipment_id
- Shelf life calculations should be implemented in application logic
- Scrap factors are percentages (e.g., 5.0 = 5%)
- Time values use consistent units as specified by UOM references
