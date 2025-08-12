from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    host = Column(String(255))
    port = Column(Integer)
    database = Column(String(255))
    username = Column(String(255))
    password = Column(Text)  # Encrypted
    connection_string = Column(Text)
    file_path = Column(String(500))
    api_url = Column(String(500))
    api_key = Column(Text)  # Encrypted
    status = Column(String(50), default="disconnected")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(36), nullable=False)
