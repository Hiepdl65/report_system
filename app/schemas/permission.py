from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class PermissionType(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class PermissionGrantRequest(BaseModel):
    template_id: str
    user_emails: List[str]
    permission_type: PermissionType

class PermissionResponse(BaseModel):
    id: str
    template_id: str
    user_id: str
    user_email: str
    user_name: str
    permission_type: PermissionType
    granted_by: str
    granted_at: str

class TemplatePermissionsResponse(BaseModel):
    template_id: str
    template_name: str
    permissions: List[PermissionResponse]