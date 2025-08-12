from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    tags = Column(JSON)  # Store as JSON array
    is_public = Column(Boolean, default=False)
    query_config = Column(JSON, nullable=False)  # Store query configuration as JSON
    display_config = Column(JSON)  # Store display configuration as JSON
    export_config = Column(JSON)  # Store export configuration as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(36), nullable=False)
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime)
