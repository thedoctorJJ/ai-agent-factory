#!/usr/bin/env python3
"""
Check what's actually in the Supabase database.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def check_supabase():
    """Check what's in the Supabase database."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ SUPABASE_URL and SUPABASE_KEY must be set")
        return
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("🔗 Connected to Supabase")
        
        # Check agents table
        print("\n📊 Checking agents table...")
        response = supabase.from_("agents").select("id, name, prd_id").execute()
        agents = response.data if response.data else []
        print(f"Found {len(agents)} agents in Supabase:")
        for agent in agents:
            print(f"  - {agent.get('name', 'Unknown')} (ID: {agent.get('id', 'N/A')[:8]}..., PRD: {agent.get('prd_id', 'None')})")
        
        # Check PRDs table
        print("\n📊 Checking prds table...")
        response = supabase.from_("prds").select("id, title").execute()
        prds = response.data if response.data else []
        print(f"Found {len(prds)} PRDs in Supabase:")
        for prd in prds:
            print(f"  - {prd.get('title', 'Unknown')} (ID: {prd.get('id', 'N/A')[:8]}...)")
        
        if len(agents) > 0 or len(prds) > 0:
            print("\n💡 Found data in Supabase! This is where the agents are coming from.")
            print("🔧 We need to clear the Supabase database to stop the agents from reappearing.")
        else:
            print("\n✅ Supabase database is clean!")
            print("💡 The agents must be coming from somewhere else (in-memory storage or local cache)")
        
    except Exception as e:
        print(f"❌ Error checking Supabase: {e}")

if __name__ == "__main__":
    check_supabase()

