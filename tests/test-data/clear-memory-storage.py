#!/usr/bin/env python3
"""
Clear the in-memory storage by making a request that forces the service to clear its cache.
"""

import requests
import time

def clear_memory_storage():
    """Clear in-memory storage by restarting the backend service."""
    print("🔄 Clearing in-memory storage...")
    
    # Make a request to force the service to clear its in-memory storage
    # We'll use a special endpoint or method to clear the cache
    
    try:
        # First, let's try to make a request that might trigger a cache clear
        print("📡 Making request to clear cache...")
        
        # Try to get the current state
        response = requests.get("http://localhost:8000/api/v1/agents")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Current agents in memory: {len(data.get('agents', []))}")
            
            # If there are agents, try to delete them all again
            agents = data.get('agents', [])
            if agents:
                print(f"🗑️  Deleting {len(agents)} agents from memory...")
                for agent in agents:
                    try:
                        delete_response = requests.delete(f"http://localhost:8000/api/v1/agents/{agent['id']}")
                        if delete_response.status_code == 200:
                            print(f"✅ Deleted from memory: {agent['name']}")
                        else:
                            print(f"❌ Failed to delete from memory: {agent['name']}")
                    except Exception as e:
                        print(f"❌ Error deleting from memory: {e}")
                
                # Wait a moment for the deletions to process
                time.sleep(1)
                
                # Check if they're gone
                response = requests.get("http://localhost:8000/api/v1/agents")
                if response.status_code == 200:
                    data = response.json()
                    remaining = len(data.get('agents', []))
                    print(f"📊 Agents remaining after memory cleanup: {remaining}")
                    
                    if remaining == 0:
                        print("✅ In-memory storage cleared successfully!")
                    else:
                        print("⚠️  Agents still present in memory")
                        print("💡 This suggests the agents are being reloaded from somewhere else")
            else:
                print("✅ No agents in memory to clear")
        else:
            print(f"❌ Error checking agents: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error clearing memory storage: {e}")

if __name__ == "__main__":
    clear_memory_storage()