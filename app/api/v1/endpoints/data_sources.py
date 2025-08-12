from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.schemas.data_source import DataSourceResponse, DataSourceConnectionRequest
from app.services.data_source_service import DataSourceService

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify routing works"""
    return {"message": "Data sources endpoint is working!"}

@router.get("/", response_model=List[DataSourceResponse])
async def get_data_sources(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all available data sources for the current user
    """
    try:
        data_source_service = DataSourceService(db)
        data_sources = data_source_service.get_user_data_sources(current_user.id)
        return data_sources
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch data sources"
        )

@router.post("/test-connection", response_model=dict)
async def test_data_source_connection(
    request: DataSourceConnectionRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Test connection to a data source
    """
    try:
        data_source_service = DataSourceService(db)
        result = data_source_service.test_connection(request)
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to test connection"
        )

@router.get("/{data_source_id}/tables", response_model=List[dict])
async def get_data_source_tables(
    data_source_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all tables from a specific data source
    """
    try:
        data_source_service = DataSourceService(db)
        tables = data_source_service.get_tables(data_source_id, current_user.id)
        return tables
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tables"
        )

@router.get("/{data_source_id}/tables/{table_name}/columns", response_model=List[dict])
async def get_table_columns(
    data_source_id: str,
    table_name: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all columns from a specific table
    """
    try:
        data_source_service = DataSourceService(db)
        columns = data_source_service.get_table_columns(data_source_id, table_name, current_user.id)
        return columns
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch columns"
        )

@router.post("/", response_model=DataSourceResponse)
async def create_data_source(
    request: DataSourceConnectionRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Create a new data source
    """
    try:
        data_source_service = DataSourceService(db)
        data_source = data_source_service.create_data_source(request, current_user.id)
        return data_source
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create data source"
        )
