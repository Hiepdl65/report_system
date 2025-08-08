# app/__init__.py
"""
Report Builder Backend Application

FastAPI-based backend for dynamic report generation system.
"""

__version__ = "1.0.0"
__author__ = "Your Team"
__email__ = "team@yourcompany.com"

# Version info
VERSION = __version__

# Package metadata
PACKAGE_NAME = "report-builder-backend"
DESCRIPTION = "Dynamic Report Generation System"

# Import main application factory
from app.main import create_application as create_app

# Package-level exports
__all__ = [
    "create_app",
    "VERSION",
    "PACKAGE_NAME",
    "DESCRIPTION"
]

# Optional: Package-level configuration
import logging

# Configure package-level logging
logger = logging.getLogger(__name__)
logger.info(f"Initializing {PACKAGE_NAME} v{VERSION}")