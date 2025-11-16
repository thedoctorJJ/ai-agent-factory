#!/usr/bin/env python3
"""
Health Check Script for MCP Server and Database Connectivity
This script verifies that:
1. MCP server is accessible and working
2. Database is accessible via MCP server
3. Can execute SQL queries through MCP
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_mcp_server():
    """Check if MCP server can be imported and initialized"""
    print("🔍 Checking MCP Server...")
    print("-" * 60)
    
    try:
        # Try to import MCP server
        import importlib.util
        mcp_script = project_root / "scripts" / "mcp" / "cursor-agent-mcp-server.py"
        
        if not mcp_script.exists():
            print("❌ MCP server script not found")
            return False
        
        spec = importlib.util.spec_from_file_location(
            "cursor_agent_mcp_server",
            mcp_script
        )
        mcp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mcp_module)
        
        # Try to initialize server
        server = mcp_module.CursorAgentMCPServer()
        print("✅ MCP server can be initialized")
        
        # Check if Supabase service is configured
        if server.supabase_service:
            print("✅ Supabase service is configured")
            if server.supabase_service.database_url:
                print("✅ Database URL is configured")
            else:
                print("⚠️  Database URL not configured")
        else:
            print("❌ Supabase service not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def check_database_via_mcp():
    """Check database connectivity via MCP server"""
    print("\n🔍 Checking Database via MCP Server...")
    print("-" * 60)
    
    try:
        # Import MCP server
        import importlib.util
        mcp_script = project_root / "scripts" / "mcp" / "cursor-agent-mcp-server.py"
        spec = importlib.util.spec_from_file_location(
            "cursor_agent_mcp_server",
            mcp_script
        )
        mcp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mcp_module)
        
        server = mcp_module.CursorAgentMCPServer()
        
        # Test 1: Simple SELECT query
        print("\n1. Testing simple SELECT query...")
        result = await server.call_tool("execute_supabase_sql", {
            "sql": "SELECT 1 as test;"
        })
        
        if result.get("success") and result.get("data"):
            print("   ✅ Database connection successful")
            print(f"   Result: {result.get('data')}")
        elif result.get("error"):
            print(f"   ❌ Database connection failed: {result.get('error')}")
            return False
        else:
            print(f"   ⚠️  Unexpected result: {result}")
            return False
        
        # Test 2: Check if tables exist
        print("\n2. Testing table access...")
        result = await server.call_tool("execute_supabase_sql", {
            "sql": "SELECT COUNT(*) as count FROM agents;"
        })
        
        if result.get("success"):
            print("   ✅ Agents table is accessible")
            if result.get("data"):
                count = result.get("data")[0].get("count", 0)
                print(f"   Found {count} agents in database")
        else:
            print(f"   ⚠️  Could not access agents table: {result.get('error', 'Unknown error')}")
        
        # Test 3: Check PRDs table
        result = await server.call_tool("execute_supabase_sql", {
            "sql": "SELECT COUNT(*) as count FROM prds;"
        })
        
        if result.get("success"):
            print("   ✅ PRDs table is accessible")
            if result.get("data"):
                count = result.get("data")[0].get("count", 0)
                print(f"   Found {count} PRDs in database")
        else:
            print(f"   ⚠️  Could not access PRDs table: {result.get('error', 'Unknown error')}")
        
        # Test 4: Check RLS policies
        print("\n3. Checking RLS policies...")
        result = await server.call_tool("execute_supabase_sql", {
            "sql": """
            SELECT tablename, policyname, with_check
            FROM pg_policies
            WHERE tablename IN ('prds', 'agents')
            ORDER BY tablename, policyname;
            """
        })
        
        if result.get("success") and result.get("data"):
            policies = result.get("data", [])
            print(f"   ✅ Found {len(policies)} RLS policies")
            for policy in policies:
                with_check = policy.get("with_check", "")
                status = "✅" if with_check else "⚠️"
                print(f"   {status} {policy.get('tablename')}.{policy.get('policyname')}")
        else:
            print(f"   ⚠️  Could not check RLS policies: {result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database check via MCP failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_mcp_config():
    """Check MCP configuration file"""
    print("\n🔍 Checking MCP Configuration...")
    print("-" * 60)
    
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    
    if not mcp_config_path.exists():
        print("❌ MCP configuration file not found")
        print(f"   Expected location: {mcp_config_path}")
        return False
    
    try:
        import json
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)
        
        if "mcpServers" in config and "ai-agent-factory" in config["mcpServers"]:
            print("✅ MCP server is configured in Cursor")
            server_config = config["mcpServers"]["ai-agent-factory"]
            
            # Check if DATABASE_URL is configured
            env = server_config.get("env", {})
            if "DATABASE_URL" in env:
                db_url = env["DATABASE_URL"]
                if "postgres:postgres" in db_url or "[PASSWORD]" in db_url:
                    print("   ⚠️  DATABASE_URL appears to have placeholder password")
                else:
                    print("   ✅ DATABASE_URL is configured")
            else:
                print("   ⚠️  DATABASE_URL not in MCP config (will use config file)")
            
            if "SUPABASE_URL" in env:
                print("   ✅ SUPABASE_URL is configured")
            if "SUPABASE_SERVICE_ROLE_KEY" in env:
                print("   ✅ SUPABASE_SERVICE_ROLE_KEY is configured")
        else:
            print("❌ MCP server not found in configuration")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to read MCP configuration: {e}")
        return False

async def main():
    """Run all health checks"""
    print("🏥 MCP Server and Database Health Check")
    print("=" * 60)
    print()
    
    results = {
        "mcp_config": False,
        "mcp_server": False,
        "database": False
    }
    
    # Check MCP configuration
    results["mcp_config"] = check_mcp_config()
    
    # Check MCP server
    results["mcp_server"] = check_mcp_server()
    
    # Check database via MCP
    if results["mcp_server"]:
        results["database"] = await check_database_via_mcp()
    else:
        print("\n⚠️  Skipping database check - MCP server not working")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Health Check Summary")
    print("=" * 60)
    print(f"MCP Configuration: {'✅ PASS' if results['mcp_config'] else '❌ FAIL'}")
    print(f"MCP Server:        {'✅ PASS' if results['mcp_server'] else '❌ FAIL'}")
    print(f"Database (via MCP): {'✅ PASS' if results['database'] else '❌ FAIL'}")
    print()
    
    if all(results.values()):
        print("✅ All checks passed! MCP server and database are working correctly.")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

