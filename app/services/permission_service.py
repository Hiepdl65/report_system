from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User
from app.models.template import ReportTemplate
from app.models.permission import TemplatePermission
from app.schemas.permission import PermissionGrantRequest, PermissionResponse, TemplatePermissionsResponse
import uuid

class PermissionService:
    def __init__(self, db: Session):
        self.db = db
    
    def grant_permissions(self, request: PermissionGrantRequest, granter_id: str) -> List[PermissionResponse]:
        """Grant permissions to users for a template"""
        try:
            # Verify template exists and granter has admin permission
            template = self.db.query(ReportTemplate).filter(
                ReportTemplate.id == request.template_id
            ).first()
            
            if not template:
                raise ValueError("Template not found")
            
            # Check if granter has admin permission or is owner
            if not self._has_admin_permission(request.template_id, granter_id):
                raise ValueError("Insufficient permissions to grant access")
            
            granted_permissions = []
            
            # Process each user email
            for email in request.user_emails:
                user = self.db.query(User).filter(User.email == email).first()
                if not user:
                    continue  # Skip non-existent users
                
                # Check if permission already exists
                existing_permission = self.db.query(TemplatePermission).filter(
                    and_(
                        TemplatePermission.template_id == request.template_id,
                        TemplatePermission.user_id == user.id
                    )
                ).first()
                
                if existing_permission:
                    # Update existing permission
                    existing_permission.permission_type = request.permission_type
                    permission = existing_permission
                else:
                    # Create new permission
                    permission = TemplatePermission(
                        id=str(uuid.uuid4()),
                        template_id=request.template_id,
                        user_id=user.id,
                        permission_type=request.permission_type,
                        granted_by=granter_id
                    )
                    self.db.add(permission)
                
                self.db.commit()
                
                # Add to response
                granted_permissions.append(PermissionResponse(
                    id=permission.id,
                    template_id=permission.template_id,
                    user_id=permission.user_id,
                    user_email=user.email,
                    user_name=user.full_name,
                    permission_type=permission.permission_type,
                    granted_by=granter_id,
                    granted_at=permission.granted_at.isoformat()
                ))
            
            return granted_permissions
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to grant permissions: {str(e)}")
    
    def get_template_permissions(self, template_id: str, requester_id: str) -> TemplatePermissionsResponse:
        """Get all permissions for a template"""
        # Verify requester has access to view permissions
        if not self._has_admin_permission(template_id, requester_id):
            raise ValueError("Insufficient permissions to view template permissions")
        
        template = self.db.query(ReportTemplate).filter(
            ReportTemplate.id == template_id
        ).first()
        
        if not template:
            raise ValueError("Template not found")
        
        # Get all permissions
        permissions_query = self.db.query(TemplatePermission, User).join(
            User, TemplatePermission.user_id == User.id
        ).filter(TemplatePermission.template_id == template_id)
        
        permissions = []
        for perm, user in permissions_query.all():
            permissions.append(PermissionResponse(
                id=perm.id,
                template_id=perm.template_id,
                user_id=perm.user_id,
                user_email=user.email,
                user_name=user.full_name,
                permission_type=perm.permission_type,
                granted_by=perm.granted_by,
                granted_at=perm.granted_at.isoformat()
            ))
        
        return TemplatePermissionsResponse(
            template_id=template_id,
            template_name=template.name,
            permissions=permissions
        )
    
    def revoke_permission(self, template_id: str, user_id: str, requester_id: str) -> bool:
        """Revoke permission for a user"""
        # Check if requester has admin permission
        if not self._has_admin_permission(template_id, requester_id):
            raise ValueError("Insufficient permissions to revoke access")
        
        permission = self.db.query(TemplatePermission).filter(
            and_(
                TemplatePermission.template_id == template_id,
                TemplatePermission.user_id == user_id
            )
        ).first()
        
        if permission:
            self.db.delete(permission)
            self.db.commit()
            return True
        
        return False
    
    def check_permission(self, template_id: str, user_id: str, required_permission: str) -> bool:
        """Check if user has required permission for template"""
        # Check if user is template owner
        template = self.db.query(ReportTemplate).filter(
            and_(
                ReportTemplate.id == template_id,
                ReportTemplate.created_by == user_id
            )
        ).first()
        
        if template:
            return True  # Owner has all permissions
        
        # Check explicit permissions
        permission = self.db.query(TemplatePermission).filter(
            and_(
                TemplatePermission.template_id == template_id,
                TemplatePermission.user_id == user_id
            )
        ).first()
        
        if not permission:
            return False
        
        # Permission hierarchy: admin > write > read
        user_perm = permission.permission_type
        
        if required_permission == "read":
            return user_perm in ["read", "write", "admin"]
        elif required_permission == "write":
            return user_perm in ["write", "admin"]
        elif required_permission == "admin":
            return user_perm == "admin"
        
        return False
    
    def _has_admin_permission(self, template_id: str, user_id: str) -> bool:
        """Check if user has admin permission for template"""
        return self.check_permission(template_id, user_id, "admin")