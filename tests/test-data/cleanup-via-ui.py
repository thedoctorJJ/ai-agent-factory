#!/usr/bin/env python3
"""
Cleanup script that uses the UI delete endpoints to remove all data.
This is the most reliable method since it goes through the same code path as the UI.
"""

import requests
import time

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def cleanup_via_ui():
    """Clean up all data using the same endpoints as the UI."""
    print("🧹 Starting cleanup via UI endpoints...")
    
    # Get all agents
    try:
        agents_response = requests.get(f"{BASE_URL}/agents")
        if agents_response.status_code == 200:
            agents_data = agents_response.json()
            agents = agents_data.get('agents', [])
            print(f"📋 Found {len(agents)} agents to delete")
            
            # Delete all agents
            for agent in agents:
                try:
                    delete_response = requests.delete(f"{BASE_URL}/agents/{agent['id']}")
                    if delete_response.status_code == 200:
                        print(f"✅ Deleted agent: {agent['name']}")
                    else:
                        print(f"❌ Failed to delete agent {agent['name']}: {delete_response.status_code}")
                except Exception as e:
                    print(f"❌ Error deleting agent {agent['name']}: {e}")
        else:
            print(f"❌ Failed to fetch agents: {agents_response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching agents: {e}")
    
    # Get all PRDs
    try:
        prds_response = requests.get(f"{BASE_URL}/prds")
        if prds_response.status_code == 200:
            prds_data = prds_response.json()
            prds = prds_data.get('prds', [])
            print(f"📋 Found {len(prds)} PRDs to delete")
            
            # Delete all PRDs
            for prd in prds:
                try:
                    delete_response = requests.delete(f"{BASE_URL}/prds/{prd['id']}")
                    if delete_response.status_code == 200:
                        print(f"✅ Deleted PRD: {prd['title']}")
                    else:
                        print(f"❌ Failed to delete PRD {prd['title']}: {delete_response.status_code}")
                except Exception as e:
                    print(f"❌ Error deleting PRD {prd['title']}: {e}")
        else:
            print(f"❌ Failed to fetch PRDs: {prds_response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching PRDs: {e}")
    
    print("\n🎉 Cleanup completed!")
    
    # Verify cleanup
    print("\n🔍 Verifying cleanup...")
    time.sleep(1)  # Give the server a moment to process
    
    try:
        agents_response = requests.get(f"{BASE_URL}/agents")
        prds_response = requests.get(f"{BASE_URL}/prds")
        
        if agents_response.status_code == 200 and prds_response.status_code == 200:
            agents_data = agents_response.json()
            prds_data = prds_response.json()
            
            remaining_agents = len(agents_data.get('agents', []))
            remaining_prds = len(prds_data.get('prds', []))
            
            print(f"📊 Final status:")
            print(f"  - Agents: {remaining_agents}")
            print(f"  - PRDs: {remaining_prds}")
            
            if remaining_agents == 0 and remaining_prds == 0:
                print("✅ All data successfully removed!")
                print("🎉 Database is clean and ready for fresh data!")
            else:
                print("⚠️  Some data may still remain")
        else:
            print("❌ Could not verify cleanup status")
    except Exception as e:
        print(f"❌ Error verifying cleanup: {e}")

if __name__ == "__main__":
    cleanup_via_ui()
