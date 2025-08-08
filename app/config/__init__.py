#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for ERP Query Application
"""
import os

class Config:
    """Base configuration class"""
    
    # Server settings
    PORT = int(os.environ.get('PORT', 3000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = '0.0.0.0'
    
    # CORS settings
    CORS_ORIGINS = [
        'http://localhost:3000', 'http://127.0.0.1:3000',
        'http://localhost:3002', 'http://127.0.0.1:3002',  # Vite default port
        'http://localhost:5500', 'http://127.0.0.1:5500'
    ]

    # Database settings
    POOL_SIZE = 10
    CONNECTION_TIMEOUT = 3600  # 1 hour
    QUERY_TIMEOUT = 30        # 30 seconds
    MAX_BATCH_SIZE = 100
    MAX_QUERY_LIMIT = 1000
    
    # Security settings
    MAX_IDENTIFIER_LENGTH = 64
    DANGEROUS_KEYWORDS = ['drop', 'delete', 'exec', 'truncate', 'alter']
    
    # Logging settings
    LOG_LEVEL = 'INFO' if not DEBUG else 'DEBUG'
    LOG_FILE = 'erp_backend.log'
    
    # JSON settings
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
} 