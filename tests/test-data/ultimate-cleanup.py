#!/usr/bin/env python3
"""
Ultimate cleanup script that handles all possible data sources and scenarios.
"""

import subprocess
import time
import requests
import os
import glob
import sys

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

def ultimate_cleanup():
    """Ultimate cleanup of all data sources."""
    print("🚨 ULTIMATE CLEANUP: Clearing all possible data sources...")
    
    # Step 1: Stop all services
    print("🛑 Stopping all services...")
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        subprocess.run(["pkill", "-f", "next dev"], check=False)
        print("✅ Services stopped")
    except Exception as e:
        print(f"⚠️  Error stopping services: {e}")
    
    # Step 2: Clear all local database files
    print("🗑️  Clearing all local database files...")
    try:
        # Find all .db files
        db_files = glob.glob("/Users/jason/Repositories/end-cap-agent-factory/**/*.db", recursive=True)
        for db_file in db_files:
            os.remove(db_file)
            print(f"✅ Removed: {db_file}")
        
        # Also check for any SQLite files in common locations
        common_locations = [
            "/Users/jason/Repositories/end-cap-agent-factory/ai_agent_factory.db",
            "/Users/jason/Repositories/end-cap-agent-factory/backend/ai_agent_factory.db",
            "/Users/jason/Repositories/end-cap-agent-factory/frontend/ai_agent_factory.db",
        ]
        
        for location in common_locations:
            if os.path.exists(location):
                os.remove(location)
                print(f"✅ Removed: {location}")
        
        if not db_files and not any(os.path.exists(loc) for loc in common_locations):
            print("✅ No local database files found")
    except Exception as e:
        print(f"⚠️  Error clearing local files: {e}")
    
    # Step 3: Clear Supabase database
    print("🗑️  Clearing Supabase database...")
    try:
        result = subprocess.run([
            "python", "tests/test-data/clear-database.py"
        ], capture_output=True, text=True, cwd="/Users/jason/Repositories/end-cap-agent-factory")
        
        if result.returncode == 0:
            print("✅ Supabase database cleared")
        else:
            print(f"⚠️  Error clearing Supabase: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Error running database cleanup: {e}")
    
    # Step 4: Clear any Python cache files
    print("🗑️  Clearing Python cache files...")
    try:
        cache_dirs = glob.glob("/Users/jason/Repositories/end-cap-agent-factory/**/__pycache__", recursive=True)
        for cache_dir in cache_dirs:
            subprocess.run(["rm", "-rf", cache_dir], check=False)
            print(f"✅ Removed cache: {cache_dir}")
        
        pyc_files = glob.glob("/Users/jason/Repositories/end-cap-agent-factory/**/*.pyc", recursive=True)
        for pyc_file in pyc_files:
            os.remove(pyc_file)
            print(f"✅ Removed: {pyc_file}")
            
        if not cache_dirs and not pyc_files:
            print("✅ No Python cache files found")
    except Exception as e:
        print(f"⚠️  Error clearing cache files: {e}")
    
    # Step 5: Wait for cleanup to complete
    print("⏳ Waiting for cleanup to complete...")
    time.sleep(5)
    
    # Step 6: Start backend
    print("🚀 Starting backend...")
    try:
        subprocess.Popen([
            "bash", "-c", 
            "cd /Users/jason/Repositories/end-cap-agent-factory/backend && source venv/bin/activate && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload"
        ])
        print("✅ Backend started")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return
    
    # Step 7: Wait for backend to be ready
    print("⏳ Waiting for backend to be ready...")
    for i in range(20):
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
    
    # Step 8: Start frontend
    print("🚀 Starting frontend...")
    try:
        subprocess.Popen([
            "bash", "-c", 
            "cd /Users/jason/Repositories/end-cap-agent-factory/frontend/next-app && npm run dev"
        ])
        print("✅ Frontend started")
    except Exception as e:
        print(f"⚠️  Error starting frontend: {e}")
    
    # Step 9: Verify cleanup
    print("\n🔍 Verifying ultimate cleanup...")
    time.sleep(3)
    
    try:
        agents_response = requests.get("http://localhost:8000/api/v1/agents")
        prds_response = requests.get("http://localhost:8000/api/v1/prds")
        
        if agents_response.status_code == 200 and prds_response.status_code == 200:
            agents_data = agents_response.json()
            prds_data = prds_response.json()
            
            remaining_agents = len(agents_data.get('agents', []))
            remaining_prds = len(prds_data.get('prds', []))
            
            print(f"📊 Final status after ultimate cleanup:")
            print(f"  - Agents: {remaining_agents}")
            print(f"  - PRDs: {remaining_prds}")
            
            if remaining_agents == 0 and remaining_prds == 0:
                print("✅ ULTIMATE CLEANUP SUCCESSFUL!")
                print("🎉 Database is completely clean and ready for fresh data!")
                return True
            else:
                print("⚠️  Some data still remains after ultimate cleanup")
                if remaining_agents > 0:
                    print(f"   - {remaining_agents} agents still present")
                    print("   - This suggests a fundamental issue with data persistence")
                if remaining_prds > 0:
                    print(f"   - {remaining_prds} PRDs still present")
                return False
        else:
            print("❌ Could not verify cleanup status")
            return False
    except Exception as e:
        print(f"❌ Error verifying cleanup: {e}")
        return False

if __name__ == "__main__":
    success = ultimate_cleanup()
    if not success:
        print("\n💡 RECOMMENDATION:")
        print("   The data is persisting despite all cleanup attempts.")
        print("   This suggests there may be:")
        print("   1. A different data source we haven't identified")
        print("   2. A caching mechanism we haven't cleared")
        print("   3. A configuration issue with the database connection")
        print("   4. Hardcoded test data somewhere in the code")
        print("\n   Consider investigating the data flow more deeply.")
