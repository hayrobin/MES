# PHASE_1_CONFIG_ONLY
# This module contains tests for CONFIGURATION data only.

"""
Unit tests for MES Configuration models
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mes_config.database import Base
from mes_config.models import (
    Enterprise, Site, Area, Line,
    EquipmentMaster, EquipmentCapacity,
    MaterialMaster, MaterialCategory,
    ProductMaster, ProductFamily,
    ApprovalStatus
)


@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_enterprise(db_session):
    """Test creating an enterprise"""
    enterprise = Enterprise(
        enterprise_code="TEST001",
        enterprise_name="Test Enterprise",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.DRAFT,
        created_by="test_user",
        is_active=1
    )
    db_session.add(enterprise)
    db_session.commit()
    
    assert enterprise.enterprise_id is not None
    assert enterprise.enterprise_code == "TEST001"
    assert enterprise.approval_status == ApprovalStatus.DRAFT


def test_create_site_with_enterprise(db_session):
    """Test creating a site linked to an enterprise"""
    enterprise = Enterprise(
        enterprise_code="ENT001",
        enterprise_name="Enterprise 1",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(enterprise)
    db_session.commit()
    
    site = Site(
        site_code="SITE001",
        site_name="Test Site",
        enterprise_id=enterprise.enterprise_id,
        timezone="America/New_York",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(site)
    db_session.commit()
    
    assert site.site_id is not None
    assert site.enterprise_id == enterprise.enterprise_id
    assert site.enterprise.enterprise_code == "ENT001"


def test_equipment_hierarchy(db_session):
    """Test equipment parent-child hierarchy"""
    parent_equipment = EquipmentMaster(
        equipment_code="LINE001",
        equipment_name="Production Line 1",
        equipment_type="LINE",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(parent_equipment)
    db_session.commit()
    
    child_equipment = EquipmentMaster(
        equipment_code="MACH001",
        equipment_name="Machine 1",
        equipment_type="MACHINE",
        parent_equipment_id=parent_equipment.equipment_id,
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(child_equipment)
    db_session.commit()
    
    assert child_equipment.parent_equipment_id == parent_equipment.equipment_id
    assert child_equipment.parent_equipment.equipment_code == "LINE001"


def test_material_category_hierarchy(db_session):
    """Test material category hierarchy"""
    parent_category = MaterialCategory(
        category_code="RAW",
        category_name="Raw Materials",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(parent_category)
    db_session.commit()
    
    child_category = MaterialCategory(
        category_code="RAW_METAL",
        category_name="Raw Metal",
        parent_category_id=parent_category.category_id,
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(child_category)
    db_session.commit()
    
    assert child_category.parent_category_id == parent_category.category_id


def test_approval_status_transition(db_session):
    """Test approval status changes"""
    product_family = ProductFamily(
        family_code="FAM001",
        family_name="Product Family 1",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.DRAFT,
        created_by="test_user",
        is_active=1
    )
    db_session.add(product_family)
    db_session.commit()
    
    assert product_family.approval_status == ApprovalStatus.DRAFT
    
    # Approve the record
    product_family.approval_status = ApprovalStatus.APPROVED
    product_family.approved_by = "approver"
    product_family.approved_at = datetime.utcnow()
    db_session.commit()
    
    assert product_family.approval_status == ApprovalStatus.APPROVED
    assert product_family.approved_by == "approver"


def test_equipment_symbolic_linkage(db_session):
    """Test equipment symbolic linkage fields (NO live integration)"""
    equipment = EquipmentMaster(
        equipment_code="MACH001",
        equipment_name="CNC Machine",
        equipment_type="MACHINE",
        opc_namespace="ns=2",
        opc_node_id="i=1001",
        modbus_tag_ref="MACHINE_STATUS_01",
        external_asset_ref="ERP_ASSET_12345",
        effective_from=datetime.utcnow(),
        approval_status=ApprovalStatus.APPROVED,
        created_by="test_user",
        is_active=1
    )
    db_session.add(equipment)
    db_session.commit()
    
    # Verify symbolic references are stored (but NOT used for live integration)
    assert equipment.opc_namespace == "ns=2"
    assert equipment.opc_node_id == "i=1001"
    assert equipment.modbus_tag_ref == "MACHINE_STATUS_01"
    assert equipment.external_asset_ref == "ERP_ASSET_12345"
