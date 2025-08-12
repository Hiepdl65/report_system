from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
import jwt
from datetime import datetime

# Mock dependencies for now - replace with actual implementations
security = HTTPBearer(auto_error=False)

# Mock user model
class MockUser:
    def __init__(self, user_id: str = "mock_user_123"):
        self.id = user_id
        self.email = "mock@example.com"
        self.is_active = True

# Mock database session
class MockDatabaseSession:
    def __init__(self):
        pass
    
    def close(self):
        pass

def get_db() -> Generator[Session, None, None]:
    """Get database session - mock implementation"""
    try:
        db = MockDatabaseSession()
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> MockUser:
    """Get current user - mock implementation"""
    # For development, always return a mock user
    # In production, validate JWT token here
    if not credentials:
        # If no token provided, still return mock user for development
        return MockUser()
    
    try:
        # In production, decode and validate JWT token
        # payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # user_id = payload.get("sub")
        # if user_id is None:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        
        # For now, return mock user
        return MockUser()
        
    except jwt.PyJWTError:
        # In production, raise error for invalid token
        # raise HTTPException(status_code=401, detail="Invalid token")
        
        # For development, return mock user
        return MockUser()

def get_current_active_user(current_user: MockUser = Depends(get_current_user)) -> MockUser:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
