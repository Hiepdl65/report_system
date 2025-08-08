import re
from typing import List

class SQLValidator:
    def __init__(self):
        self.dangerous_keywords = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 
            'TRUNCATE', 'EXEC', 'EXECUTE', 'UNION', 'SCRIPT'
        ]
        self.allowed_functions = [
            'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'GROUP_CONCAT',
            'UPPER', 'LOWER', 'SUBSTRING', 'LENGTH', 'TRIM'
        ]
    
    def validate_sql(self, sql: str) -> bool:
        """Validate SQL for security"""
        sql_upper = sql.upper()
        
        # Check for dangerous keywords
        for keyword in self.dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(f"Dangerous SQL keyword not allowed: {keyword}")
        
        # Check for SQL injection patterns
        injection_patterns = [
            r"(\s|^)(OR|AND)\s+\d+\s*=\s*\d+",  # OR 1=1, AND 1=1
            r"(\s|^)(OR|AND)\s+\w+\s*=\s*\w+",  # OR admin=admin
            r"--",  # SQL comments
            r"/\*.*\*/",  # Block comments
            r";\s*(DROP|DELETE|UPDATE|INSERT)",  # Statement injection
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, sql_upper):
                raise ValueError("Potential SQL injection detected")
        
        return True

class SQLSanitizer:
    def sanitize_identifier(self, identifier: str) -> str:
        """Sanitize SQL identifiers (table/column names)"""
        # Remove special characters except underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '', identifier)
        
        # Ensure it starts with letter or underscore
        if not re.match(r'^[a-zA-Z_]', sanitized):
            raise ValueError(f"Invalid identifier: {identifier}")
        
        return sanitized
    
    def sanitize_string_value(self, value: str) -> str:
        """Sanitize string values"""
        # Escape single quotes
        return value.replace("'", "''")