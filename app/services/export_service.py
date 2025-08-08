from typing import List, Dict, Any
import pandas as pd
import os
import uuid
from datetime import datetime
from app.core.config import settings
from app.utils.excel_utils import ExcelFormatter

class ExportService:
    def __init__(self):
        self.export_dir = settings.EXPORT_DIR
        os.makedirs(self.export_dir, exist_ok=True)
        self.excel_formatter = ExcelFormatter()
    
    async def export_to_excel(self, data: List[Dict[str, Any]], 
                            columns: List[str], user_id: str) -> str:
        """Export data to Excel file"""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}_{uuid.uuid4().hex[:8]}.xlsx"
            file_path = os.path.join(self.export_dir, filename)
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Apply formatting and create Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Report Data', index=False)
                
                # Apply formatting
                workbook = writer.book
                worksheet = writer.sheets['Report Data']
                self.excel_formatter.format_worksheet(worksheet, workbook, df)
            
            # Return download URL
            return f"/api/v1/export/download/{filename}"
            
        except Exception as e:
            raise ValueError(f"Excel export failed: {str(e)}")
    
    async def export_to_csv(self, data: List[Dict[str, Any]], 
                          columns: List[str], user_id: str) -> str:
        """Export data to CSV file"""
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}_{uuid.uuid4().hex[:8]}.csv"
            file_path = os.path.join(self.export_dir, filename)
            
            # Create DataFrame and save as CSV
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            
            # Return download URL
            return f"/api/v1/export/download/{filename}"
            
        except Exception as e:
            raise ValueError(f"CSV export failed: {str(e)}")
    
    def get_export_file(self, filename: str) -> str:
        """Get full path to export file"""
        file_path = os.path.join(self.export_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError("Export file not found")
        return file_path