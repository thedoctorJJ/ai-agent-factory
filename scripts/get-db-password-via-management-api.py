#!/usr/bin/env python3
"""
Get Supabase database password using Management API
Requires: SUPABASE_ACCESS_TOKEN (personal access token, not service role key)
"""

import sys
import requests
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config

def get_database_password_via_api():
    """Get database password using Supabase Management API"""
    
    config = Config()
    
    if not config.supabase_url:
        print("❌ SUPABASE_URL not configured")
        return None
    
    # Extract project ref from URL
    project_ref = config.supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    # Get access token from environment
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    if not access_token:
        print("❌ SUPABASE_ACCESS_TOKEN not found in environment")
        print("\n💡 To get your access token:")
        print("   1. Go to: https://supabase.com/dashboard/account/tokens")
        print("   2. Generate a new personal access token")
        print("   3. Set it as: export SUPABASE_ACCESS_TOKEN='your-token'")
        return None
    
    print(f"🔍 Retrieving database password for project: {project_ref}")
    print("=" * 60)
    
    # Supabase Management API endpoint
    url = f"https://api.supabase.com/v1/projects/{project_ref}/database/password"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            password = data.get("password")
            if password:
                print(f"✅ Database password retrieved successfully")
                return password
            else:
                print("❌ Password not found in API response")
                print(f"   Response: {data}")
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

if __name__ == "__main__":
    import os
    password = get_database_password_via_api()
    if password:
        print(f"\n✅ Database Password: {password}")
        print("\n📝 Update your configuration:")
        print(f"   DATABASE_URL=postgresql://postgres:{password}@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres")
    else:
        print("\n⚠️  Could not retrieve password")







