from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.schemas.template import TemplateCreate, TemplateResponse, TemplateUpdate
import uuid
from datetime import datetime

class TemplateService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_templates(self, user_id: str, skip: int = 0, limit: int = 50) -> List[TemplateResponse]:
        """Get all templates for a user"""
        # Mock data for now - replace with actual database query
        mock_templates = [
            {
                "id": str(uuid.uuid4()),
                "name": "Sales Report Template",
                "description": "Monthly sales performance analysis",
                "category": "sales",
                "tags": ["sales", "monthly", "performance"],
                "is_public": False,
                "query_config": {
                    "tables": ["orders", "customers"],
                    "fields": ["order_date", "total_amount", "customer_name"],
                    "filters": {"status": "completed"}
                },
                "display_config": {
                    "chart_type": "line",
                    "x_axis": "order_date",
                    "y_axis": "total_amount"
                },
                "export_config": {
                    "formats": ["pdf", "excel"],
                    "orientation": "landscape"
                },
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "created_by": user_id,
                "usage_count": 15,
                "last_used": datetime.now()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Customer Analytics",
                "description": "Customer behavior and demographics analysis",
                "category": "analytics",
                "tags": ["customers", "analytics", "demographics"],
                "is_public": True,
                "query_config": {
                    "tables": ["customers", "orders"],
                    "fields": ["customer_id", "total_orders", "avg_order_value"],
                    "group_by": ["customer_id"]
                },
                "display_config": {
                    "chart_type": "bar",
                    "x_axis": "customer_id",
                    "y_axis": "total_orders"
                },
                "export_config": {
                    "formats": ["pdf", "csv"],
                    "orientation": "portrait"
                },
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "created_by": user_id,
                "usage_count": 8,
                "last_used": datetime.now()
            }
        ]
        
        return [TemplateResponse(**template) for template in mock_templates[skip:skip+limit]]

    def create_template(self, template: TemplateCreate, user_id: str) -> TemplateResponse:
        """Create a new template"""
        # Mock template creation - replace with actual database insert
        new_template = {
            "id": str(uuid.uuid4()),
            "name": template.name,
            "description": template.description,
            "category": template.category,
            "tags": template.tags or [],
            "is_public": template.is_public,
            "query_config": template.query_config,
            "display_config": template.display_config or {},
            "export_config": template.export_config or {},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": user_id,
            "usage_count": 0,
            "last_used": None
        }
        
        return TemplateResponse(**new_template)

    def get_template(self, template_id: str, user_id: str) -> Optional[TemplateResponse]:
        """Get a specific template by ID"""
        # Mock template retrieval - replace with actual database query
        mock_template = {
            "id": template_id,
            "name": "Sample Template",
            "description": "A sample template for testing",
            "category": "sample",
            "tags": ["sample", "test"],
            "is_public": False,
            "query_config": {
                "tables": ["sample_table"],
                "fields": ["id", "name"]
            },
            "display_config": {},
            "export_config": {},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": user_id,
            "usage_count": 0,
            "last_used": None
        }
        
        return TemplateResponse(**mock_template)

    def update_template(self, template_id: str, template_update: TemplateUpdate, user_id: str) -> Optional[TemplateResponse]:
        """Update an existing template"""
        # Mock template update - replace with actual database update
        existing_template = self.get_template(template_id, user_id)
        if not existing_template:
            return None
        
        # Update fields if provided
        update_data = template_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_template, field, value)
        
        existing_template.updated_at = datetime.now()
        return existing_template

    def delete_template(self, template_id: str, user_id: str) -> bool:
        """Delete a template"""
        # Mock template deletion - replace with actual database delete
        # Check if template exists and user has permission
        template = self.get_template(template_id, user_id)
        if not template:
            return False
        
        # Mock successful deletion
        return True

    def duplicate_template(self, template_id: str, user_id: str) -> TemplateResponse:
        """Duplicate an existing template"""
        # Mock template duplication - replace with actual database logic
        original_template = self.get_template(template_id, user_id)
        if not original_template:
            raise ValueError("Template not found")
        
        # Create duplicate with new ID and name
        duplicate_template = {
            "id": str(uuid.uuid4()),
            "name": f"{original_template.name} (Copy)",
            "description": original_template.description,
            "category": original_template.category,
            "tags": original_template.tags + ["copy"],
            "is_public": False,  # Duplicates are always private
            "query_config": original_template.query_config,
            "display_config": original_template.display_config,
            "export_config": original_template.export_config,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": user_id,
            "usage_count": 0,
            "last_used": None
        }
        
        return TemplateResponse(**duplicate_template)
