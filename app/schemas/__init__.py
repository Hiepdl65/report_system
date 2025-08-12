#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pydantic schemas for Report System
"""

from .data_source import DataSourceResponse, DataSourceConnectionRequest, TableInfo, ColumnInfo
from .template import TemplateCreate, TemplateResponse, TemplateUpdate
from .permission import PermissionGrantRequest, PermissionResponse, TemplatePermissionsResponse
from .query import ReportRunRequest, ReportRunResponse

__all__ = [
    "DataSourceResponse", "DataSourceConnectionRequest", "TableInfo", "ColumnInfo",
    "TemplateCreate", "TemplateResponse", "TemplateUpdate",
    "PermissionGrantRequest", "PermissionResponse", "TemplatePermissionsResponse",
    "ReportRunRequest", "ReportRunResponse"
]
