from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import pymysql
from app.core.config import settings

# Install PyMySQL
pymysql.install_as_MySQLdb()

# Create engine with optimizations
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
    connect_args={
        "charset": "utf8mb4",
        "sql_mode": "TRADITIONAL",
        "init_command": "SET SESSION time_zone='+00:00'"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dynamic database connections for external data sources
class DatabaseManager:
    def __init__(self):
        self._connections = {}
    
    def get_connection(self, datasource_config: dict):
        """Get database connection for external data source"""
        conn_key = f"{datasource_config['type']}_{datasource_config['host']}_{datasource_config['database']}"
        
        if conn_key not in self._connections:
            db_type = datasource_config['type']
            
            if db_type == 'mysql':
                url = f"mysql+pymysql://{datasource_config['username']}:{datasource_config['password']}@{datasource_config['host']}:{datasource_config['port']}/{datasource_config['database']}"
            elif db_type == 'postgresql':
                url = f"postgresql://{datasource_config['username']}:{datasource_config['password']}@{datasource_config['host']}:{datasource_config['port']}/{datasource_config['database']}"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            
            engine = create_engine(url, pool_pre_ping=True)
            self._connections[conn_key] = engine
        
        return self._connections[conn_key]
    
    def test_connection(self, datasource_config: dict) -> bool:
        """Test database connection"""
        try:
            engine = self.get_connection(datasource_config)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

db_manager = DatabaseManager()