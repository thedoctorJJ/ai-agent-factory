#!/usr/bin/env python3
"""
Simple script to fix RLS policies using MCP server code
Uses minimal dependencies - just psycopg2 and environment variables
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

# Load environment variables from config
project_root = Path(__file__).parent.parent
env_local = project_root / "config" / "env" / ".env.local"

# Simple env loader
def load_env():
    """Load environment variables from .env.local"""
    if env_local.exists():
        with open(env_local) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env()

# Get DATABASE_URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("❌ DATABASE_URL not found in environment")
    print("   Make sure config/env/.env.local has DATABASE_URL set")
    sys.exit(1)

print("🔧 Fixing RLS Policies")
print("=" * 60)

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

try:
    print("Connecting to database...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("Executing RLS fix SQL...")
    cursor.execute(rls_fix_sql)
    conn.commit()
    
    print("✅ RLS policies fixed successfully!")
    
    # Verify
    print("\nVerifying policies...")
    cursor.execute("""
        SELECT tablename, policyname, with_check
        FROM pg_policies
        WHERE tablename IN ('prds', 'agents')
        ORDER BY tablename, policyname;
    """)
    policies = cursor.fetchall()
    
    for policy in policies:
        print(f"   ✅ {policy['tablename']}.{policy['policyname']} (WITH CHECK: {policy['with_check']})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! RLS policies are now fixed")
    print("   You can now link the Redis agent to its PRD")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)








