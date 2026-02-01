"""
API endpoints for MES Execution Layer
"""

from .work_orders import router as work_orders_router
from .production import router as production_router
from .material import router as material_router
from .quality import router as quality_router
from .equipment_status import router as equipment_router
from .oee import router as oee_router

__all__ = [
    "work_orders_router",
    "production_router",
    "material_router",
    "quality_router",
    "equipment_router",
    "oee_router",
]
