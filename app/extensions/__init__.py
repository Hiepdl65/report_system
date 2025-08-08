#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extensions initialization for ERP Query Application
"""
from flask_cors import CORS

def init_extensions(app):
    """Initialize all Flask extensions"""
    # Initialize CORS
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', []), 
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Set JSON configuration
    app.config['JSON_SORT_KEYS'] = app.config.get('JSON_SORT_KEYS', False) 