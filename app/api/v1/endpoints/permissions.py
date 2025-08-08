from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.permission import (
    PermissionGrantRequest, 
    PermissionResponse, 
    TemplatePermissionsResponse
)
from app.services.permission_service import PermissionService

router = APIRouter()

@router.post("/grant", response_model=List[PermissionResponse])
async def grant_template_permissions(
    request: PermissionGrantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Grant permissions to users for a specific template
    
    Body:
    {
        "template_id": "uuid",
        "user_emails": ["user1@email.com", "user2@email.com"],
        "permission_type": "read" | "write" | "admin"
    }
    
    Returns:
    - List of granted permissions with user details
    """
    try:
        permission_service = PermissionService(db)
        permissions = permission_service.grant_permissions(request, current_user.id)
        return permissions
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to grant permissions"
        )

@router.get("/template/{template_id}", response_model=TemplatePermissionsResponse)
async def get_template_permissions(
    template_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all permissions for a specific template
    """
    try:
        permission_service = PermissionService(db)
        permissions = permission_service.get_template_permissions(template_id, current_user.id)
        return permissions
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.delete("/template/{template_id}/user/{user_id}")
async def revoke_template_permission(
    template_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Revoke permission for a specific user on a template
    """
    try:
        permission_service = PermissionService(db)
        success = permission_service.revoke_permission(template_id, user_id, current_user.id)
        
        if success:
            return {"message": "Permission revoked successfully"}
        else:
            return {"message": "Permission not found"}
            
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

@router.get("/check/{template_id}")
async def check_template_permission(
    template_id: str,
    permission: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Check if current user has specific permission for a template
    """
    permission_service = PermissionService(db)
    has_permission = permission_service.check_permission(
        template_id, current_user.id, permission
    )
    
    return {
        "template_id": template_id,
        "user_id": current_user.id,
        "permission": permission,
        "has_permission": has_permission
    }