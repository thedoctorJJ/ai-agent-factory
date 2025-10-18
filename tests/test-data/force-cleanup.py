#!/usr/bin/env python3
"""
Force cleanup by restarting the backend and clearing all data.
"""

import subprocess
import time
import requests

def force_cleanup():
    """Force cleanup by restarting backend."""
    print("🔄 Force cleaning up by restarting backend...")
    
    # Kill the backend process
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        print("✅ Killed backend process")
    except Exception as e:
        print(f"⚠️  Error killing backend: {e}")
    
    # Wait a moment
    time.sleep(2)
    
    # Start the backend again
    try:
        subprocess.Popen([
            "bash", "-c", 
            "cd /Users/jason/Repositories/ai-agent-factory/backend && source venv/bin/activate && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload"
        ])
        print("✅ Restarted backend process")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    for i in range(10):
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Backend failed to start")
        return
    
    # Check if data is cleared
    try:
        agents_response = requests.get("http://localhost:8000/api/v1/agents")
        prds_response = requests.get("http://localhost:8000/api/v1/prds")
        
        if agents_response.status_code == 200 and prds_response.status_code == 200:
            agents_data = agents_response.json()
            prds_data = prds_response.json()
            
            remaining_agents = len(agents_data.get('agents', []))
            remaining_prds = len(prds_data.get('prds', []))
            
            print(f"📊 Data status after restart:")
            print(f"  - Agents: {remaining_agents}")
            print(f"  - PRDs: {remaining_prds}")
            
            if remaining_agents == 0 and remaining_prds == 0:
                print("✅ All data successfully cleared!")
            else:
                print("⚠️  Some data still remains")
        else:
            print("❌ Could not check data status")
    except Exception as e:
        print(f"❌ Error checking data status: {e}")

if __name__ == "__main__":
    force_cleanup()
