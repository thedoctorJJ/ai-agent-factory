#!/usr/bin/env python3
"""
Register Redis Agent in Production
This script registers the Redis agent once the agents table is created
"""

import requests
import json
import sys

def register_redis_agent():
    """Register the Redis agent with the production platform"""
    
    print("🤖 Registering Redis Caching Layer Agent")
    print("=" * 50)
    
    # Production backend URL
    backend_url = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    redis_agent_url = "https://redis-caching-agent-fdqqqinvyq-uc.a.run.app"
    
    # Agent registration data
    agent_data = {
        "name": "Redis Caching Layer Agent",
        "description": "High-performance caching service for Google Cloud Run with in-memory fallback",
        "purpose": "Provide fast, reliable caching operations with TTL support and comprehensive monitoring",
        "version": "2.0.0",
        "repository_url": "https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/redis-caching-agent",
        "deployment_url": redis_agent_url,
        "health_check_url": f"{redis_agent_url}/health",
        "prd_id": "6e495754-d340-476e-a2a4-cb16e9abb5d1",  # Redis PRD ID
        "devin_task_id": None,
        "capabilities": [
            "cache_set",
            "cache_get", 
            "cache_delete",
            "cache_invalidate",
            "cache_stats",
            "health_monitoring",
            "metrics_collection"
        ],
        "configuration": {
            "platform": "google-cloud-run",
            "region": "us-central1",
            "cache_type": "in-memory-fallback",
            "redis_host": "10.1.93.195",
            "redis_port": 6379,
            "auto_scaling": "1-10_instances",
            "memory": "2GB",
            "cpu": "2_vCPU"
        }
    }
    
    print(f"🔧 Backend URL: {backend_url}")
    print(f"🔧 Agent URL: {redis_agent_url}")
    print(f"🔧 PRD ID: {agent_data['prd_id']}")
    print()
    
    try:
        # Test the agent first
        print("🧪 Testing Redis agent endpoints...")
        
        # Test health endpoint
        health_response = requests.get(f"{redis_agent_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health check: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
        
        # Test cache operations
        cache_response = requests.post(
            f"{redis_agent_url}/cache",
            json={"key": "test-registration", "value": "test-value", "ttl": 60},
            timeout=10
        )
        if cache_response.status_code == 200:
            print("✅ Cache operations working")
        else:
            print(f"❌ Cache operations failed: {cache_response.status_code}")
            return False
        
        print()
        
        # Test if agents endpoint is working
        print("🔍 Testing agents endpoint...")
        agents_test_response = requests.get(f"{backend_url}/api/v1/agents", timeout=10)
        if agents_test_response.status_code == 200:
            print("✅ Agents endpoint is working")
        else:
            print(f"❌ Agents endpoint still broken: {agents_test_response.status_code}")
            print("Please create the agents table first using the SQL provided earlier.")
            return False
        
        print()
        
        # Register the agent
        print("📝 Registering Redis agent...")
        register_response = requests.post(
            f"{backend_url}/api/v1/agents",
            json=agent_data,
            timeout=10
        )
        
        if register_response.status_code in [200, 201]:
            agent_info = register_response.json()
            print("✅ Redis agent registered successfully!")
            print(f"   Agent ID: {agent_info.get('id', 'N/A')}")
            print(f"   Name: {agent_info.get('name', 'N/A')}")
            print(f"   Status: {agent_info.get('status', 'N/A')}")
            print(f"   Deployment URL: {agent_info.get('deployment_url', 'N/A')}")
            print()
            print("🎉 Redis agent should now be visible in the frontend!")
            print(f"   Frontend: https://ai-agent-factory-frontend-952475323593.us-central1.run.app")
            return True
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting Redis Agent Registration")
    print("=" * 40)
    
    success = register_redis_agent()
    
    if success:
        print("\n✅ Redis agent registration completed successfully!")
        print("The agent should now appear in the AI Agent Factory dashboard.")
    else:
        print("\n❌ Redis agent registration failed!")
        print("Please ensure the agents table has been created first.")

if __name__ == "__main__":
    main()
