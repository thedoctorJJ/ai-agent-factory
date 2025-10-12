#!/usr/bin/env python3
"""
Test script to verify the Supabase schema update for ready_for_devin status
"""
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi_app.utils.database import db_manager

async def test_schema_update():
    """Test if the ready_for_devin status is available in the database."""
    print("🧪 Testing Supabase Schema Update")
    print("=" * 40)
    
    try:
        # Test if we can create a PRD with ready_for_devin status
        print("1️⃣ Testing PRD creation with ready_for_devin status...")
        
        test_prd_data = {
            "id": "test-schema-update-123",
            "title": "Schema Update Test",
            "description": "Testing if ready_for_devin status works",
            "requirements": ["Test requirement"],
            "prd_type": "agent",
            "status": "ready_for_devin",
            "created_at": "2025-10-12T14:00:00Z",
            "updated_at": "2025-10-12T14:00:00Z"
        }
        
        # Try to create the PRD
        result = await db_manager.create_prd(test_prd_data)
        
        if result:
            print("✅ SUCCESS: ready_for_devin status is working!")
            print(f"   Created PRD: {result.get('title', 'Unknown')}")
            print(f"   Status: {result.get('status', 'Unknown')}")
            
            # Clean up - delete the test PRD
            await db_manager.delete_prd("test-schema-update-123")
            print("✅ Test PRD cleaned up")
            
            return True
        else:
            print("❌ FAILED: Could not create PRD with ready_for_devin status")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n🔧 This means the schema update is not complete.")
        print("   Please run the SQL command in Supabase:")
        print("   ALTER TYPE prd_status ADD VALUE 'ready_for_devin';")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_schema_update())
    if success:
        print("\n🎉 Schema update successful! You can now test the manual Devin workflow.")
    else:
        print("\n⚠️  Schema update needed. Please complete the Supabase update first.")
    sys.exit(0 if success else 1)
