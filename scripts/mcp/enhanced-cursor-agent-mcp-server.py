#!/usr/bin/env python3
"""
Enhanced Cursor Agent MCP Server with Supabase Management
This server provides comprehensive database management and security tools
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import sys
from pathlib import Path

# Add the MCP directory to the Python path
mcp_dir = Path(__file__).parent
sys.path.insert(0, str(mcp_dir))

from supabase_manager import SupabaseManager
from simple_services import SimpleSupabaseService, SimpleGitHubService, SimpleOpenAIService

class Config:
    """Configuration manager for environment variables"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.google_cloud_project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

class EnhancedCursorAgentMCPServer:
    """Enhanced MCP Server with Supabase management capabilities"""
    
    def __init__(self):
        self.config = Config()
        self.supabase_manager = None
        self.supabase_service = None
        self.github_service = None
        self.openai_service = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all platform services"""
        try:
            # Initialize Supabase Manager
            if self.config.supabase_url and self.config.supabase_service_role_key:
                self.supabase_manager = SupabaseManager(
                    self.config.supabase_url,
                    self.config.supabase_service_role_key
                )
                self.supabase_service = SimpleSupabaseService(
                    self.config.supabase_url,
                    self.config.supabase_service_role_key
                )
            
            # Initialize other services
            if self.config.github_token:
                self.github_service = SimpleGitHubService(self.config.github_token)
            
            if self.config.openai_api_key:
                self.openai_service = SimpleOpenAIService(self.config.openai_api_key)
        
        except Exception as e:
            print(f"Warning: Failed to initialize some services: {e}", file=sys.stderr)
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools for Cursor Agent"""
        return [
            {
                "name": "check_database_security",
                "description": "Check security status and RLS policies for all database tables",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "fix_agents_table_security",
                "description": "Fix security issues preventing access to the agents table",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "disable_rls": {
                            "type": "boolean",
                            "description": "Whether to disable RLS (default: true)",
                            "default": True
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_database_schema",
                "description": "Get comprehensive database schema information",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "test_database_connection",
                "description": "Test database connection and basic operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_security_recommendations",
                "description": "Get security recommendations based on current database state",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "check_agents_endpoint",
                "description": "Check if the agents endpoint is working and diagnose issues",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "register_redis_agent",
                "description": "Register the Redis agent once security issues are fixed",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "list_prds",
                "description": "List all PRDs in the system",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with arguments"""
        try:
            if name == "check_database_security":
                return await self._check_database_security()
            elif name == "fix_agents_table_security":
                return await self._fix_agents_table_security(arguments.get("disable_rls", True))
            elif name == "get_database_schema":
                return await self._get_database_schema()
            elif name == "test_database_connection":
                return await self._test_database_connection()
            elif name == "get_security_recommendations":
                return await self._get_security_recommendations()
            elif name == "check_agents_endpoint":
                return await self._check_agents_endpoint()
            elif name == "register_redis_agent":
                return await self._register_redis_agent()
            elif name == "list_prds":
                return await self._list_prds()
            else:
                return {"error": f"Unknown tool: {name}"}
        
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    async def _check_database_security(self) -> Dict[str, Any]:
        """Check security status for all database tables"""
        if not self.supabase_manager:
            return {"error": "Supabase manager not configured"}
        
        try:
            schema_info = await self.supabase_manager.get_database_schema()
            return {
                "success": True,
                "message": "Database security check completed",
                "data": schema_info
            }
        except Exception as e:
            return {"error": f"Security check failed: {str(e)}"}
    
    async def _fix_agents_table_security(self, disable_rls: bool = True) -> Dict[str, Any]:
        """Fix security issues for the agents table"""
        if not self.supabase_manager:
            return {"error": "Supabase manager not configured"}
        
        try:
            fix_result = await self.supabase_manager.fix_table_security("agents", disable_rls)
            return {
                "success": fix_result.get("success", False),
                "message": fix_result.get("message", "Fix attempt completed"),
                "data": fix_result
            }
        except Exception as e:
            return {"error": f"Fix attempt failed: {str(e)}"}
    
    async def _get_database_schema(self) -> Dict[str, Any]:
        """Get comprehensive database schema information"""
        if not self.supabase_manager:
            return {"error": "Supabase manager not configured"}
        
        try:
            schema = await self.supabase_manager.get_database_schema()
            return {
                "success": True,
                "message": "Database schema retrieved",
                "data": schema
            }
        except Exception as e:
            return {"error": f"Schema retrieval failed: {str(e)}"}
    
    async def _test_database_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        if not self.supabase_manager:
            return {"error": "Supabase manager not configured"}
        
        try:
            connection_test = await self.supabase_manager.test_database_connection()
            return {
                "success": connection_test.get("success", False),
                "message": connection_test.get("message", "Connection test completed"),
                "data": connection_test
            }
        except Exception as e:
            return {"error": f"Connection test failed: {str(e)}"}
    
    async def _get_security_recommendations(self) -> Dict[str, Any]:
        """Get security recommendations"""
        if not self.supabase_manager:
            return {"error": "Supabase manager not configured"}
        
        try:
            recommendations = await self.supabase_manager.get_security_recommendations()
            return {
                "success": True,
                "message": "Security recommendations generated",
                "data": recommendations
            }
        except Exception as e:
            return {"error": f"Recommendations failed: {str(e)}"}
    
    async def _check_agents_endpoint(self) -> Dict[str, Any]:
        """Check if the agents endpoint is working"""
        try:
            import requests
            
            # Test the agents endpoint
            response = requests.get(
                "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents",
                timeout=10
            )
            
            if response.status_code == 200:
                agents_data = response.json()
                return {
                    "success": True,
                    "message": "Agents endpoint is working",
                    "data": {
                        "status_code": response.status_code,
                        "total_agents": agents_data.get("total", 0),
                        "agents": agents_data.get("agents", [])
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"Agents endpoint returned HTTP {response.status_code}",
                    "data": {
                        "status_code": response.status_code,
                        "response": response.text
                    }
                }
        except Exception as e:
            return {"error": f"Agents endpoint check failed: {str(e)}"}
    
    async def _register_redis_agent(self) -> Dict[str, Any]:
        """Register the Redis agent"""
        try:
            import requests
            
            # Redis agent data
            agent_data = {
                "name": "Redis Caching Layer Agent",
                "description": "High-performance caching service for Google Cloud Run with in-memory fallback",
                "purpose": "Provide fast, reliable caching operations with TTL support and comprehensive monitoring",
                "version": "2.0.0",
                "repository_url": "https://github.com/thedoctorJJ/ai-agent-factory/tree/main/agents/redis-caching-agent",
                "deployment_url": "https://redis-caching-agent-fdqqqinvyq-uc.a.run.app",
                "health_check_url": "https://redis-caching-agent-fdqqqinvyq-uc.a.run.app/health",
                "prd_id": "33b59b96-dda7-485d-97e7-dcc6b9d71d31",
                "capabilities": [
                    "cache_set", "cache_get", "cache_delete", "cache_invalidate",
                    "cache_stats", "health_monitoring", "metrics_collection"
                ],
                "configuration": {
                    "platform": "google-cloud-run",
                    "region": "us-central1",
                    "cache_type": "in-memory-fallback"
                }
            }
            
            # Register the agent
            response = requests.post(
                "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents",
                json=agent_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                agent_info = response.json()
                return {
                    "success": True,
                    "message": "Redis agent registered successfully",
                    "data": agent_info
                }
            else:
                return {
                    "success": False,
                    "message": f"Registration failed: HTTP {response.status_code}",
                    "data": {
                        "status_code": response.status_code,
                        "response": response.text
                    }
                }
        except Exception as e:
            return {"error": f"Redis agent registration failed: {str(e)}"}
    
    async def _list_prds(self) -> Dict[str, Any]:
        """List all PRDs in the system"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.execute_query("prds", "select")
            if result.get("success"):
                return {
                    "success": True,
                    "message": f"Found {len(result['data'])} PRDs",
                    "data": result["data"]
                }
            else:
                return {"error": result.get("error", "Failed to list PRDs")}
        except Exception as e:
            return {"error": f"PRD listing failed: {str(e)}"}

# MCP Server implementation
async def main():
    """Main MCP server loop"""
    server = EnhancedCursorAgentMCPServer()
    
    # This would be the actual MCP server implementation
    # For now, we'll just show the available tools
    tools = await server.list_tools()
    print("Enhanced Cursor Agent MCP Server")
    print("=" * 40)
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    asyncio.run(main())
