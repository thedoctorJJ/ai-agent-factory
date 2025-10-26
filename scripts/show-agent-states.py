#!/usr/bin/env python3
"""
Show Agent States and Status
This script displays the different agent states and their current status in the system
"""

import requests
import json
import sys
from datetime import datetime

def show_agent_states():
    """Show different agent states and their definitions"""
    
    print("🤖 AI Agent Factory - Agent States and Status")
    print("=" * 60)
    
    # Agent Status Types
    print("\n📋 Agent Status Types:")
    print("-" * 30)
    agent_statuses = {
        "draft": "Initial state when agent is created but not yet active",
        "active": "Agent is running and operational",
        "inactive": "Agent is stopped or paused",
        "deprecated": "Agent is no longer maintained but may still work",
        "error": "Agent has encountered an error and needs attention"
    }
    
    for status, description in agent_statuses.items():
        print(f"  {status.upper():<12} - {description}")
    
    # Agent Health Status Types
    print("\n🏥 Agent Health Status Types:")
    print("-" * 35)
    health_statuses = {
        "healthy": "Agent is responding normally to health checks",
        "degraded": "Agent is working but with reduced functionality",
        "unhealthy": "Agent is not responding or has critical issues",
        "unknown": "Health status has not been checked yet"
    }
    
    for status, description in health_statuses.items():
        print(f"  {status.upper():<12} - {description}")
    
    # Agent Type Types
    print("\n🔧 Agent Type Categories:")
    print("-" * 30)
    agent_types = {
        "web_app": "Web application or frontend service",
        "api_service": "REST API or backend service",
        "data_processor": "Data processing or ETL service",
        "automation_script": "Automation or workflow script",
        "ai_model": "AI/ML model or inference service",
        "integration": "Integration or connector service",
        "other": "Other type of agent"
    }
    
    for agent_type, description in agent_types.items():
        print(f"  {agent_type.upper():<15} - {description}")
    
    print("\n" + "=" * 60)

def check_current_agents():
    """Check current agents in the system"""
    
    print("\n🔍 Current Agents in System:")
    print("-" * 35)
    
    backend_url = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    
    try:
        # Test if agents endpoint is working
        response = requests.get(f"{backend_url}/api/v1/agents", timeout=10)
        
        if response.status_code == 200:
            agents_data = response.json()
            agents = agents_data.get('agents', [])
            total = agents_data.get('total', 0)
            
            print(f"✅ Agents endpoint is working")
            print(f"📊 Total agents: {total}")
            
            if total > 0:
                print("\n📋 Agent Details:")
                for i, agent in enumerate(agents, 1):
                    print(f"\n  {i}. {agent.get('name', 'Unknown')}")
                    print(f"     ID: {agent.get('id', 'N/A')}")
                    print(f"     Status: {agent.get('status', 'N/A').upper()}")
                    print(f"     Health: {agent.get('health_status', 'N/A').upper()}")
                    print(f"     Type: {agent.get('agent_type', 'N/A').upper()}")
                    print(f"     Version: {agent.get('version', 'N/A')}")
                    print(f"     Deployment: {agent.get('deployment_url', 'N/A')}")
                    print(f"     Created: {agent.get('created_at', 'N/A')}")
            else:
                print("📭 No agents found in the system")
                
        else:
            print(f"❌ Agents endpoint error: {response.status_code}")
            print(f"   Response: {response.text}")
            print("\n💡 This likely means the agents table doesn't exist in the database.")
            print("   Please create the agents table first using the SQL provided earlier.")
            
    except Exception as e:
        print(f"❌ Error checking agents: {e}")
        print("\n💡 This likely means the agents table doesn't exist in the database.")
        print("   Please create the agents table first using the SQL provided earlier.")

def check_redis_agent_status():
    """Check the Redis agent status specifically"""
    
    print("\n🔴 Redis Agent Status:")
    print("-" * 25)
    
    redis_agent_url = "https://redis-caching-agent-fdqqqinvyq-uc.a.run.app"
    
    try:
        # Check Redis agent health
        health_response = requests.get(f"{redis_agent_url}/health", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Redis agent is running")
            print(f"   URL: {redis_agent_url}")
            print(f"   Status: {health_data.get('status', 'unknown').upper()}")
            print(f"   Version: {health_data.get('version', 'N/A')}")
            print(f"   Redis Connected: {health_data.get('redis_connected', 'N/A')}")
            print(f"   Uptime: {health_data.get('uptime_seconds', 'N/A')} seconds")
        else:
            print(f"❌ Redis agent health check failed: {health_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking Redis agent: {e}")

def show_system_status():
    """Show overall system status"""
    
    print("\n🌐 System Status:")
    print("-" * 20)
    
    backend_url = "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    frontend_url = "https://ai-agent-factory-frontend-952475323593.us-central1.run.app"
    
    # Check backend health
    try:
        health_response = requests.get(f"{backend_url}/api/v1/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Backend: {health_data.get('status', 'unknown').upper()}")
        else:
            print(f"❌ Backend: Error {health_response.status_code}")
    except Exception as e:
        print(f"❌ Backend: Error - {e}")
    
    # Check frontend
    try:
        frontend_response = requests.get(frontend_url, timeout=10)
        if frontend_response.status_code == 200:
            print(f"✅ Frontend: Accessible")
        else:
            print(f"❌ Frontend: Error {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")
    
    # Check PRDs
    try:
        prds_response = requests.get(f"{backend_url}/api/v1/prds", timeout=10)
        if prds_response.status_code == 200:
            prds_data = prds_response.json()
            print(f"✅ PRDs: {prds_data.get('total', 0)} available")
        else:
            print(f"❌ PRDs: Error {prds_response.status_code}")
    except Exception as e:
        print(f"❌ PRDs: Error - {e}")

def main():
    """Main function"""
    print("🚀 AI Agent Factory - Agent States and Status Checker")
    print("=" * 60)
    
    # Show agent state definitions
    show_agent_states()
    
    # Check current agents
    check_current_agents()
    
    # Check Redis agent specifically
    check_redis_agent_status()
    
    # Show system status
    show_system_status()
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("   - Agent states define the operational status of agents")
    print("   - Health status indicates the health of individual agents")
    print("   - Agent types categorize different kinds of agents")
    print("   - The Redis agent is running but may not be registered in the system")
    print("   - The agents table needs to be created to register agents")

if __name__ == "__main__":
    main()
