# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Seed Data Loader for MES Configuration Layer
Loads initial master data from JSON files
"""

import json
import os
from pathlib import Path
from datetime import datetime, time
from sqlalchemy.orm import Session

from mes_config.database import SessionLocal, init_db
from mes_config.models import (
    Enterprise, Site, Area, Line, Department, ShiftCalendar, UnitOfMeasure,
    EquipmentMaster, EquipmentCapacity,
    MaterialCategory, MaterialMaster,
    ProductFamily, ProductMaster, ProductEquipmentCompatibility,
    BillOfResources, BorMaterial, BorTooling, BorQualityCheckpoint,
    RejectionCodeCategory, MaterialRejectionCode, ProductionRejectionCode,
    OeeTarget, KpiDefinition,
    ApprovalStatus
)


def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO 8601 datetime string"""
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))


def parse_time(time_str: str) -> time:
    """Parse time string (HH:MM:SS)"""
    if not time_str:
        return None
    parts = time_str.split(':')
    return time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)


def load_json_file(file_path: str) -> dict:
    """Load JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def load_enterprise_data(db: Session, data: dict):
    """Load enterprise and organizational data"""
    print("Loading enterprise data...")
    
    # Load enterprises
    for item in data.get('enterprises', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(Enterprise(**item))
    
    # Load sites
    for item in data.get('sites', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(Site(**item))
    
    # Load areas
    for item in data.get('areas', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(Area(**item))
    
    # Load lines
    for item in data.get('lines', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(Line(**item))
    
    # Load departments
    for item in data.get('departments', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(Department(**item))
    
    # Load shift calendars
    for item in data.get('shift_calendars', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        item['start_time'] = parse_time(item['start_time'])
        item['end_time'] = parse_time(item['end_time'])
        db.add(ShiftCalendar(**item))
    
    # Load units of measure
    for item in data.get('units_of_measure', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(UnitOfMeasure(**item))
    
    db.commit()
    print("Enterprise data loaded successfully")


def load_equipment_data(db: Session, data: dict):
    """Load equipment and capacity data"""
    print("Loading equipment data...")
    
    # Load equipment master
    for item in data.get('equipment', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(EquipmentMaster(**item))
    
    # Load equipment capacities
    for item in data.get('equipment_capacities', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(EquipmentCapacity(**item))
    
    db.commit()
    print("Equipment data loaded successfully")


def load_material_data(db: Session, data: dict):
    """Load material master data"""
    print("Loading material data...")
    
    # Load material categories
    for item in data.get('material_categories', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(MaterialCategory(**item))
    
    # Load materials
    for item in data.get('materials', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(MaterialMaster(**item))
    
    db.commit()
    print("Material data loaded successfully")


def load_product_data(db: Session, data: dict):
    """Load product master data"""
    print("Loading product data...")
    
    # Load product families
    for item in data.get('product_families', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(ProductFamily(**item))
    
    # Load products
    for item in data.get('products', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(ProductMaster(**item))
    
    # Load product equipment compatibility
    for item in data.get('product_equipment_compatibility', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(ProductEquipmentCompatibility(**item))
    
    db.commit()
    print("Product data loaded successfully")


def load_bor_data(db: Session, data: dict):
    """Load bill of resources data"""
    print("Loading bill of resources data...")
    
    # Load bill of resources
    for item in data.get('bill_of_resources', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(BillOfResources(**item))
    
    # Load BOR materials
    for item in data.get('bor_materials', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(BorMaterial(**item))
    
    # Load BOR tooling
    for item in data.get('bor_tooling', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(BorTooling(**item))
    
    # Load BOR quality checkpoints
    for item in data.get('bor_quality_checkpoints', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(BorQualityCheckpoint(**item))
    
    db.commit()
    print("Bill of resources data loaded successfully")


def load_rejection_codes_data(db: Session, data: dict):
    """Load rejection codes data"""
    print("Loading rejection codes data...")
    
    # Load rejection code categories
    for item in data.get('rejection_code_categories', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(RejectionCodeCategory(**item))
    
    # Load material rejection codes
    for item in data.get('material_rejection_codes', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(MaterialRejectionCode(**item))
    
    # Load production rejection codes
    for item in data.get('production_rejection_codes', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(ProductionRejectionCode(**item))
    
    db.commit()
    print("Rejection codes data loaded successfully")


def load_oee_targets_data(db: Session, data: dict):
    """Load OEE targets and KPI definitions data"""
    print("Loading OEE targets and KPI definitions data...")
    
    # Load OEE targets
    for item in data.get('oee_targets', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(OeeTarget(**item))
    
    # Load KPI definitions
    for item in data.get('kpi_definitions', []):
        item['effective_from'] = parse_datetime(item['effective_from'])
        item['created_at'] = parse_datetime(item['created_at'])
        item['approval_status'] = ApprovalStatus[item['approval_status']]
        db.add(KpiDefinition(**item))
    
    db.commit()
    print("OEE targets and KPI definitions data loaded successfully")


def load_all_seed_data():
    """Load all seed data from JSON files"""
    print("=" * 80)
    print("MES Configuration Layer - Seed Data Loader")
    print("=" * 80)
    
    # Initialize database
    print("\nInitializing database...")
    init_db()
    print("Database initialized")
    
    # Get seed data directory
    seed_data_dir = Path(__file__).parent.parent / 'seed_data'
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Load data in dependency order
        load_enterprise_data(db, load_json_file(seed_data_dir / 'enterprise.json'))
        load_equipment_data(db, load_json_file(seed_data_dir / 'equipment.json'))
        load_material_data(db, load_json_file(seed_data_dir / 'materials.json'))
        load_product_data(db, load_json_file(seed_data_dir / 'products.json'))
        load_bor_data(db, load_json_file(seed_data_dir / 'bill_of_resources.json'))
        load_rejection_codes_data(db, load_json_file(seed_data_dir / 'rejection_codes.json'))
        load_oee_targets_data(db, load_json_file(seed_data_dir / 'oee_targets.json'))
        
        print("\n" + "=" * 80)
        print("All seed data loaded successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError loading seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_all_seed_data()
