# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
MES Configuration Layer - Phase 1
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mes_config.config import settings
from mes_config.database import init_db, Base, engine
from mes_config.api import (
    enterprise_router,
    equipment_router,
    material_router,
    product_router,
    bill_of_resources_router,
    quality_router,
    kpi_targets_router,
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="MES Master Data & Configuration Layer - Phase 1 (CONFIGURATION ONLY)",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("Initializing MES Configuration database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down MES Configuration service...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "phase": "PHASE_1_CONFIG_ONLY",
        "description": "MES Master Data & Configuration Layer",
        "documentation": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MES Configuration Layer",
        "phase": "PHASE_1_CONFIG_ONLY"
    }


# Register API routers with prefix
app.include_router(
    enterprise_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Enterprise & Organizational Configuration"]
)

app.include_router(
    equipment_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Equipment & Capacity"]
)

app.include_router(
    material_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Material Master"]
)

app.include_router(
    product_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Product & Production"]
)

app.include_router(
    bill_of_resources_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Bill of Resources"]
)

app.include_router(
    quality_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Quality & Rejection Codes"]
)

app.include_router(
    kpi_targets_router,
    prefix=settings.API_V1_PREFIX,
    tags=["OEE Targets & KPI Configuration"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
