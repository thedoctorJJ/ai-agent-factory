#!/usr/bin/env python3
"""
Link Redis Agent to Redis PRD
This script directly updates the agent's prd_id in the database
"""

import sys
import os
sys.path.append('backend')

from fastapi_app.utils.simple_data_manager import SimpleDataManager
import asyncio

async def link_redis_agent_to_prd():
    """Link Redis agent to Redis PRD"""
    
    print("🔗 Linking Redis Agent to Redis PRD")
    print("=" * 50)
    
    data_manager = SimpleDataManager()
    
    # Get Redis agent
    agents = await data_manager.get_agents(0, 100)
    redis_agent = next((a for a in agents if 'redis' in a.get('name', '').lower()), None)
    
    # Get Redis PRD
    prds = await data_manager.get_prds(0, 100)
    redis_prd = next((p for p in prds if 'redis' in p.get('title', '').lower() and 'agent' in p.get('title', '').lower()), None)
    
    if not redis_agent:
        print("❌ Redis agent not found")
        return False
    
    if not redis_prd:
        print("❌ Redis PRD not found")
        return False
    
    agent_id = redis_agent.get('id')
    prd_id = redis_prd.get('id')
    
    print(f"Agent: {redis_agent.get('name')}")
    print(f"  ID: {agent_id}")
    print()
    print(f"PRD: {redis_prd.get('title')}")
    print(f"  ID: {prd_id}")
    print()
    
    # Update agent with PRD ID
    print("Updating agent with PRD ID...")
    update_data = {'prd_id': prd_id}
    
    try:
        updated_agent = await data_manager.update_agent(agent_id, update_data)
        
        if updated_agent:
            print("✅ Successfully linked!")
            print(f"  Agent PRD ID: {updated_agent.get('prd_id')}")
            return True
        else:
            print("❌ Update returned None - agent might not exist in database")
            return False
    except Exception as e:
        print(f"❌ Error updating agent: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(link_redis_agent_to_prd())
    if success:
        print("\n✅ Link established!")
    else:
        print("\n❌ Failed to establish link")
        sys.exit(1)

