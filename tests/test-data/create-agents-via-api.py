#!/usr/bin/env python3
"""
Create test agents via API calls instead of direct service calls.
This ensures the agents are properly stored and accessible via the API.
"""

import requests
import json
import uuid
from datetime import datetime, timezone

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test agents data
TEST_AGENTS = [
    # Multiple agents for the same PRD (Database Integration)
    {
        "name": "TEST_Database_Connection_Agent",
        "description": "Handles database connection pooling and optimization",
        "purpose": "Database connection management and optimization",
        "prd_id": "1f43559d-2fb2-480e-8a87-f357db5346c0",  # Database Integration PRD
        "capabilities": ["connection_pooling", "query_optimization", "health_monitoring"],
        "repository_url": "https://github.com/test/database-connection-agent",
        "deployment_url": "https://database-connection-agent.test.com",
        "health_check_url": "https://database-connection-agent.test.com/health"
    },
    {
        "name": "TEST_Database_Migration_Agent",
        "description": "Manages database schema migrations and versioning",
        "purpose": "Database schema migration and version control",
        "prd_id": "1f43559d-2fb2-480e-8a87-f357db5346c0",  # Same PRD as above
        "capabilities": ["schema_migration", "version_control", "rollback_management"],
        "repository_url": "https://github.com/test/database-migration-agent",
        "deployment_url": "https://database-migration-agent.test.com",
        "health_check_url": "https://database-migration-agent.test.com/health"
    },
    {
        "name": "TEST_Database_Backup_Agent",
        "description": "Automated database backup and recovery management",
        "purpose": "Database backup and disaster recovery",
        "prd_id": "1f43559d-2fb2-480e-8a87-f357db5346c0",  # Same PRD as above
        "capabilities": ["backup_scheduling", "recovery_testing", "storage_management"],
        "repository_url": "https://github.com/test/database-backup-agent",
        "deployment_url": "https://database-backup-agent.test.com",
        "health_check_url": "https://database-backup-agent.test.com/health"
    },
    
    # Multiple agents for JWT Authentication PRD
    {
        "name": "TEST_JWT_Token_Agent",
        "description": "JWT token generation, validation, and refresh management",
        "purpose": "JWT token lifecycle management",
        "prd_id": "c95961a4-e45d-45fb-bf4d-75a65ac372ef",  # JWT Authentication PRD
        "capabilities": ["token_generation", "token_validation", "refresh_management"],
        "repository_url": "https://github.com/test/jwt-token-agent",
        "deployment_url": "https://jwt-token-agent.test.com",
        "health_check_url": "https://jwt-token-agent.test.com/health"
    },
    {
        "name": "TEST_Authentication_Middleware_Agent",
        "description": "Authentication middleware for API request validation",
        "purpose": "API request authentication and authorization",
        "prd_id": "c95961a4-e45d-45fb-bf4d-75a65ac372ef",  # Same PRD as above
        "capabilities": ["request_validation", "authorization_check", "rate_limiting"],
        "repository_url": "https://github.com/test/auth-middleware-agent",
        "deployment_url": "https://auth-middleware-agent.test.com",
        "health_check_url": "https://auth-middleware-agent.test.com/health"
    },
    
    # Single agent for Testing Suite PRD
    {
        "name": "TEST_Automated_Test_Runner_Agent",
        "description": "Automated test execution and reporting system",
        "purpose": "Automated testing and quality assurance",
        "prd_id": "99286e57-619e-4d9e-9fc7-ec2f82a4c286",  # Testing Suite PRD
        "capabilities": ["test_execution", "reporting", "coverage_analysis"],
        "repository_url": "https://github.com/test/test-runner-agent",
        "deployment_url": "https://test-runner-agent.test.com",
        "health_check_url": "https://test-runner-agent.test.com/health"
    },
    
    # Standalone agent (no PRD reference)
    {
        "name": "TEST_Standalone_Monitoring_Agent",
        "description": "System monitoring and alerting agent",
        "purpose": "System health monitoring and alerting",
        "prd_id": None,  # No PRD reference
        "capabilities": ["system_monitoring", "alerting", "metrics_collection"],
        "repository_url": "https://github.com/test/monitoring-agent",
        "deployment_url": "https://monitoring-agent.test.com",
        "health_check_url": "https://monitoring-agent.test.com/health"
    }
]

def create_agent(agent_data):
    """Create an agent via API call."""
    # Prepare the request data
    request_data = {
        "name": agent_data["name"],
        "description": agent_data["description"],
        "purpose": agent_data["purpose"],
        "version": "1.0.0",
        "repository_url": agent_data["repository_url"],
        "deployment_url": agent_data["deployment_url"],
        "health_check_url": agent_data["health_check_url"],
        "prd_id": agent_data["prd_id"],
        "devin_task_id": str(uuid.uuid4()),
        "capabilities": agent_data["capabilities"],
        "configuration": {
            "test_data": True,
            "created_by": "test_script",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agents", json=request_data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to create agent {agent_data['name']}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating agent {agent_data['name']}: {e}")
        return None

def main():
    """Create test agents via API."""
    print("🚀 Creating test agents via API...")
    
    created_agents = []
    
    for agent_data in TEST_AGENTS:
        print(f"Creating agent: {agent_data['name']}")
        agent = create_agent(agent_data)
        if agent:
            created_agents.append(agent)
            prd_info = f" (PRD: {agent_data['prd_id'][:8]}...)" if agent_data['prd_id'] else " (Standalone)"
            print(f"✅ Created agent: {agent['name']}{prd_info}")
        else:
            print(f"❌ Failed to create agent: {agent_data['name']}")
    
    print(f"\n🎉 Test agent creation completed!")
    print(f"📊 Created {len(created_agents)} test agents")
    
    # Show summary by PRD
    prd_summary = {}
    for agent in created_agents:
        prd_id = agent.get('prd_id') or "standalone"
        if prd_id not in prd_summary:
            prd_summary[prd_id] = []
        prd_summary[prd_id].append(agent['name'])
    
    print("\n📋 Agent Summary by PRD:")
    for prd_id, agents in prd_summary.items():
        if prd_id == "standalone":
            print(f"  🏷️  Standalone: {len(agents)} agent(s)")
        else:
            print(f"  📄 PRD {prd_id[:8]}...: {len(agents)} agent(s)")
        for agent_name in agents:
            print(f"    - {agent_name}")
    
    # Test the API to verify agents are accessible
    print("\n🔍 Verifying agents are accessible via API...")
    try:
        response = requests.get(f"{BASE_URL}/agents")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned {data['total']} agents")
            if data['total'] > 0:
                print("📋 Agent names:")
                for agent in data['agents']:
                    print(f"  - {agent['name']}")
        else:
            print(f"❌ API verification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying API: {e}")

if __name__ == "__main__":
    main()
