#!/usr/bin/env python3
"""
Fix RLS policies using MCP server code directly
This uses the same code as the MCP server to execute SQL
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config
from scripts.mcp.simple_services import SimpleSupabaseService

async def fix_rls_policies():
    """Fix RLS policies using MCP server code"""
    
    print("🔧 Fixing RLS Policies Using MCP Server Code")
    print("=" * 60)
    
    config = Config()
    
    if not config.database_url:
        print("❌ DATABASE_URL not configured")
        return False
    
    # Initialize Supabase service (same as MCP server)
    supabase_service = SimpleSupabaseService(
        config.supabase_url,
        config.supabase_service_role_key,
        database_url=config.database_url
    )
    
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
    
    print("Executing RLS fix SQL...")
    result = await supabase_service.execute_sql(rls_fix_sql)
    
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
        return False
    
    print("✅ RLS policies fixed successfully!")
    
    # Verify
    print("\nVerifying policies...")
    verify_sql = """
SELECT 
    tablename,
    policyname,
    with_check
FROM pg_policies
WHERE tablename IN ('prds', 'agents')
ORDER BY tablename, policyname;
"""
    
    verify_result = await supabase_service.execute_sql(verify_sql)
    if verify_result.get("data"):
        print("✅ Policies verified:")
        for policy in verify_result["data"]:
            print(f"   - {policy['tablename']}.{policy['policyname']} (WITH CHECK: {policy['with_check']})")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(fix_rls_policies())
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! RLS policies are now fixed")
        print("   You can now link the Redis agent to its PRD")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED! Please check the errors above")
        print("=" * 60)
        sys.exit(1)







