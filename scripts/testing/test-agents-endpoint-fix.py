#!/usr/bin/env python3
"""
Test script to verify the agents endpoint fix.
This script simulates the data format from Supabase and tests the conversion logic.
"""

import sys
import asyncio
import requests
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any

# Add backend to path for model imports only
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from fastapi_app.models.agent import AgentResponse, AgentStatus, AgentHealthStatus
except ImportError as e:
    print(f"⚠️  Could not import models: {e}")
    print("   This is okay - we'll test the conversion logic directly")
    AgentResponse = None
    AgentStatus = None
    AgentHealthStatus = None


def create_mock_supabase_agent() -> Dict[str, Any]:
    """Create a mock agent in the format that Supabase returns."""
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Test Agent",
        "description": "A test agent",
        "purpose": "Testing the fix",
        "agent_type": "api_service",
        "version": "1.0.0",
        "status": "draft",  # String from Supabase
        "health_status": "unknown",  # String from Supabase
        "repository_url": "https://github.com/test/test-agent",
        "deployment_url": "https://test-agent.example.com",
        "health_check_url": "https://test-agent.example.com/health",
        "prd_id": None,
        "devin_task_id": None,
        "capabilities": ["test", "debug"],
        "configuration": {},
        "metrics": {},
        "created_at": "2025-11-13T21:00:00.000000Z",  # ISO string from Supabase
        "updated_at": "2025-11-13T21:00:00.000000Z",  # ISO string from Supabase
        "last_health_check": None,
    }


def apply_fix_logic(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Apply the fix logic to convert Supabase data format."""
    # Convert datetime strings to datetime objects if needed
    if isinstance(agent.get("created_at"), str):
        agent["created_at"] = datetime.fromisoformat(agent["created_at"].replace('Z', '+00:00'))
    if isinstance(agent.get("updated_at"), str):
        agent["updated_at"] = datetime.fromisoformat(agent["updated_at"].replace('Z', '+00:00'))
    if agent.get("last_health_check") and isinstance(agent["last_health_check"], str):
        agent["last_health_check"] = datetime.fromisoformat(agent["last_health_check"].replace('Z', '+00:00'))
    
    # Ensure status and health_status are valid enum values
    if agent.get("status"):
        try:
            if AgentStatus:
                AgentStatus(agent["status"])
        except (ValueError, TypeError):
            agent["status"] = "draft"  # Default value
    else:
        agent["status"] = "draft"
        
    if agent.get("health_status"):
        try:
            if AgentHealthStatus:
                AgentHealthStatus(agent["health_status"])
        except (ValueError, TypeError):
            agent["health_status"] = "unknown"  # Default value
    else:
        agent["health_status"] = "unknown"
    
    return agent


def test_datetime_conversion():
    """Test that datetime strings are properly converted."""
    print("🧪 Test 1: Datetime Conversion")
    print("=" * 50)
    
    mock_agent = create_mock_supabase_agent()
    
    # Apply the fix logic
    fixed_agent = apply_fix_logic(mock_agent.copy())
    
    # Verify conversion worked
    assert isinstance(fixed_agent["created_at"], datetime), "created_at should be datetime object"
    assert isinstance(fixed_agent["updated_at"], datetime), "updated_at should be datetime object"
    
    print("✅ Datetime conversion test passed")
    print(f"   created_at type: {type(fixed_agent['created_at'])}")
    print(f"   updated_at type: {type(fixed_agent['updated_at'])}")
    print(f"   created_at value: {fixed_agent['created_at']}")
    print()


def test_enum_validation():
    """Test that enum values are properly validated."""
    print("🧪 Test 2: Enum Validation")
    print("=" * 50)
    
    # Test valid enum values
    mock_agent = create_mock_supabase_agent()
    mock_agent["status"] = "draft"
    mock_agent["health_status"] = "unknown"
    
    fixed_agent = apply_fix_logic(mock_agent.copy())
    
    assert fixed_agent["status"] == "draft", "Status should remain draft"
    assert fixed_agent["health_status"] == "unknown", "Health status should remain unknown"
    
    print("✅ Valid enum values preserved")
    
    # Test invalid enum values (should default to safe values)
    mock_agent["status"] = "invalid_status"
    mock_agent["health_status"] = "invalid_health"
    
    fixed_agent = apply_fix_logic(mock_agent.copy())
    
    assert fixed_agent["status"] == "draft", "Invalid status should default to draft"
    assert fixed_agent["health_status"] == "unknown", "Invalid health_status should default to unknown"
    
    print("✅ Invalid enum values defaulted to safe values")
    print(f"   Final status: {fixed_agent['status']}")
    print(f"   Final health_status: {fixed_agent['health_status']}")
    print()


def test_agent_response_creation():
    """Test that AgentResponse can be created from Supabase data format."""
    print("🧪 Test 3: AgentResponse Creation")
    print("=" * 50)
    
    if not AgentResponse:
        print("⚠️  Skipping - AgentResponse model not available")
        print("   (This is okay if dependencies aren't installed)")
        return False
    
    mock_agent = create_mock_supabase_agent()
    fixed_agent = apply_fix_logic(mock_agent.copy())
    
    # Try to create AgentResponse
    try:
        agent_response = AgentResponse(**fixed_agent)
        print("✅ AgentResponse created successfully")
        print(f"   Agent ID: {agent_response.id}")
        print(f"   Agent Name: {agent_response.name}")
        print(f"   Status: {agent_response.status}")
        print(f"   Health Status: {agent_response.health_status}")
        print(f"   Created At: {agent_response.created_at} (type: {type(agent_response.created_at)})")
        return True
    except Exception as e:
        print(f"❌ Failed to create AgentResponse: {e}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_production_endpoint():
    """Test the actual production endpoint."""
    print("🧪 Test 4: Production Endpoint Test")
    print("=" * 50)
    
    url = "https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app/api/v1/agents"
    
    try:
        print(f"   Testing: {url}")
        response = requests.get(url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Production endpoint working!")
            print(f"   Response keys: {list(data.keys())}")
            print(f"   Total agents: {data.get('total', 0)}")
            if data.get('agents'):
                print(f"   First agent ID: {data['agents'][0].get('id', 'N/A')}")
            return True
        elif response.status_code == 500:
            print("❌ Production endpoint still returning 500 error")
            print("   The fix has not been deployed yet")
            print(f"   Response: {response.text[:200]}")
            return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error testing production endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Testing Agents Endpoint Fix")
    print("=" * 50)
    print()
    
    results = []
    
    # Test 1: Datetime conversion
    try:
        test_datetime_conversion()
        results.append(("Datetime Conversion", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Datetime Conversion", False))
    
    # Test 2: Enum validation
    try:
        test_enum_validation()
        results.append(("Enum Validation", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Enum Validation", False))
    
    # Test 3: AgentResponse creation
    try:
        success = test_agent_response_creation()
        results.append(("AgentResponse Creation", success))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("AgentResponse Creation", False))
    
    # Test 4: Production endpoint
    try:
        success = test_production_endpoint()
        results.append(("Production Endpoint", success))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Production Endpoint", False))
    
    # Summary
    print()
    print("📊 Test Summary")
    print("=" * 50)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    print()
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed - see details above")
        print()
        print("💡 Note: If Production Endpoint test failed, the fix needs to be deployed.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
