#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database models for ERP Query Application
"""
import pyodbc
import threading
import hashlib
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

class DatabaseConnection:
    """Database connection wrapper with connection pooling"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
        self.last_used = time.time()
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.connection.timeout = 30
        except Exception as e:
            raise Exception(f"Failed to connect to database: {str(e)}")
    
    def execute_query(self, query: str, params: Optional[List] = None) -> Dict[str, Any]:
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description] if cursor.description else []
            
            # Fetch results
            rows = cursor.fetchall()
            results = []
            
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    # Handle datetime objects
                    if isinstance(value, datetime):
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = value
                results.append(row_dict)
            
            cursor.close()
            self.last_used = time.time()
            
            return {
                'success': True,
                'data': results,
                'columns': columns,
                'row_count': len(results)
            }
            
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    def execute_batch(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple operations in a batch"""
        try:
            cursor = self.connection.cursor()
            results = []
            
            for operation in operations:
                query = operation.get('query')
                params = operation.get('params', [])
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results.append({
                    'query': query,
                    'affected_rows': cursor.rowcount
                })
            
            self.connection.commit()
            cursor.close()
            self.last_used = time.time()
            
            return {
                'success': True,
                'results': results,
                'total_operations': len(operations)
            }
            
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Batch execution failed: {str(e)}")
    
    def is_healthy(self) -> bool:
        """Check if connection is healthy"""
        try:
            if not self.connection:
                return False
            
            # Test connection with a simple query
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
            
        except Exception:
            return False
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            finally:
                self.connection = None

class ConnectionPool:
    """Connection pool manager"""
    
    def __init__(self):
        self.pool: Dict[str, DatabaseConnection] = {}
        self.pool_lock = threading.Lock()
        self.max_pool_size = 10
        self.connection_timeout = 3600  # 1 hour
    
    def get_connection(self, connection_string: str) -> DatabaseConnection:
        """Get a connection from pool or create new one"""
        connection_key = self._get_connection_key(connection_string)
        
        with self.pool_lock:
            # Check if connection exists and is healthy
            if connection_key in self.pool:
                connection = self.pool[connection_key]
                if connection.is_healthy():
                    return connection
                else:
                    # Remove unhealthy connection
                    connection.close()
                    del self.pool[connection_key]
            
            # Create new connection if pool not full
            if len(self.pool) < self.max_pool_size:
                connection = DatabaseConnection(connection_string)
                self.pool[connection_key] = connection
                return connection
            else:
                # Reuse oldest connection
                oldest_key = min(self.pool.keys(), 
                               key=lambda k: self.pool[k].last_used)
                old_connection = self.pool[oldest_key]
                old_connection.close()
                
                connection = DatabaseConnection(connection_string)
                self.pool[connection_key] = connection
                return connection
    
    def _get_connection_key(self, connection_string: str) -> str:
        """Generate unique key for connection string"""
        return hashlib.md5(connection_string.encode()).hexdigest()[:8]
    
    def cleanup_stale_connections(self):
        """Remove stale connections from pool"""
        current_time = time.time()
        
        with self.pool_lock:
            stale_keys = []
            for key, connection in self.pool.items():
                if current_time - connection.last_used > self.connection_timeout:
                    stale_keys.append(key)
            
            for key in stale_keys:
                connection = self.pool[key]
                connection.close()
                del self.pool[key]
    
    def close_all(self):
        """Close all connections in pool"""
        with self.pool_lock:
            for connection in self.pool.values():
                connection.close()
            self.pool.clear()

# Global connection pool instance
connection_pool = ConnectionPool() 