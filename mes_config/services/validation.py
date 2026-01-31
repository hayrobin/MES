# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Validation utilities for configuration data
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def validate_unique_code(
    db: Session,
    model: type,
    code_field: str,
    code_value: str,
    exclude_id: Optional[int] = None,
    id_field: str = "id"
) -> None:
    """
    Validate that a code is unique in the database
    
    Args:
        db: Database session
        model: SQLAlchemy model class
        code_field: Name of the code field to check
        code_value: Value to check for uniqueness
        exclude_id: ID to exclude from check (for updates)
        id_field: Name of the ID field
    
    Raises:
        HTTPException: If code already exists
    """
    try:
        query = db.query(model).filter(getattr(model, code_field) == code_value)
        
        if exclude_id is not None:
            query = query.filter(getattr(model, id_field) != exclude_id)
        
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{code_field} '{code_value}' already exists"
            )
    except Exception as e:
        # If table doesn't exist yet, skip validation (let database handle it)
        if "no such table" not in str(e).lower() and "does not exist" not in str(e).lower():
            raise


def validate_effective_dates(
    effective_from: datetime,
    effective_to: Optional[datetime] = None
) -> None:
    """
    Validate that effective dates are logical
    
    Args:
        effective_from: Start date
        effective_to: End date (optional)
    
    Raises:
        HTTPException: If dates are invalid
    """
    if effective_to and effective_from >= effective_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="effective_from must be before effective_to"
        )


def validate_foreign_key_exists(
    db: Session,
    model: type,
    id_field: str,
    id_value: int,
    resource_name: str
) -> None:
    """
    Validate that a foreign key reference exists
    
    Args:
        db: Database session
        model: SQLAlchemy model class to check
        id_field: Name of the ID field
        id_value: ID value to check
        resource_name: Human-readable name for error messages
    
    Raises:
        HTTPException: If reference doesn't exist
    """
    if not db.query(model).filter(getattr(model, id_field) == id_value).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} with id {id_value} not found"
        )
