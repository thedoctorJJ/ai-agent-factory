#!/usr/bin/env python3
"""
Debug script to check the agent service state directly.
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from fastapi_app.services.agent_service import agent_service

def debug_agent_service():
    """Debug the agent service state."""
    print("🔍 Debugging agent service state...")
    
    print(f"📊 Agent service type: {type(agent_service)}")
    print(f"📊 Agent service ID: {id(agent_service)}")
    
    if hasattr(agent_service, '_agents_db'):
        print(f"📊 In-memory storage size: {len(agent_service._agents_db)}")
        if len(agent_service._agents_db) > 0:
            print("📋 Agents in memory:")
            for agent_id, agent_data in agent_service._agents_db.items():
                print(f"  - {agent_data.get('name', 'Unknown')} ({agent_id[:8]}...)")
        else:
            print("✅ In-memory storage is empty")
    else:
        print("❌ No _agents_db attribute found")
    
    # Check if there are any other attributes that might contain data
    print(f"\n📊 All agent service attributes:")
    for attr in dir(agent_service):
        if not attr.startswith('_'):
            continue
        try:
            value = getattr(agent_service, attr)
            if isinstance(value, (list, dict)):
                print(f"  - {attr}: {type(value)} with {len(value)} items")
            else:
                print(f"  - {attr}: {type(value)}")
        except:
            print(f"  - {attr}: <unable to access>")

if __name__ == "__main__":
    debug_agent_service()
