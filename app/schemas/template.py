from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TemplateCreate(BaseModel):
    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    category: Optional[str] = Field(None, description="Template category")
    tags: Optional[List[str]] = Field(None, description="Template tags")
    is_public: bool = Field(False, description="Whether template is public")
    query_config: Dict[str, Any] = Field(..., description="Query configuration")
    display_config: Optional[Dict[str, Any]] = Field(None, description="Display configuration")
    export_config: Optional[Dict[str, Any]] = Field(None, description="Export configuration")

class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    category: Optional[str] = Field(None, description="Template category")
    tags: Optional[List[str]] = Field(None, description="Template tags")
    is_public: Optional[bool] = Field(None, description="Whether template is public")
    query_config: Optional[Dict[str, Any]] = Field(None, description="Query configuration")
    display_config: Optional[Dict[str, Any]] = Field(None, description="Display configuration")
    export_config: Optional[Dict[str, Any]] = Field(None, description="Export configuration")

class TemplateResponse(BaseModel):
    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    category: Optional[str] = Field(None, description="Template category")
    tags: List[str] = Field(..., description="Template tags")
    is_public: bool = Field(..., description="Whether template is public")
    query_config: Dict[str, Any] = Field(..., description="Query configuration")
    display_config: Dict[str, Any] = Field(..., description="Display configuration")
    export_config: Dict[str, Any] = Field(..., description="Export configuration")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: str = Field(..., description="User ID who created the template")
    usage_count: int = Field(..., description="Number of times template was used")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")

class TemplateListResponse(BaseModel):
    templates: List[TemplateResponse] = Field(..., description="List of templates")
    total: int = Field(..., description="Total number of templates")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
