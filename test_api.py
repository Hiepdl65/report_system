#!/usr/bin/env python3
"""
Simple test script to verify API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Health endpoint error: {e}")

def test_data_sources():
    """Test data sources endpoints"""
    try:
        # Test simple endpoint
        response = requests.get(f"{BASE_URL}/api/v1/data-sources/test")
        print(f"Data sources test endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
            
        # Test main endpoint
        response = requests.get(f"{BASE_URL}/api/v1/data-sources/")
        print(f"Data sources main endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Data sources endpoints error: {e}")

def test_templates():
    """Test templates endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/templates/")
        print(f"Templates endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Templates endpoint error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 50)
    
    test_health()
    print("-" * 30)
    
    test_data_sources()
    print("-" * 30)
    
    test_templates()
    print("=" * 50)
    print("Testing complete!")
