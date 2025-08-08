from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Report System API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "report_user"
    MYSQL_PASSWORD: str = "secure_password"
    MYSQL_DB: str = "report_system"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Export settings
    EXPORT_DIR: str = "./exports"
    MAX_EXPORT_ROWS: int = 1000000
    EXPORT_TIMEOUT: int = 300  # seconds
    
    # Query limits
    MAX_QUERY_TIMEOUT: int = 60  # seconds
    MAX_JOINS: int = 10
    MAX_WHERE_CONDITIONS: int = 50
    
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()