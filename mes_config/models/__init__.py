# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
MES Configuration Layer - All Models
Phase 1: Master Data & Configuration
"""

# Module 8: Governance & Control
from .governance import (
    GovernanceMixin,
    ApprovalStatus,
    AuditAction,
    AuditTrail,
    UserRole,
    RolePermission,
)

# Module 1: Enterprise & Organizational Configuration
from .enterprise import (
    Enterprise,
    Site,
    Area,
    Line,
    Department,
    ShiftCalendar,
    UnitOfMeasure,
)

# Module 2: Equipment & Capacity Definition
from .equipment import (
    EquipmentMaster,
    EquipmentCapacity,
)

# Module 3: Material Master
from .material import (
    MaterialCategory,
    MaterialMaster,
)

# Module 4: Product & Production Definitions
from .product import (
    ProductFamily,
    ProductMaster,
    ProductEquipmentCompatibility,
)

# Module 5: Bill of Resources
from .bill_of_resources import (
    BillOfResources,
    BorMaterial,
    BorTooling,
    BorQualityCheckpoint,
)

# Module 6: Quality Rejection & Defect Codes
from .quality import (
    RejectionCodeCategory,
    MaterialRejectionCode,
    ProductionRejectionCode,
)

# Module 7: OEE Targets & KPI Configuration
from .kpi_targets import (
    OeeTarget,
    KpiDefinition,
)

__all__ = [
    # Governance
    "GovernanceMixin",
    "ApprovalStatus",
    "AuditAction",
    "AuditTrail",
    "UserRole",
    "RolePermission",
    # Enterprise
    "Enterprise",
    "Site",
    "Area",
    "Line",
    "Department",
    "ShiftCalendar",
    "UnitOfMeasure",
    # Equipment
    "EquipmentMaster",
    "EquipmentCapacity",
    # Material
    "MaterialCategory",
    "MaterialMaster",
    # Product
    "ProductFamily",
    "ProductMaster",
    "ProductEquipmentCompatibility",
    # Bill of Resources
    "BillOfResources",
    "BorMaterial",
    "BorTooling",
    "BorQualityCheckpoint",
    # Quality
    "RejectionCodeCategory",
    "MaterialRejectionCode",
    "ProductionRejectionCode",
    # KPI Targets
    "OeeTarget",
    "KpiDefinition",
]
