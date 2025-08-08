from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.query import ReportRunRequest, ReportRunResponse
from app.services.report_service import ReportService

router = APIRouter()

@router.post("/run", response_model=ReportRunResponse)
async def run_report(
    request: ReportRunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Execute a report based on query configuration
    
    This endpoint accepts a JSON payload containing:
    - Query configuration (tables, joins, fields, filters, etc.)
    - Export format (optional)
    - Template saving options (optional)
    
    Returns:
    - Query results as JSON
    - Export file URL if export format specified
    - Execution metadata (timing, row count, etc.)
    """
    try:
        report_service = ReportService(db)
        result = await report_service.run_report(request, current_user.id)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred"
        )

@router.post("/preview", response_model=ReportRunResponse)
async def preview_report(
    request: ReportRunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Preview report with limited results (first 100 rows)
    """
    try:
        # Limit preview to 100 rows
        request.query_config.limit = min(request.query_config.limit or 100, 100)
        
        report_service = ReportService(db)
        result = await report_service.run_report(request, current_user.id)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/history")
async def get_report_history(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user's report execution history
    """
    # Implementation for getting report history
    pass