#!/usr/bin/env python3
"""
Local Redis Agent Registration
Register the Redis agent using the local backend service
"""

import sys
import os
import asyncio
from datetime import datetime, timezone

# Add the backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi_app.services.agent_service import agent_service
from fastapi_app.models.agent import AgentRegistration

async def register_redis_agent():
    """Register the Redis agent with the platform"""
    
    # Agent registration data
    agent_data = AgentRegistration(
        name="Redis Caching Layer Agent",
        description="High-performance caching service for Google Cloud Run with in-memory fallback",
        purpose="Provide fast, reliable caching operations with TTL support and comprehensive monitoring",
        version="2.0.0",
        repository_url="https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/redis-caching-agent",
        deployment_url="https://redis-caching-agent-fdqqqinvyq-uc.a.run.app",
        health_check_url="https://redis-caching-agent-fdqqqinvyq-uc.a.run.app/health",
        prd_id=None,
        devin_task_id=None,
        capabilities=[
            "cache_set",
            "cache_get", 
            "cache_delete",
            "cache_invalidate",
            "cache_stats",
            "health_monitoring",
            "metrics_collection"
        ],
        configuration={
            "platform": "google-cloud-run",
            "region": "us-central1",
            "cache_type": "in-memory-fallback",
            "redis_host": "10.1.93.195",
            "redis_port": 6379,
            "auto_scaling": "1-10_instances",
            "memory": "2GB",
            "cpu": "2_vCPU"
        }
    )
    
    print("🔄 Registering Redis Caching Agent...")
    print(f"Agent URL: {agent_data.deployment_url}")
    
    try:
        # Create the agent
        agent_response = await agent_service.create_agent(agent_data)
        
        print("✅ Agent registered successfully!")
        print(f"   Agent ID: {agent_response.id}")
        print(f"   Name: {agent_response.name}")
        print(f"   Status: {agent_response.status}")
        print(f"   Deployment URL: {agent_response.deployment_url}")
        print(f"   Created at: {agent_response.created_at}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    success = await register_redis_agent()
    
    if success:
        print("\n🎉 Redis Agent registration completed successfully!")
        print("\nNext steps:")
        print("1. Verify the agent appears in the AI Agent Factory dashboard")
        print("2. Test all functionality through the platform")
        print("3. Monitor performance and scaling")
    else:
        print("\n❌ Redis Agent registration failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
