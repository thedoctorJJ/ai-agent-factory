#!/usr/bin/env python3
"""
Complete cleanup script that handles all possible data sources.
"""

import subprocess
import time
import requests
import os
import glob

def complete_cleanup():
    """Complete cleanup of all data sources."""
    print("🧹 Starting complete cleanup...")
    
    # Step 1: Stop all services
    print("🛑 Stopping all services...")
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "next dev"], check=False)
        print("✅ Services stopped")
    except Exception as e:
        print(f"⚠️  Error stopping services: {e}")
    
    # Step 2: Clear local database files
    print("🗑️  Clearing local database files...")
    try:
        db_files = glob.glob("/Users/jason/Repositories/ai-agent-factory/**/*.db", recursive=True)
        for db_file in db_files:
            os.remove(db_file)
            print(f"✅ Removed: {db_file}")
        if not db_files:
            print("✅ No local database files found")
    except Exception as e:
        print(f"⚠️  Error clearing local files: {e}")
    
    # Step 3: Clear Supabase database
    print("🗑️  Clearing Supabase database...")
    try:
        result = subprocess.run([
            "python", "tests/test-data/clear-database.py"
        ], capture_output=True, text=True, cwd="/Users/jason/Repositories/ai-agent-factory")
        
        if result.returncode == 0:
            print("✅ Supabase database cleared")
        else:
            print(f"⚠️  Error clearing Supabase: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Error running database cleanup: {e}")
    
    # Step 4: Wait a moment
    print("⏳ Waiting for cleanup to complete...")
    time.sleep(3)
    
    # Step 5: Start backend
    print("🚀 Starting backend...")
    try:
        subprocess.Popen([
            "bash", "-c", 
            "cd /Users/jason/Repositories/ai-agent-factory/backend && source venv/bin/activate && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload"
        ])
        print("✅ Backend started")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return
    
    # Step 6: Wait for backend to be ready
    print("⏳ Waiting for backend to be ready...")
    for i in range(15):
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
    
    # Step 7: Start frontend
    print("🚀 Starting frontend...")
    try:
        subprocess.Popen([
            "bash", "-c", 
            "cd /Users/jason/Repositories/ai-agent-factory/frontend/next-app && npm run dev"
        ])
        print("✅ Frontend started")
    except Exception as e:
        print(f"⚠️  Error starting frontend: {e}")
    
    # Step 8: Verify cleanup
    print("\n🔍 Verifying cleanup...")
    time.sleep(2)
    
    try:
        agents_response = requests.get("http://localhost:8000/api/v1/agents")
        prds_response = requests.get("http://localhost:8000/api/v1/prds")
        
        if agents_response.status_code == 200 and prds_response.status_code == 200:
            agents_data = agents_response.json()
            prds_data = prds_response.json()
            
            remaining_agents = len(agents_data.get('agents', []))
            remaining_prds = len(prds_data.get('prds', []))
            
            print(f"📊 Final status:")
            print(f"  - Agents: {remaining_agents}")
            print(f"  - PRDs: {remaining_prds}")
            
            if remaining_agents == 0 and remaining_prds == 0:
                print("✅ Complete cleanup successful!")
                print("🎉 Database is completely clean and ready for fresh data!")
            else:
                print("⚠️  Some data still remains")
                if remaining_agents > 0:
                    print(f"   - {remaining_agents} agents still present")
                if remaining_prds > 0:
                    print(f"   - {remaining_prds} PRDs still present")
        else:
            print("❌ Could not verify cleanup status")
    except Exception as e:
        print(f"❌ Error verifying cleanup: {e}")

if __name__ == "__main__":
    complete_cleanup()
