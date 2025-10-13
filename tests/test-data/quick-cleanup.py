#!/usr/bin/env python3
"""
Quick cleanup script to remove all test data without interactive prompts.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def cleanup_all_data():
    """Remove all agents and PRDs."""
    print("🧹 Starting quick cleanup of all data...")
    
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
    try:
        agents_response = requests.get(f"{BASE_URL}/agents")
        prds_response = requests.get(f"{BASE_URL}/prds")
        
        if agents_response.status_code == 200 and prds_response.status_code == 200:
            agents_data = agents_response.json()
            prds_data = prds_response.json()
            
            remaining_agents = len(agents_data.get('agents', []))
            remaining_prds = len(prds_data.get('prds', []))
            
            print(f"📊 Remaining data:")
            print(f"  - Agents: {remaining_agents}")
            print(f"  - PRDs: {remaining_prds}")
            
            if remaining_agents == 0 and remaining_prds == 0:
                print("✅ All data successfully removed!")
            else:
                print("⚠️  Some data may still remain")
        else:
            print("❌ Could not verify cleanup status")
    except Exception as e:
        print(f"❌ Error verifying cleanup: {e}")

if __name__ == "__main__":
    cleanup_all_data()
