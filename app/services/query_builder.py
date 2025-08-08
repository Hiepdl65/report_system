from typing import List, Dict, Any, Tuple
from sqlalchemy import text, MetaData, Table
from sqlalchemy.engine import Engine
from app.schemas.query import QueryConfiguration, QueryTable, QueryJoin, QueryField, QueryFilter, FilterOperator
from app.core.database import db_manager
from app.utils.sql_utils import SQLValidator, SQLSanitizer
import re

class QueryBuilder:
    def __init__(self, datasource_config: dict):
        self.datasource_config = datasource_config
        self.engine = db_manager.get_connection(datasource_config)
        self.validator = SQLValidator()
        self.sanitizer = SQLSanitizer()
    
    def build_sql(self, config: QueryConfiguration) -> str:
        """Convert query configuration to SQL"""
        try:
            # Validate configuration
            self._validate_configuration(config)
            
            # Build SQL parts
            select_clause = self._build_select_clause(config.fields)
            from_clause = self._build_from_clause(config.tables, config.joins)
            where_clause = self._build_where_clause(config.filters)
            group_by_clause = self._build_group_by_clause(config.group_by)
            order_by_clause = self._build_order_by_clause(config.order_by)
            limit_clause = self._build_limit_clause(config.limit)
            
            # Combine SQL parts
            sql_parts = [
                f"SELECT {select_clause}",
                f"FROM {from_clause}"
            ]
            
            if where_clause:
                sql_parts.append(f"WHERE {where_clause}")
            
            if group_by_clause:
                sql_parts.append(f"GROUP BY {group_by_clause}")
            
            if order_by_clause:
                sql_parts.append(f"ORDER BY {order_by_clause}")
            
            if limit_clause:
                sql_parts.append(f"LIMIT {limit_clause}")
            
            sql = " ".join(sql_parts)
            
            # Final validation
            self.validator.validate_sql(sql)
            
            return sql
            
        except Exception as e:
            raise ValueError(f"Failed to build SQL: {str(e)}")
    
    def _validate_configuration(self, config: QueryConfiguration):
        """Validate query configuration"""
        # Check table existence
        for table in config.tables:
            if not self._table_exists(table.name, table.schema):
                raise ValueError(f"Table {table.name} does not exist")
        
        # Check column existence
        for field in config.fields:
            table = next((t for t in config.tables if t.alias == field.table_alias), None)
            if not table:
                raise ValueError(f"Table alias {field.table_alias} not found")
            
            if not self._column_exists(table.name, field.column, table.schema):
                raise ValueError(f"Column {field.column} does not exist in table {table.name}")
    
    def _build_select_clause(self, fields: List[QueryField]) -> str:
        """Build SELECT clause"""
        select_parts = []
        
        for field in fields:
            if not field.visible:
                continue
            
            column_ref = f"{field.table_alias}.{self.sanitizer.sanitize_identifier(field.column)}"
            
            if field.aggregation:
                if field.aggregation == "GROUP_CONCAT":
                    column_expr = f"GROUP_CONCAT({column_ref})"
                else:
                    column_expr = f"{field.aggregation}({column_ref})"
            else:
                column_expr = column_ref
            
            if field.alias:
                column_expr += f" AS {self.sanitizer.sanitize_identifier(field.alias)}"
            
            select_parts.append(column_expr)
        
        return ", ".join(select_parts) if select_parts else "*"
    
    def _build_from_clause(self, tables: List[QueryTable], joins: List[QueryJoin]) -> str:
        """Build FROM clause with JOINs"""
        if not tables:
            raise ValueError("No tables specified")
        
        # Start with first table
        main_table = tables[0]
        from_clause = f"{self.sanitizer.sanitize_identifier(main_table.name)} AS {main_table.alias}"
        
        # Add joins
        for join in joins:
            # Find the right table
            right_table = next((t for t in tables if t.alias == join.right_table), None)
            if not right_table:
                raise ValueError(f"Join table {join.right_table} not found")
            
            join_clause = f" {join.join_type} JOIN {self.sanitizer.sanitize_identifier(right_table.name)} AS {right_table.alias}"
            join_clause += f" ON {self._sanitize_join_condition(join.condition)}"
            from_clause += join_clause
        
        return from_clause
    
    def _build_where_clause(self, filters: List[QueryFilter]) -> str:
        """Build WHERE clause"""
        if not filters:
            return ""
        
        where_conditions = []
        
        for filter_item in filters:
            condition = self._build_filter_condition(filter_item)
            where_conditions.append(condition)
        
        return " AND ".join(where_conditions)
    
    def _build_filter_condition(self, filter_item: QueryFilter) -> str:
        """Build individual filter condition"""
        column_ref = f"{filter_item.table_alias}.{self.sanitizer.sanitize_identifier(filter_item.column)}"
        operator = filter_item.operator
        value = filter_item.value
        
        if operator == FilterOperator.IS_NULL:
            return f"{column_ref} IS NULL"
        elif operator == FilterOperator.IS_NOT_NULL:
            return f"{column_ref} IS NOT NULL"
        elif operator in [FilterOperator.IN, FilterOperator.NOT_IN]:
            if isinstance(value, list):
                value_list = ", ".join([self._format_value(v, filter_item.data_type) for v in value])
                return f"{column_ref} {operator} ({value_list})"
            else:
                raise ValueError(f"IN/NOT IN operator requires list value")
        elif operator == FilterOperator.BETWEEN:
            if isinstance(value, list) and len(value) == 2:
                val1 = self._format_value(value[0], filter_item.data_type)
                val2 = self._format_value(value[1], filter_item.data_type)
                return f"{column_ref} BETWEEN {val1} AND {val2}"
            else:
                raise ValueError("BETWEEN operator requires array of 2 values")
        else:
            formatted_value = self._format_value(value, filter_item.data_type)
            return f"{column_ref} {operator} {formatted_value}"
    
    def _format_value(self, value: Any, data_type: str) -> str:
        """Format value based on data type"""
        if value is None:
            return "NULL"
        
        if data_type == "string":
            # Escape single quotes
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"
        elif data_type == "number":
            return str(value)
        elif data_type == "date":
            return f"'{value}'"
        elif data_type == "boolean":
            return "1" if value else "0"
        else:
            return f"'{value}'"
    
    def _build_group_by_clause(self, group_by: List[str]) -> str:
        """Build GROUP BY clause"""
        if not group_by:
            return ""
        
        sanitized_fields = [self.sanitizer.sanitize_identifier(field) for field in group_by]
        return ", ".join(sanitized_fields)
    
    def _build_order_by_clause(self, order_by: List) -> str:
        """Build ORDER BY clause"""
        if not order_by:
            return ""
        
        order_parts = []
        for sort_item in order_by:
            field = self.sanitizer.sanitize_identifier(sort_item.field)
            direction = sort_item.direction
            order_parts.append(f"{field} {direction}")
        
        return ", ".join(order_parts)
    
    def _build_limit_clause(self, limit: int) -> str:
        """Build LIMIT clause"""
        if limit is None:
            return ""
        
        if limit <= 0 or limit > 1000000:
            raise ValueError("Invalid limit value")
        
        return str(limit)
    
    def _sanitize_join_condition(self, condition: str) -> str:
        """Sanitize JOIN condition"""
        # Basic sanitization - remove dangerous keywords
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'UNION']
        condition_upper = condition.upper()
        
        for keyword in dangerous_keywords:
            if keyword in condition_upper:
                raise ValueError(f"Dangerous keyword '{keyword}' not allowed in JOIN condition")
        
        return condition
    
    def _table_exists(self, table_name: str, schema: str = None) -> bool:
        """Check if table exists"""
        try:
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=self.engine, schema=schema)
            return True
        except Exception:
            return False
    
    def _column_exists(self, table_name: str, column_name: str, schema: str = None) -> bool:
        """Check if column exists in table"""
        try:
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=self.engine, schema=schema)
            return column_name in [col.name for col in table.columns]
        except Exception:
            return False
    
    def get_table_schema(self, table_name: str, schema: str = None) -> Dict[str, Any]:
        """Get table schema information"""
        try:
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=self.engine, schema=schema)
            
            columns = []
            for col in table.columns:
                columns.append({
                    "name": col.name,
                    "type": str(col.type),
                    "nullable": col.nullable,
                    "primary_key": col.primary_key,
                    "foreign_key": len(col.foreign_keys) > 0
                })
            
            return {
                "table_name": table_name,
                "columns": columns
            }
        except Exception as e:
            raise ValueError(f"Failed to get table schema: {str(e)}")

    def execute_query(self, sql: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                columns = list(result.keys())
                rows = [dict(row) for row in result.fetchall()]
                return rows, columns
        except Exception as e:
            raise ValueError(f"Query execution failed: {str(e)}")