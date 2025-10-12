#!/usr/bin/env python3
"""
Test script to verify the agent_type column was added successfully
"""
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi_app.utils.database import db_manager

async def test_agent_type_column():
    """Test if the agent_type column exists and works correctly."""
    print("🧪 Testing Agent Type Column")
    print("=" * 40)
    
    try:
        # Test if we can create an agent with agent_type
        print("1️⃣ Testing agent creation with agent_type...")
        
        import uuid
        test_agent_data = {
            "id": str(uuid.uuid4()),
            "name": "Test Agent Type",
            "description": "Testing agent_type column",
            "purpose": "Test the new agent_type functionality",
            "agent_type": "web_app",
            "version": "1.0.0",
            "status": "draft",
            "health_status": "unknown",
            "created_at": "2025-10-12T15:00:00Z",
            "updated_at": "2025-10-12T15:00:00Z"
        }
        
        # Try to create the agent
        result = await db_manager.create_agent(test_agent_data)
        
        if result:
            print("✅ SUCCESS: agent_type column is working!")
            print(f"   Created agent: {result.get('name', 'Unknown')}")
            print(f"   Agent type: {result.get('agent_type', 'Unknown')}")
            
            # Clean up - delete the test agent
            await db_manager.delete_agent(test_agent_data["id"])
            print("✅ Test agent cleaned up")
            
            return True
        else:
            print("❌ FAILED: Could not create agent with agent_type")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n🔧 This means the agent_type column is not properly added.")
        print("   Please run the SQL command in Supabase:")
        print("   See scripts/setup/add-agent-type-column.sql")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_type_column())
    if success:
        print("\n🎉 Agent type column working! Devin AI can now create agents successfully.")
    else:
        print("\n⚠️  Agent type column needs to be added. Please complete the Supabase update first.")
    sys.exit(0 if success else 1)
