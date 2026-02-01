"""
MES Execution Layer - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mes_execution.api import (
    work_orders_router,
    production_router,
    material_router,
    quality_router,
    equipment_router,
    oee_router,
)

# Create FastAPI application
app = FastAPI(
    title="MES Execution API",
    description="Manufacturing Execution System - Phase 2: Execution & Tracking",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(work_orders_router)
app.include_router(production_router)
app.include_router(material_router)
app.include_router(quality_router)
app.include_router(equipment_router)
app.include_router(oee_router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "MES Execution API - Phase 2",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    # Create database tables on startup
    from mes_execution.database import create_tables
    create_tables()
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
