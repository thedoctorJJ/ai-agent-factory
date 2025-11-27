#!/usr/bin/env python3
"""
Fix RLS policies using Supabase REST API
This uses the Supabase service role key to execute SQL via the API
"""

import sys
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config

def fix_rls_policies():
    """Fix RLS policies using Supabase REST API"""
    
    print("🔧 Fixing RLS Policies Using Supabase API")
    print("=" * 60)
    
    config = Config()
    
    if not config.supabase_url or not config.supabase_service_role_key:
        print("❌ Supabase configuration not found")
        return False
    
    # Use Supabase REST API to execute SQL
    # Supabase has a REST endpoint for running SQL queries
    url = f"{config.supabase_url}/rest/v1/rpc/exec_sql"
    
    # SQL to fix RLS
    rls_fix_sql = """
-- Fix Foreign Key Constraint Issue with RLS
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
DROP POLICY IF EXISTS "Service role can do everything on agents" ON agents;

CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL 
    USING (true)
    WITH CHECK (true);
"""
    
    headers = {
        "apikey": config.supabase_service_role_key,
        "Authorization": f"Bearer {config.supabase_service_role_key}",
        "Content-Type": "application/json"
    }
    
    # Note: Supabase REST API doesn't directly support arbitrary SQL execution
    # We need to use the PostgREST API or direct PostgreSQL connection
    # Let's try using the Supabase client library instead
    
    print("⚠️  Supabase REST API doesn't support arbitrary SQL execution")
    print("   We need to use direct PostgreSQL connection or Supabase Dashboard")
    print("\n📋 SQL to execute in Supabase Dashboard:")
    print("-" * 60)
    print(rls_fix_sql)
    print("-" * 60)
    print("\n🔗 Go to: https://supabase.com/dashboard")
    print("   1. Select your project")
    print("   2. Go to SQL Editor")
    print("   3. Paste the SQL above")
    print("   4. Click Run")
    
    return False

if __name__ == "__main__":
    fix_rls_policies()







