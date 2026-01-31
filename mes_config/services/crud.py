# PHASE_1_CONFIG_ONLY
# This module contains CONFIGURATION data only.
# NO execution logic, NO live telemetry integration.

"""
Generic CRUD operations for configuration entities
"""

from typing import TypeVar, Generic, Type, List, Optional, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from mes_config.models.governance import ApprovalStatus, AuditAction, AuditTrail

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[int] = None,
        approval_status: Optional[ApprovalStatus] = None
    ) -> List[ModelType]:
        """Get multiple records with optional filters"""
        query = db.query(self.model)
        
        # Filter by is_active if model has this field
        if is_active is not None and hasattr(self.model, 'is_active'):
            query = query.filter(self.model.is_active == is_active)
        
        # Filter by approval_status if specified
        if approval_status is not None and hasattr(self.model, 'approval_status'):
            query = query.filter(self.model.approval_status == approval_status)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: CreateSchemaType, created_by: str = "system") -> ModelType:
        """Create a new record"""
        obj_data = obj_in.model_dump()
        obj_data['created_by'] = created_by
        obj_data['created_at'] = datetime.utcnow()
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Create audit trail entry
        self._create_audit_trail(
            db, db_obj, AuditAction.INSERT, created_by, None, obj_data
        )
        
        return db_obj
    
    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        updated_by: str = "system"
    ) -> ModelType:
        """Update an existing record"""
        # Store old values for audit
        old_values = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        
        # Update fields
        obj_data = obj_in.model_dump(exclude_unset=True)
        obj_data['updated_by'] = updated_by
        obj_data['updated_at'] = datetime.utcnow()
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        
        # Create audit trail entry
        new_values = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        self._create_audit_trail(
            db, db_obj, AuditAction.UPDATE, updated_by, old_values, new_values
        )
        
        return db_obj
    
    def delete(self, db: Session, id: int, deleted_by: str = "system") -> ModelType:
        """Soft delete (archive) a record"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        
        # Store old values for audit
        old_values = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        
        # Soft delete by setting approval_status to ARCHIVED
        obj.approval_status = ApprovalStatus.ARCHIVED
        obj.updated_by = deleted_by
        obj.updated_at = datetime.utcnow()
        
        # Only set effective_to if not already set
        if hasattr(obj, 'effective_to') and obj.effective_to is None:
            obj.effective_to = datetime.utcnow()
        
        if hasattr(obj, 'is_active'):
            obj.is_active = 0
        
        db.commit()
        db.refresh(obj)
        
        # Create audit trail entry
        new_values = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        self._create_audit_trail(
            db, obj, AuditAction.ARCHIVE, deleted_by, old_values, new_values
        )
        
        return obj
    
    def approve(self, db: Session, id: int, approved_by: str) -> ModelType:
        """Approve a draft record"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        
        if obj.approval_status != ApprovalStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only DRAFT records can be approved"
            )
        
        # Store old values for audit
        old_values = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        
        obj.approval_status = ApprovalStatus.APPROVED
        obj.approved_by = approved_by
        obj.approved_at = datetime.utcnow()
        obj.updated_by = approved_by
        obj.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(obj)
        
        # Create audit trail entry
        new_values = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        self._create_audit_trail(
            db, obj, AuditAction.APPROVE, approved_by, old_values, new_values
        )
        
        return obj
    
    def _create_audit_trail(
        self,
        db: Session,
        obj: ModelType,
        action: AuditAction,
        changed_by: str,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None
    ):
        """Create an audit trail entry"""
        # Get primary key value
        pk_column = list(obj.__table__.primary_key.columns)[0]
        record_id = getattr(obj, pk_column.name)
        
        audit_entry = AuditTrail(
            table_name=obj.__tablename__,
            record_id=record_id,
            action=action,
            changed_by=changed_by,
            old_values=old_values,
            new_values=new_values
        )
        db.add(audit_entry)
        db.commit()
