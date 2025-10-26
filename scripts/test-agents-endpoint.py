#!/usr/bin/env python3
"""
Test Agents Endpoint
This script tests the agents endpoint and provides detailed error information
"""

import requests
import json

def test_agents_endpoint():
    """Test the agents endpoint with detailed error reporting"""
    
    print("🧪 Testing Agents Endpoint")
    print("=" * 30)
    
    backend_url = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    
    # Test 1: Basic agents endpoint
    print("1️⃣ Testing GET /api/v1/agents...")
    try:
        response = requests.get(f"{backend_url}/api/v1/agents", timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('total', 0)} agents found")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Test with different parameters
    print("\n2️⃣ Testing with parameters...")
    try:
        response = requests.get(f"{backend_url}/api/v1/agents?limit=1", timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 3: Test other endpoints for comparison
    print("\n3️⃣ Testing other endpoints for comparison...")
    
    # Test health endpoint
    try:
        health_response = requests.get(f"{backend_url}/api/v1/health", timeout=10)
        print(f"   Health endpoint: {health_response.status_code}")
    except Exception as e:
        print(f"   Health endpoint error: {e}")
    
    # Test PRDs endpoint
    try:
        prds_response = requests.get(f"{backend_url}/api/v1/prds", timeout=10)
        print(f"   PRDs endpoint: {prds_response.status_code}")
        if prds_response.status_code == 200:
            prds_data = prds_response.json()
            print(f"   PRDs count: {prds_data.get('total', 0)}")
    except Exception as e:
        print(f"   PRDs endpoint error: {e}")
    
    # Test 4: Try to create a test agent
    print("\n4️⃣ Testing agent creation...")
    try:
        test_agent = {
            "name": "Test Agent",
            "description": "Test agent for debugging",
            "purpose": "Testing the agents endpoint",
            "version": "1.0.0",
            "repository_url": "https://example.com",
            "deployment_url": "https://example.com",
            "health_check_url": "https://example.com/health",
            "capabilities": ["test"],
            "configuration": {}
        }
        
        response = requests.post(f"{backend_url}/api/v1/agents", json=test_agent, timeout=10)
        print(f"   POST Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"   POST Response: {response.text}")
        else:
            print(f"   ✅ Agent created successfully")
            # Clean up the test agent
            agent_data = response.json()
            agent_id = agent_data.get('id')
            if agent_id:
                delete_response = requests.delete(f"{backend_url}/api/v1/agents/{agent_id}", timeout=10)
                print(f"   Cleanup: {delete_response.status_code}")
            
    except Exception as e:
        print(f"   POST Exception: {e}")
    
    return False

def main():
    """Main function"""
    print("🚀 Agents Endpoint Diagnostic Tool")
    print("=" * 40)
    
    success = test_agents_endpoint()
    
    print(f"\n📋 Summary:")
    if success:
        print("✅ Agents endpoint is working correctly")
    else:
        print("❌ Agents endpoint has issues")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Check backend service logs")
        print("2. Verify database connection in backend")
        print("3. Check for code errors in agent service")
        print("4. Restart the backend service if needed")

if __name__ == "__main__":
    main()
