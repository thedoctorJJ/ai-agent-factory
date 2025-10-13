#!/usr/bin/env python3
"""
Test Data Cleanup Script for AI Agent Factory
Removes all test data created by the test scripts.

This script identifies and removes:
- All agents with names starting with "TEST_"
- All PRDs created by the sample PRD script
- Any other test data marked with test_data: true
"""

import sys
import os
import asyncio

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from fastapi_app.services.agent_service import agent_service
from fastapi_app.services.prd_service import prd_service

async def cleanup_test_agents():
    """Remove all test agents."""
    print("🧹 Cleaning up test agents...")
    
    try:
        # Get all agents
        agents_response = await agent_service.get_agents(limit=1000)
        test_agents = []
        
        for agent in agents_response.agents:
            # Check if it's a test agent
            if (agent.name.startswith("TEST_") or 
                (agent.configuration and agent.configuration.get("test_data") == True)):
                test_agents.append(agent)
        
        if not test_agents:
            print("✅ No test agents found to clean up")
            return
        
        print(f"📋 Found {len(test_agents)} test agents to remove:")
        for agent in test_agents:
            print(f"  - {agent.name}")
        
        # Delete test agents
        deleted_count = 0
        for agent in test_agents:
            try:
                await agent_service.delete_agent(agent.id)
                deleted_count += 1
                print(f"✅ Deleted agent: {agent.name}")
            except Exception as e:
                print(f"❌ Failed to delete agent {agent.name}: {e}")
        
        print(f"🎉 Cleaned up {deleted_count} test agents")
        
    except Exception as e:
        print(f"❌ Error cleaning up test agents: {e}")

async def cleanup_test_prds():
    """Remove all test PRDs."""
    print("\n🧹 Cleaning up test PRDs...")
    
    try:
        # Get all PRDs
        prds_response = await prd_service.get_prds(limit=1000)
        test_prds = []
        
        # Known test PRD titles from the sample script
        test_prd_titles = [
            "Database Integration with Supabase",
            "JWT Authentication System", 
            "Comprehensive Testing Suite",
            "Structured Logging and Error Tracking",
            "Redis Caching Layer",
            "Performance Monitoring and Metrics",
            "Enhanced User Interface Components",
            "Advanced Agent Orchestration"
        ]
        
        for prd in prds_response.prds:
            # Check if it's a test PRD
            if (prd.title in test_prd_titles or 
                prd.title.startswith("Sample ") or
                prd.title.startswith("TEST_")):
                test_prds.append(prd)
        
        if not test_prds:
            print("✅ No test PRDs found to clean up")
            return
        
        print(f"📋 Found {len(test_prds)} test PRDs to remove:")
        for prd in test_prds:
            print(f"  - {prd.title}")
        
        # Delete test PRDs
        deleted_count = 0
        for prd in test_prds:
            try:
                await prd_service.delete_prd(prd.id)
                deleted_count += 1
                print(f"✅ Deleted PRD: {prd.title}")
            except Exception as e:
                print(f"❌ Failed to delete PRD {prd.title}: {e}")
        
        print(f"🎉 Cleaned up {deleted_count} test PRDs")
        
    except Exception as e:
        print(f"❌ Error cleaning up test PRDs: {e}")

async def main():
    """Main cleanup function."""
    print("🚀 Starting test data cleanup...")
    print("⚠️  This will remove all test data from the AI Agent Factory")
    
    # Confirm cleanup
    try:
        confirm = input("\nAre you sure you want to delete all test data? (yes/no): ").lower().strip()
        if confirm not in ['yes', 'y']:
            print("❌ Cleanup cancelled")
            return
    except KeyboardInterrupt:
        print("\n❌ Cleanup cancelled")
        return
    
    try:
        await cleanup_test_agents()
        await cleanup_test_prds()
        print("\n🎉 Test data cleanup completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
