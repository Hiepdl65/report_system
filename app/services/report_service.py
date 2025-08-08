from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.services.query_builder import QueryBuilder
from app.services.export_service import ExportService
from app.models.datasource import DataSource
from app.models.report import Report
from app.models.template import ReportTemplate
from app.schemas.query import ReportRunRequest, ReportRunResponse
from app.core.database import get_db
import time
import uuid

class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.export_service = ExportService()
    
    async def run_report(self, request: ReportRunRequest, user_id: str) -> ReportRunResponse:
        """Execute report and return results"""
        start_time = time.time()
        
        try:
            # Get datasource configuration
            datasource = self.db.query(DataSource).filter(
                DataSource.id == request.query_config.datasource_id
            ).first()
            
            if not datasource:
                raise ValueError("Datasource not found")
            
            # Create query builder
            query_builder = QueryBuilder(datasource.connection_config)
            
            # Build and execute SQL
            sql = query_builder.build_sql(request.query_config)
            data, columns = query_builder.execute_query(sql)
            
            execution_time = time.time() - start_time
            
            # Save report if requested
            report_id = None
            if request.save_as_template:
                report_id = await self._save_report(request, user_id, sql)
            
            # Handle export
            export_file_url = None
            if request.export_format:
                export_file_url = await self._handle_export(
                    data, columns, request.export_format, user_id, report_id
                )
            
            return ReportRunResponse(
                success=True,
                data=data,
                columns=columns,
                row_count=len(data),
                execution_time=execution_time,
                export_file_url=export_file_url,
                message="Report executed successfully"
            )
            
        except Exception as e:
            return ReportRunResponse(
                success=False,
                message=f"Report execution failed: {str(e)}"
            )
    
    async def _save_report(self, request: ReportRunRequest, user_id: str, sql: str) -> str:
        """Save report to database"""
        report = Report(
            id=str(uuid.uuid4()),
            name=request.template_name or f"Report_{int(time.time())}",
            generated_by=user_id,
            status="completed"
        )
        
        self.db.add(report)
        self.db.commit()
        
        return report.id
    
    async def _handle_export(self, data: List[Dict], columns: List[str], 
                           export_format: str, user_id: str, report_id: str = None) -> str:
        """Handle data export"""
        if export_format == "excel":
            return await self.export_service.export_to_excel(data, columns, user_id)
        elif export_format == "csv":
            return await self.export_service.export_to_csv(data, columns, user_id)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")