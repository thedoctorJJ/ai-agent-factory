#!/usr/bin/env python3
"""
Supabase Security Fixer
This script helps diagnose and fix Supabase security issues directly
"""

import os
import sys
import json
import requests
from datetime import datetime

def load_config():
    """Load configuration from environment"""
    config = {}
    
    # Try to load from .env.local
    env_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'env', '.env.local')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    
    # Override with environment variables
    config.update({
        'SUPABASE_URL': os.getenv('SUPABASE_URL', config.get('SUPABASE_URL')),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY', config.get('SUPABASE_SERVICE_ROLE_KEY'))
    })
    
    return config

def check_table_security(url, key, table_name):
    """Check security status for a specific table"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{url}/rest/v1/{table_name}?select=*&limit=1", headers=headers)
        
        security_info = {
            "table_name": table_name,
            "exists": False,
            "accessible": False,
            "status_code": response.status_code,
            "error": None
        }
        
        if response.status_code == 200:
            security_info["exists"] = True
            security_info["accessible"] = True
            data = response.json()
            security_info["sample_data"] = data[0] if data else None
        elif response.status_code == 401:
            security_info["error"] = "Unauthorized - Check API key permissions"
        elif response.status_code == 403:
            security_info["error"] = "Forbidden - RLS policies may be blocking access"
        elif response.status_code == 404:
            security_info["error"] = "Table not found"
        else:
            security_info["error"] = f"HTTP {response.status_code}: {response.text}"
        
        return security_info
        
    except Exception as e:
        return {
            "table_name": table_name,
            "exists": False,
            "accessible": False,
            "error": str(e)
        }

def test_agents_endpoint():
    """Test the agents endpoint"""
    try:
        response = requests.get(
            "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents",
            timeout=10
        )
        
        if response.status_code == 200:
            agents_data = response.json()
            return {
                "success": True,
                "message": "Agents endpoint is working",
                "total_agents": agents_data.get("total", 0),
                "agents": agents_data.get("agents", [])
            }
        else:
            return {
                "success": False,
                "message": f"Agents endpoint returned HTTP {response.status_code}",
                "response": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """Main function"""
    print("🔒 Supabase Security Fixer")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    
    if not config.get('SUPABASE_URL') or not config.get('SUPABASE_SERVICE_ROLE_KEY'):
        print("❌ Error: Supabase credentials not found")
        print("Please ensure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set")
        return
    
    print(f"🔧 Supabase URL: {config['SUPABASE_URL']}")
    print(f"🔧 Service Role Key: {config['SUPABASE_SERVICE_ROLE_KEY'][:50]}...")
    print()
    
    # Check database tables
    print("🔍 Checking database table security...")
    tables = ["agents", "prds", "devin_tasks"]
    
    for table in tables:
        print(f"\n📋 Checking {table} table...")
        security_info = check_table_security(
            config['SUPABASE_URL'],
            config['SUPABASE_SERVICE_ROLE_KEY'],
            table
        )
        
        if security_info["accessible"]:
            print(f"✅ {table}: Accessible")
            if security_info.get("sample_data"):
                print(f"   Sample data: {len(security_info['sample_data'])} fields")
        else:
            print(f"❌ {table}: Not accessible")
            print(f"   Error: {security_info['error']}")
            print(f"   Status Code: {security_info['status_code']}")
    
    # Test agents endpoint
    print(f"\n🌐 Testing agents endpoint...")
    agents_test = test_agents_endpoint()
    
    if agents_test["success"]:
        print(f"✅ Agents endpoint: Working")
        print(f"   Total agents: {agents_test['total_agents']}")
    else:
        print(f"❌ Agents endpoint: Not working")
        print(f"   Error: {agents_test.get('error', agents_test.get('message'))}")
    
    # Provide recommendations
    print(f"\n📋 Security Recommendations:")
    print("=" * 30)
    
    agents_security = check_table_security(
        config['SUPABASE_URL'],
        config['SUPABASE_SERVICE_ROLE_KEY'],
        "agents"
    )
    
    if not agents_security["accessible"]:
        print("🔧 Fix agents table security:")
        print("1. Go to Supabase Dashboard → SQL Editor")
        print("2. Run these SQL commands:")
        print()
        print("   -- Disable RLS on agents table")
        print("   ALTER TABLE agents DISABLE ROW LEVEL SECURITY;")
        print()
        print("   -- Grant permissions")
        print("   GRANT ALL PRIVILEGES ON TABLE agents TO postgres;")
        print("   GRANT ALL PRIVILEGES ON TABLE agents TO service_role;")
        print()
        print("3. Test the agents endpoint again")
    
    if not agents_test["success"]:
        print("🔧 Fix agents endpoint:")
        print("1. Ensure the agents table exists and is accessible")
        print("2. Check that the backend service is running")
        print("3. Verify database connection in the backend")
    
    print(f"\n🎯 Next Steps:")
    print("1. Fix the agents table security issues")
    print("2. Test the agents endpoint")
    print("3. Register the Redis agent")
    print("4. Verify the agent appears in the frontend")

if __name__ == "__main__":
    main()
