from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class DataSourceType(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLSERVER = "sqlserver"
    ORACLE = "oracle"
    CSV = "csv"
    EXCEL = "excel"
    API = "api"

class DataSourceStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class DataSourceConnectionRequest(BaseModel):
    name: str = Field(..., description="Data source name")
    type: DataSourceType = Field(..., description="Data source type")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: Optional[str] = Field(None, description="Database name")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    connection_string: Optional[str] = Field(None, description="Full connection string")
    file_path: Optional[str] = Field(None, description="File path for file-based sources")
    api_url: Optional[str] = Field(None, description="API URL for API-based sources")
    api_key: Optional[str] = Field(None, description="API key for authentication")

class DataSourceResponse(BaseModel):
    id: str = Field(..., description="Data source ID")
    name: str = Field(..., description="Data source name")
    type: DataSourceType = Field(..., description="Data source type")
    status: DataSourceStatus = Field(..., description="Connection status")
    host: Optional[str] = Field(None, description="Database host")
    port: Optional[int] = Field(None, description="Database port")
    database: Optional[str] = Field(None, description="Database name")
    username: Optional[str] = Field(None, description="Database username")
    file_path: Optional[str] = Field(None, description="File path for file-based sources")
    api_url: Optional[str] = Field(None, description="API URL for API-based sources")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    created_by: str = Field(..., description="User ID who created the data source")
    is_active: bool = Field(..., description="Whether the data source is active")

class TableInfo(BaseModel):
    name: str = Field(..., description="Table name")
    table_schema: Optional[str] = Field(None, description="Table schema")
    type: str = Field(..., description="Table type (table, view, etc.)")
    row_count: Optional[int] = Field(None, description="Approximate row count")
    size_mb: Optional[float] = Field(None, description="Table size in MB")

class ColumnInfo(BaseModel):
    name: str = Field(..., description="Column name")
    type: str = Field(..., description="Column data type")
    nullable: bool = Field(..., description="Whether column can be null")
    primary_key: bool = Field(..., description="Whether column is primary key")
    default_value: Optional[str] = Field(None, description="Default value")
    description: Optional[str] = Field(None, description="Column description")
