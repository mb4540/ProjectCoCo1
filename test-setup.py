#!/usr/bin/env python3
"""
Simple test script to verify the AI Dev Platform setup.
Run this after starting the services with: docker compose up
"""

import requests
import json
import time

def test_backend_health():
    """Test if the backend is running and healthy"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ Backend health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_backend_api():
    """Test the main API endpoint"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API test passed")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Backend API test failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend API test failed: {e}")
        return False

def test_frontend():
    """Test if the frontend is accessible"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessibility test passed")
            return True
        else:
            print(f"❌ Frontend test failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    print("🚀 Testing AI Dev Platform Setup...")
    print("-" * 50)
    
    # Wait a moment for services to be ready
    print("Waiting for services to start...")
    time.sleep(2)
    
    backend_health = test_backend_health()
    backend_api = test_backend_api()
    frontend = test_frontend()
    
    print("-" * 50)
    
    if all([backend_health, backend_api, frontend]):
        print("🎉 All tests passed! Your AI Dev Platform is ready to use.")
        print("\n📍 Access your application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the Docker containers:")
        print("   docker compose ps")
        print("   docker compose logs")

if __name__ == "__main__":
    main()