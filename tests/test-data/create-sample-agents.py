#!/usr/bin/env python3
"""
Test Data Creation Script for AI Agent Factory
Creates sample agents to demonstrate one-to-many PRD-to-Agent relationships.

This script creates test data that can be easily identified and removed.
All test agents have names starting with "TEST_" for easy identification.
"""

import sys
import os
import asyncio
import uuid
from datetime import datetime, timezone

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from fastapi_app.services.agent_service import agent_service
from fastapi_app.models.agent import AgentRegistration, AgentStatus, AgentHealthStatus

# Test data configuration
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

async def create_test_agents():
    """Create test agents to demonstrate one-to-many relationships."""
    print("Creating test agents to demonstrate PRD-to-Agent relationships...")
    
    created_agents = []
    
    for agent_data in TEST_AGENTS:
        try:
            # Create agent registration
            agent_registration = AgentRegistration(
                name=agent_data["name"],
                description=agent_data["description"],
                purpose=agent_data["purpose"],
                version="1.0.0",
                repository_url=agent_data["repository_url"],
                deployment_url=agent_data["deployment_url"],
                health_check_url=agent_data["health_check_url"],
                prd_id=agent_data["prd_id"],
                devin_task_id=str(uuid.uuid4()),
                capabilities=agent_data["capabilities"],
                configuration={
                    "test_data": True,
                    "created_by": "test_script",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # Create the agent
            agent = await agent_service.create_agent(agent_registration)
            created_agents.append(agent)
            
            prd_info = f" (PRD: {agent_data['prd_id'][:8]}...)" if agent_data['prd_id'] else " (Standalone)"
            print(f"✅ Created agent: {agent.name}{prd_info}")
            
        except Exception as e:
            print(f"❌ Failed to create agent {agent_data['name']}: {e}")
    
    print(f"\n🎉 Test agent creation completed!")
    print(f"📊 Created {len(created_agents)} test agents")
    
    # Show summary by PRD
    prd_summary = {}
    for agent in created_agents:
        prd_id = agent.prd_id or "standalone"
        if prd_id not in prd_summary:
            prd_summary[prd_id] = []
        prd_summary[prd_id].append(agent.name)
    
    print("\n📋 Agent Summary by PRD:")
    for prd_id, agents in prd_summary.items():
        if prd_id == "standalone":
            print(f"  🏷️  Standalone: {len(agents)} agent(s)")
        else:
            print(f"  📄 PRD {prd_id[:8]}...: {len(agents)} agent(s)")
        for agent_name in agents:
            print(f"    - {agent_name}")
    
    return created_agents

async def main():
    """Main function to create test agents."""
    try:
        await create_test_agents()
    except Exception as e:
        print(f"❌ Error creating test agents: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
