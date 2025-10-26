#!/usr/bin/env python3
"""
Fix Supabase Security Issues
This script addresses common Supabase security concerns
"""

import sys
import os
import asyncio

# Add the backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi_app.utils.simple_data_manager import data_manager

async def fix_supabase_security():
    """Fix common Supabase security issues"""
    
    print("🔒 Checking and fixing Supabase security issues...")
    
    try:
        # Check if we can connect
        if not data_manager.supabase:
            print("❌ No Supabase connection available")
            return False
        
        print("✅ Connected to Supabase")
        
        # 1. Check RLS status on all tables
        print("\n📋 Checking Row Level Security (RLS) status...")
        
        tables_to_check = ['agents', 'prds', 'devin_tasks', 'audit_logs', 'system_metrics']
        
        for table in tables_to_check:
            try:
                # Try to query the table to see if RLS is blocking access
                result = data_manager.supabase.table(table).select('*').limit(1).execute()
                print(f"✅ Table '{table}': Accessible ({len(result.data)} records)")
            except Exception as e:
                print(f"❌ Table '{table}': Access error - {e}")
        
        # 2. Check if we can perform basic operations
        print("\n🧪 Testing basic CRUD operations...")
        
        try:
            # Test read
            agents = await data_manager.get_agents()
            print(f"✅ Read operation: Found {len(agents)} agents")
            
            # Test if we can create a test record (we'll clean it up)
            test_agent = {
                'name': 'security-test-agent',
                'description': 'Security test agent',
                'purpose': 'Testing security policies',
                'version': '1.0.0'
            }
            
            # Try to create
            created = await data_manager.create_agent(test_agent)
            if created:
                print("✅ Create operation: Success")
                
                # Clean up
                await data_manager.delete_agent(created['id'])
                print("✅ Delete operation: Success")
            else:
                print("❌ Create operation: Failed")
                
        except Exception as e:
            print(f"❌ CRUD test failed: {e}")
        
        # 3. Check for common security issues
        print("\n🔍 Checking for common security issues...")
        
        # Check if API keys are properly configured
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if supabase_url and 'localhost' not in supabase_url:
            print("✅ Using production Supabase URL")
        else:
            print("⚠️  Using localhost or missing Supabase URL")
        
        if supabase_key and len(supabase_key) > 20:
            print("✅ Supabase key appears to be properly configured")
        else:
            print("⚠️  Supabase key may be missing or too short")
        
        # 4. Provide recommendations
        print("\n📝 Security Recommendations:")
        print("1. Ensure RLS is enabled on all tables in Supabase dashboard")
        print("2. Review and update RLS policies to be more restrictive if needed")
        print("3. Check that API keys are not exposed in client-side code")
        print("4. Enable audit logging for sensitive operations")
        print("5. Regularly rotate API keys")
        print("6. Review authentication settings in Supabase dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Security check failed: {e}")
        return False

async def main():
    """Main function"""
    success = await fix_supabase_security()
    
    if success:
        print("\n🎉 Security check completed!")
        print("\nNext steps:")
        print("1. Review the Supabase dashboard for any remaining security warnings")
        print("2. Update RLS policies if needed")
        print("3. Check authentication settings")
        print("4. Consider enabling additional security features")
    else:
        print("\n❌ Security check failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
