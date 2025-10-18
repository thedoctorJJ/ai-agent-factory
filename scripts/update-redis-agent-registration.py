#!/usr/bin/env python3
"""
Update Redis Agent registration in AI Agent Factory platform
Updates the agent record with new Google Cloud Run deployment URL
"""

import os
import sys
import json
import requests
from typing import Dict, Any

# Add the backend directory to the path
sys.path.append('/Users/jason/Repositories/ai-agent-factory/backend')

from fastapi_app.services.agent_service import agent_service
from fastapi_app.models.agent import AgentRegistration, AgentStatus

class RedisAgentUpdater:
    def __init__(self, new_deployment_url: str):
        self.new_deployment_url = new_deployment_url
        self.agent_name = "Redis Caching Layer Agent"
        
    async def find_existing_agent(self) -> Dict[str, Any]:
        """Find the existing Redis agent in the platform"""
        try:
            # Get all agents
            agents_response = await agent_service.get_all_agents()
            
            # Find the Redis agent
            for agent in agents_response.get('agents', []):
                if 'redis' in agent.get('name', '').lower() or 'caching' in agent.get('name', '').lower():
                    return agent
            
            return None
            
        except Exception as e:
            print(f"❌ Error finding existing agent: {e}")
            return None
    
    async def update_agent_registration(self) -> bool:
        """Update the agent registration with new deployment URL"""
        try:
            # Find existing agent
            existing_agent = await self.find_existing_agent()
            
            if not existing_agent:
                print("❌ No existing Redis agent found")
                return False
            
            print(f"✅ Found existing agent: {existing_agent['name']}")
            print(f"   Current URL: {existing_agent.get('deployment_url', 'N/A')}")
            
            # Create updated agent registration
            updated_registration = AgentRegistration(
                name=existing_agent['name'],
                description=existing_agent['description'],
                purpose=existing_agent['purpose'],
                version="2.0.0",  # Updated version for Google Cloud Run
                repository_url=existing_agent.get('repository_url', ''),
                deployment_url=self.new_deployment_url,
                health_check_url=f"{self.new_deployment_url}/health",
                prd_id=existing_agent.get('prd_id'),
                devin_task_id=existing_agent.get('devin_task_id'),
                capabilities=existing_agent.get('capabilities', []),
                configuration={
                    **existing_agent.get('configuration', {}),
                    'platform': 'google-cloud-run',
                    'region': 'us-central1',
                    'redis_host': '10.1.93.195',
                    'redis_port': 6379
                }
            )
            
            # Update the agent
            result = await agent_service.update_agent(
                existing_agent['id'], 
                updated_registration
            )
            
            if result:
                print(f"✅ Agent registration updated successfully!")
                print(f"   New URL: {self.new_deployment_url}")
                print(f"   Health Check: {self.new_deployment_url}/health")
                return True
            else:
                print("❌ Failed to update agent registration")
                return False
                
        except Exception as e:
            print(f"❌ Error updating agent registration: {e}")
            return False
    
    async def test_new_deployment(self) -> bool:
        """Test the new deployment to ensure it's working"""
        try:
            print("🧪 Testing new deployment...")
            
            # Test health endpoint
            health_url = f"{self.new_deployment_url}/health"
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('status') == 'healthy':
                    print("✅ Health check passed")
                else:
                    print(f"❌ Health check failed: {health_data}")
                    return False
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test cache operations
            cache_url = f"{self.new_deployment_url}/cache"
            
            # Test set
            set_response = requests.post(
                cache_url,
                json={"key": "migration-test", "value": "test-value", "ttl": 60},
                timeout=10
            )
            
            if set_response.status_code == 200:
                print("✅ Cache set operation passed")
            else:
                print(f"❌ Cache set operation failed: {set_response.status_code}")
                return False
            
            # Test get
            get_response = requests.get(f"{cache_url}/migration-test", timeout=10)
            
            if get_response.status_code == 200:
                get_data = get_response.json()
                if get_data.get('value') == 'test-value':
                    print("✅ Cache get operation passed")
                else:
                    print(f"❌ Cache get operation failed: {get_data}")
                    return False
            else:
                print(f"❌ Cache get operation failed: {get_response.status_code}")
                return False
            
            # Test stats
            stats_response = requests.get(f"{self.new_deployment_url}/cache/stats", timeout=10)
            
            if stats_response.status_code == 200:
                print("✅ Cache stats operation passed")
            else:
                print(f"❌ Cache stats operation failed: {stats_response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing deployment: {e}")
            return False

async def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python update-redis-agent-registration.py <new-deployment-url>")
        print("Example: python update-redis-agent-registration.py https://redis-caching-agent-xxxxx-uc.a.run.app")
        sys.exit(1)
    
    new_deployment_url = sys.argv[1].rstrip('/')
    
    print("🔄 Updating Redis Agent registration...")
    print(f"New deployment URL: {new_deployment_url}")
    
    updater = RedisAgentUpdater(new_deployment_url)
    
    # Test the new deployment first
    if not await updater.test_new_deployment():
        print("❌ New deployment test failed. Aborting update.")
        sys.exit(1)
    
    # Update the agent registration
    if await updater.update_agent_registration():
        print("🎉 Redis Agent migration completed successfully!")
        print("")
        print("Next steps:")
        print("1. Verify the agent appears correctly in the AI Agent Factory dashboard")
        print("2. Test all functionality through the platform")
        print("3. Monitor performance and scaling")
        print("4. Consider decommissioning the Fly.io deployment")
    else:
        print("❌ Failed to update agent registration")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
