#!/usr/bin/env python3
"""
Fix RLS policies and link Redis agent to PRD
This script uses the same code as the MCP server to execute SQL directly
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config
from scripts.mcp.simple_services import SimpleSupabaseService
from backend.fastapi_app.utils.simple_data_manager import SimpleDataManager

async def fix_rls_and_link_agent():
    """Fix RLS policies and link Redis agent to PRD"""
    
    print("🔧 Fixing RLS Policies and Linking Redis Agent to PRD")
    print("=" * 60)
    
    config = Config()
    
    # Initialize Supabase service for SQL execution
    if not config.database_url:
        print("❌ DATABASE_URL not configured")
        return False
    
    supabase_service = SimpleSupabaseService(
        config.supabase_url,
        config.supabase_service_role_key,
        database_url=config.database_url
    )
    
    # Step 1: Fix RLS policies
    print("\n📋 Step 1: Fixing RLS Policies...")
    print("-" * 60)
    
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
        print(f"❌ Error fixing RLS: {result['error']}")
        return False
    
    print("✅ RLS policies fixed successfully!")
    if result.get("rows_affected"):
        print(f"   Rows affected: {result['rows_affected']}")
    
    # Step 2: Verify policies
    print("\n📋 Step 2: Verifying RLS Policies...")
    print("-" * 60)
    
    verify_sql = """
SELECT 
    tablename,
    policyname,
    cmd,
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
    else:
        print("⚠️  Could not verify policies (this is okay)")
    
    # Step 3: Link Redis agent to PRD
    print("\n📋 Step 3: Linking Redis Agent to PRD...")
    print("-" * 60)
    
    data_manager = SimpleDataManager()
    
    # Get Redis agent
    agents = await data_manager.get_agents(0, 100)
    redis_agent = next((a for a in agents if 'redis' in a.get('name', '').lower()), None)
    
    # Get Redis PRD
    prds = await data_manager.get_prds(0, 100)
    redis_prd = next((p for p in prds if 'redis' in p.get('title', '').lower() and 'caching' in p.get('title', '').lower()), None)
    
    if not redis_agent:
        print("❌ Redis agent not found")
        return False
    
    if not redis_prd:
        print("❌ Redis PRD not found")
        return False
    
    agent_id = redis_agent.get('id')
    prd_id = redis_prd.get('id')
    
    print(f"Agent: {redis_agent.get('name')}")
    print(f"  ID: {agent_id}")
    print(f"  Current PRD ID: {redis_agent.get('prd_id') or 'None (not linked)'}")
    print()
    print(f"PRD: {redis_prd.get('title')}")
    print(f"  ID: {prd_id}")
    print()
    
    # Update agent with PRD ID
    print("Updating agent with PRD ID...")
    update_data = {'prd_id': prd_id}
    
    try:
        updated_agent = await data_manager.update_agent(agent_id, update_data)
        
        if updated_agent:
            print("✅ Successfully linked!")
            print(f"   Agent PRD ID: {updated_agent.get('prd_id')}")
            return True
        else:
            print("❌ Update returned None - agent might not exist in database")
            return False
    except Exception as e:
        print(f"❌ Error updating agent: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(fix_rls_and_link_agent())
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Redis agent is now linked to its PRD")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED! Please check the errors above")
        print("=" * 60)
        sys.exit(1)








