#!/usr/bin/env python3
"""
Manual Redis Agent Registration
Simple script to register the Redis agent with the AI Agent Factory platform
"""

import requests
import json
import sys

def register_redis_agent():
    """Register the Redis agent with the platform"""
    
    # Configuration
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
        "prd_id": None,
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
    
    print("🔄 Registering Redis Caching Agent...")
    print(f"Backend URL: {backend_url}")
    print(f"Agent URL: {redis_agent_url}")
    
    try:
        # Test the agent first
        print("\n🧪 Testing agent endpoints...")
        
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
            print("✅ Cache set operation working")
        else:
            print(f"❌ Cache set failed: {cache_response.status_code}")
            return False
        
        # Register the agent
        print("\n📝 Registering agent with platform...")
        register_response = requests.post(
            f"{backend_url}/api/v1/agents",
            json=agent_data,
            timeout=10
        )
        
        if register_response.status_code in [200, 201]:
            agent_info = register_response.json()
            print("✅ Agent registered successfully!")
            print(f"   Agent ID: {agent_info.get('id', 'N/A')}")
            print(f"   Name: {agent_info.get('name', 'N/A')}")
            print(f"   Status: {agent_info.get('status', 'N/A')}")
            print(f"   Deployment URL: {agent_info.get('deployment_url', 'N/A')}")
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
    if len(sys.argv) != 1:
        print("Usage: python manual-redis-agent-registration.py")
        sys.exit(1)
    
    success = register_redis_agent()
    
    if success:
        print("\n🎉 Redis Agent migration completed successfully!")
        print("\nNext steps:")
        print("1. Verify the agent appears in the AI Agent Factory dashboard")
        print("2. Test all functionality through the platform")
        print("3. Monitor performance and scaling")
        print("4. Consider decommissioning the Fly.io deployment")
    else:
        print("\n❌ Redis Agent migration failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
