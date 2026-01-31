# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
API Router initialization
"""

from .enterprise import router as enterprise_router
from .equipment import router as equipment_router
from .material import router as material_router
from .product import router as product_router
from .bill_of_resources import router as bill_of_resources_router
from .quality import router as quality_router
from .kpi_targets import router as kpi_targets_router

__all__ = [
    "enterprise_router",
    "equipment_router",
    "material_router",
    "product_router",
    "bill_of_resources_router",
    "quality_router",
    "kpi_targets_router",
]
