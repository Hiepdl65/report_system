# app/api/v1/api.py
"""
API v1 router aggregation.

This file aggregates all v1 API endpoints into a single router.
"""

from fastapi import APIRouter

# Import endpoint routers
from app.api.v1.endpoints import health, reports

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health.router, 
    tags=["health"]
)

api_router.include_router(
    reports.router, 
    prefix="/reports",
    tags=["reports"]
)

# Export the main router
__all__ = ["api_router"]

import logging
logger = logging.getLogger(__name__)
logger.info("API v1 router initialized with all endpoints")

# Log registered routes for debugging
routes_count = len(api_router.routes)
logger.debug(f"Registered {routes_count} routes in API v1")