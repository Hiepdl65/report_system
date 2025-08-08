from typing import List, Optional, Any, Dict
from pydantic import BaseModel, validator
from enum import Enum

class JoinType(str, Enum):
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FULL = "FULL"

class AggregationType(str, Enum):
    COUNT = "COUNT"
    SUM = "SUM"
    AVG = "AVG"
    MIN = "MIN"
    MAX = "MAX"
    GROUP_CONCAT = "GROUP_CONCAT"

class FilterOperator(str, Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    GREATER_EQUALS = ">="
    LESS_THAN = "<"
    LESS_EQUALS = "<="
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"
    IN = "IN"
    NOT_IN = "NOT IN"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"
    BETWEEN = "BETWEEN"

class SortDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class QueryTable(BaseModel):
    id: str
    name: str
    alias: str
    schema: Optional[str] = None

class QueryJoin(BaseModel):
    left_table: str
    right_table: str
    join_type: JoinType = JoinType.INNER
    condition: str  # e.g., "u.id = o.user_id"

class QueryField(BaseModel):
    table_alias: str
    column: str
    alias: Optional[str] = None
    aggregation: Optional[AggregationType] = None
    visible: bool = True

class QueryFilter(BaseModel):
    table_alias: str
    column: str
    operator: FilterOperator
    value: Any
    data_type: str = "string"  # string, number, date, boolean

class QuerySort(BaseModel):
    field: str  # table_alias.column or alias
    direction: SortDirection = SortDirection.ASC

class QueryConfiguration(BaseModel):
    datasource_id: str
    tables: List[QueryTable]
    joins: List[QueryJoin] = []
    fields: List[QueryField]
    filters: List[QueryFilter] = []
    group_by: List[str] = []  # field references
    order_by: List[QuerySort] = []
    limit: Optional[int] = None
    
    @validator('tables')
    def validate_tables(cls, v):
        if len(v) == 0:
            raise ValueError("At least one table is required")
        if len(v) > 10:  # Limit complexity
            raise ValueError("Maximum 10 tables allowed")
        return v
    
    @validator('joins')
    def validate_joins(cls, v, values):
        if 'tables' in values:
            table_aliases = {t.alias for t in values['tables']}
            for join in v:
                if join.left_table not in table_aliases:
                    raise ValueError(f"Left table alias '{join.left_table}' not found")
                if join.right_table not in table_aliases:
                    raise ValueError(f"Right table alias '{join.right_table}' not found")
        return v

class ReportRunRequest(BaseModel):
    query_config: QueryConfiguration
    export_format: Optional[str] = None  # "excel", "csv", "json"
    template_name: Optional[str] = None
    save_as_template: bool = False

class ReportRunResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    row_count: int = 0
    execution_time: float = 0.0
    export_file_url: Optional[str] = None
    message: Optional[str] = None