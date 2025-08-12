from fastapi import APIRouter

from app.api.v1.endpoints import health, reports, permissions, data_sources, templates

api_router = APIRouter()

# Include health endpoint
api_router.include_router(health.router, tags=["health"])

# Include reports endpoints
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])

# Include permissions endpoints
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])

# Include data sources endpoints
api_router.include_router(data_sources.router, prefix="/data-sources", tags=["data-sources"])

# Include templates endpoints
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
