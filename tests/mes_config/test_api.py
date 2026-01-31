# PHASE_1_CONFIG_ONLY
# This module contains tests for CONFIGURATION data only.

"""
Integration tests for MES Configuration API
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["phase"] == "PHASE_1_CONFIG_ONLY"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["phase"] == "PHASE_1_CONFIG_ONLY"


def test_api_docs_available(client):
    """Test that API documentation is available"""
    response = client.get("/api/docs")
    assert response.status_code == 200
    
    
def test_api_structure(client):
    """Test basic API structure"""
    # Test that root works
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["phase"] == "PHASE_1_CONFIG_ONLY"
    
    # Test health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    # Test docs are available
    response = client.get("/api/docs")
    assert response.status_code == 200
