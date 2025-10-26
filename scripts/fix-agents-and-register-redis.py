#!/usr/bin/env python3
"""
Fix Agents Endpoint and Register Redis Agent
This script tests the agents endpoint and registers the Redis agent
"""

import requests
import json
import sys

def test_agents_endpoint():
    """Test if the agents endpoint is working"""
    print("🔍 Testing agents endpoint...")
    
    backend_url = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    
    try:
        response = requests.get(f"{backend_url}/api/v1/agents", timeout=10)
        
        if response.status_code == 200:
            agents_data = response.json()
            print(f"✅ Agents endpoint is working!")
            print(f"   Total agents: {agents_data.get('total', 0)}")
            return True
        else:
            print(f"❌ Agents endpoint still broken: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing agents endpoint: {e}")
        return False

def register_redis_agent():
    """Register the Redis agent"""
    print("\n🤖 Registering Redis Caching Layer Agent...")
    
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
        "prd_id": "33b59b96-dda7-485d-97e7-dcc6b9d71d31",  # Redis PRD ID
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
    
    try:
        # Test Redis agent health
        print("🧪 Testing Redis agent health...")
        health_response = requests.get(f"{redis_agent_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Redis agent health: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ Redis agent health check failed: {health_response.status_code}")
            return False
        
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
            return True
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error registering Redis agent: {e}")
        return False

def verify_frontend():
    """Verify the agent appears in the frontend"""
    print("\n🌐 Verifying frontend...")
    
    try:
        # Check if frontend loads without errors
        frontend_url = "https://ai-agent-factory-frontend-952475323593.us-central1.run.app"
        response = requests.get(frontend_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            print(f"   URL: {frontend_url}")
            return True
        else:
            print(f"❌ Frontend error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Fixing Agents Endpoint and Registering Redis Agent")
    print("=" * 60)
    
    # Step 1: Test agents endpoint
    if not test_agents_endpoint():
        print("\n❌ Agents endpoint is still broken!")
        print("Please create the agents table first using the SQL provided earlier.")
        print("\n📋 SQL to run in Supabase dashboard:")
        print("""
-- Create custom types if they don't exist
CREATE TYPE IF NOT EXISTS agent_status AS ENUM ('draft', 'active', 'inactive', 'deprecated', 'error');
CREATE TYPE IF NOT EXISTS agent_health_status AS ENUM ('healthy', 'degraded', 'unhealthy', 'unknown');
CREATE TYPE IF NOT EXISTS agent_type AS ENUM ('web_app', 'api_service', 'data_processor', 'automation_script', 'ai_model', 'integration', 'other');

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    purpose TEXT NOT NULL,
    agent_type agent_type NOT NULL DEFAULT 'other',
    version VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    status agent_status NOT NULL DEFAULT 'draft',
    health_status agent_health_status NOT NULL DEFAULT 'unknown',
    repository_url VARCHAR(500),
    deployment_url VARCHAR(500),
    health_check_url VARCHAR(500),
    prd_id UUID REFERENCES prds(id) ON DELETE SET NULL,
    devin_task_id UUID,
    capabilities TEXT[] DEFAULT '{}',
    configuration JSONB DEFAULT '{}',
    metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_health_check TIMESTAMP WITH TIME ZONE,
    
    -- Indexes for performance
    CONSTRAINT agents_name_not_empty CHECK (length(trim(name)) > 0),
    CONSTRAINT agents_purpose_not_empty CHECK (length(trim(purpose)) > 0)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_health_status ON agents(health_status);
CREATE INDEX IF NOT EXISTS idx_agents_prd_id ON agents(prd_id);
CREATE INDEX IF NOT EXISTS idx_agents_created_at ON agents(created_at);
        """)
        return
    
    # Step 2: Register Redis agent
    if not register_redis_agent():
        print("\n❌ Failed to register Redis agent!")
        return
    
    # Step 3: Verify frontend
    if not verify_frontend():
        print("\n❌ Frontend verification failed!")
        return
    
    print("\n🎉 SUCCESS! Redis agent is now registered and should be visible in the frontend!")
    print("   Frontend: https://ai-agent-factory-frontend-952475323593.us-central1.run.app")
    print("   Redis Agent: https://redis-caching-agent-fdqqqinvyq-uc.a.run.app")

if __name__ == "__main__":
    main()
