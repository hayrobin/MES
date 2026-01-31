# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings for MES Configuration Layer"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./mes_config.db"
    
    # API
    API_V1_PREFIX: str = "/api/v1/mes-config"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Application
    APP_NAME: str = "MES Configuration Layer - Phase 1"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
