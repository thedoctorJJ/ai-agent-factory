#!/usr/bin/env python3
"""
Clear the entire database by dropping and recreating tables.
This is a nuclear option that will clear ALL data.
"""

import sys
import os
import asyncio
from supabase import create_client, Client

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from fastapi_app.config import config

async def clear_database():
    """Clear the entire database."""
    print("🚨 NUCLEAR OPTION: Clearing entire database...")
    print("⚠️  This will delete ALL data in the database!")
    
    try:
        # Create Supabase client
        supabase: Client = create_client(config.supabase_url, config.supabase_key)
        
        print("🔗 Connected to Supabase database")
        
        # Clear agents table
        print("🗑️  Clearing agents table...")
        try:
            result = supabase.table('agents').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            print(f"✅ Cleared agents table: {len(result.data)} records deleted")
        except Exception as e:
            print(f"❌ Error clearing agents table: {e}")
        
        # Clear prds table
        print("🗑️  Clearing PRDs table...")
        try:
            result = supabase.table('prds').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            print(f"✅ Cleared PRDs table: {len(result.data)} records deleted")
        except Exception as e:
            print(f"❌ Error clearing PRDs table: {e}")
        
        # Clear devin_tasks table if it exists
        print("🗑️  Clearing devin_tasks table...")
        try:
            result = supabase.table('devin_tasks').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            print(f"✅ Cleared devin_tasks table: {len(result.data)} records deleted")
        except Exception as e:
            print(f"⚠️  devin_tasks table may not exist or error: {e}")
        
        print("\n🎉 Database cleared successfully!")
        
        # Verify cleanup
        print("\n🔍 Verifying cleanup...")
        try:
            agents_result = supabase.table('agents').select('*').execute()
            prds_result = supabase.table('prds').select('*').execute()
            
            agents_count = len(agents_result.data)
            prds_count = len(prds_result.data)
            
            print(f"📊 Remaining data:")
            print(f"  - Agents: {agents_count}")
            print(f"  - PRDs: {prds_count}")
            
            if agents_count == 0 and prds_count == 0:
                print("✅ Database is completely clean!")
            else:
                print("⚠️  Some data may still remain")
                
        except Exception as e:
            print(f"❌ Error verifying cleanup: {e}")
            
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("💡 Make sure your Supabase credentials are correct in the config")

if __name__ == "__main__":
    asyncio.run(clear_database())
