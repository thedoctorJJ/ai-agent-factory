#!/usr/bin/env python3
"""
Test Supabase Connection Script
This script tests the connection to Supabase and verifies the schema is applied correctly.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi_app.config import config
from fastapi_app.utils.database import db_manager

async def test_supabase_connection():
    """Test the Supabase connection and schema."""
    print("🧪 Testing Supabase Connection")
    print("=" * 40)
    
    # Check configuration
    print(f"🔧 Supabase URL: {config.supabase_url}")
    print(f"🔧 Supabase Key: {config.supabase_key[:50]}...")
    print()
    
    try:
        # Test basic connection
        print("1️⃣ Testing basic connection...")
        from supabase import create_client
        client = create_client(config.supabase_url, config.supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test if tables exist
        print("\n2️⃣ Testing table existence...")
        tables_to_test = ['prds', 'agents', 'devin_tasks']
        
        for table in tables_to_test:
            try:
                result = client.table(table).select('id').limit(1).execute()
                print(f"✅ Table '{table}' exists and is accessible")
            except Exception as e:
                print(f"❌ Table '{table}' not found or not accessible: {e}")
                return False
        
        # Test database manager
        print("\n3️⃣ Testing database manager...")
        is_connected = await db_manager.test_connection()
        if is_connected:
            print("✅ Database manager connection test successful")
        else:
            print("❌ Database manager connection test failed")
            return False
        
        # Test basic operations
        print("\n4️⃣ Testing basic operations...")
        
        # Test PRD operations
        prds = await db_manager.get_prds(limit=5)
        print(f"✅ PRD operations working - found {len(prds)} PRDs")
        
        # Test Agent operations
        agents = await db_manager.get_agents(limit=5)
        print(f"✅ Agent operations working - found {len(agents)} agents")
        
        print("\n🎉 All tests passed! Supabase is properly configured and working.")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you've applied the schema to your Supabase project")
        print("2. Check that your Supabase URL and keys are correct")
        print("3. Verify that Row Level Security policies are set up correctly")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_supabase_connection())
    sys.exit(0 if success else 1)
