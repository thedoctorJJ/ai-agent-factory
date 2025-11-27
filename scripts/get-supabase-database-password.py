#!/usr/bin/env python3
"""
Get Supabase database password using Management API
This script attempts to retrieve the database connection string from Supabase
"""

import sys
import requests
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config

def get_database_password():
    """Attempt to get database password from Supabase Management API"""
    
    config = Config()
    
    if not config.supabase_url:
        print("❌ SUPABASE_URL not configured")
        return None
    
    # Extract project ref from URL
    # URL format: https://[PROJECT_REF].supabase.co
    project_ref = config.supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    print(f"🔍 Attempting to retrieve database password for project: {project_ref}")
    print("=" * 60)
    
    # Option 1: Try Supabase Management API
    # Note: This requires a personal access token, not the service role key
    print("\n📋 Option 1: Supabase Management API")
    print("   Requires: Personal Access Token (not service role key)")
    print("   API: https://api.supabase.com/v1/projects/{project_ref}/database/password")
    print("   Status: ⚠️  Requires personal access token setup")
    
    # Option 2: Use Supabase CLI
    print("\n📋 Option 2: Supabase CLI")
    print("   Command: supabase projects api-keys --project-ref {project_ref}")
    print("   Status: ⚠️  Requires Supabase CLI installation and authentication")
    
    # Option 3: Check if password is stored elsewhere
    print("\n📋 Option 3: Check existing configuration")
    print("   Checking MCP config...")
    
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if mcp_config_path.exists():
        with open(mcp_config_path) as f:
            mcp_config = json.load(f)
            db_url = mcp_config.get("mcpServers", {}).get("ai-agent-factory", {}).get("env", {}).get("DATABASE_URL", "")
            if db_url and "postgres:postgres" not in db_url:
                print(f"   ✅ Found DATABASE_URL in MCP config (non-placeholder)")
                # Extract password
                if "@" in db_url:
                    parts = db_url.split("@")
                    if ":" in parts[0]:
                        password = parts[0].split(":")[-1]
                        if password != "postgres":
                            print(f"   Password found: {password[:10]}...")
                            return password
    
    print("\n❌ Could not retrieve database password automatically")
    print("\n💡 Solutions:")
    print("   1. Use Supabase CLI: supabase projects api-keys --project-ref {project_ref}")
    print("   2. Check Supabase project settings for connection string")
    print("   3. Reset database password in Supabase Dashboard")
    print("   4. Use Supabase Management API with personal access token")
    
    return None

if __name__ == "__main__":
    password = get_database_password()
    if password:
        print(f"\n✅ Database password retrieved: {password[:10]}...")
    else:
        print("\n⚠️  Manual intervention required to get database password")







