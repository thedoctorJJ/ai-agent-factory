#!/usr/bin/env python3
"""
Cursor Agent MCP Server for AI Agent Factory
Provides comprehensive access to all platform components for Cursor Agent
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.fastapi_app.config import Config
# Import GoogleCloudRunDeployer dynamically to handle hyphenated filename
import importlib.util
spec = importlib.util.spec_from_file_location("google_cloud_run_deploy", str(project_root / "scripts" / "mcp" / "google-cloud-run-deploy.py"))
google_cloud_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(google_cloud_module)
GoogleCloudRunDeployer = google_cloud_module.GoogleCloudRunDeployer
from scripts.mcp.simple_services import SimpleSupabaseService, SimpleGitHubService, SimpleOpenAIService, SimpleDatabaseService

class CursorAgentMCPServer:
    """MCP Server for Cursor Agent integration with AI Agent Factory"""
    
    def __init__(self):
        self.config = Config()
        self.supabase_service = None
        self.github_service = None
        self.openai_service = None
        self.gcp_deployer = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all platform services"""
        try:
            # Initialize Supabase
            if self.config.supabase_url and self.config.supabase_service_role_key:
                self.supabase_service = SimpleSupabaseService(
                    self.config.supabase_url,
                    self.config.supabase_service_role_key
                )
            
            # Initialize GitHub
            if self.config.github_token:
                self.github_service = SimpleGitHubService(self.config.github_token)
            
            # Initialize OpenAI
            if self.config.openai_api_key:
                self.openai_service = SimpleOpenAIService(self.config.openai_api_key)
            
            # Initialize Database
            if self.config.database_url:
                self.database_service = SimpleDatabaseService(self.config.database_url)
            
            # Initialize Google Cloud Run Deployer
            if self.config.google_cloud_project_id:
                service_account_path = os.path.join(
                    project_root, 
                    "config", 
                    "google-cloud-service-account.json"
                )
                if os.path.exists(service_account_path):
                    self.gcp_deployer = GoogleCloudRunDeployer(
                        self.config.google_cloud_project_id,
                        service_account_path
                    )
        
        except Exception as e:
            print(f"Warning: Failed to initialize some services: {e}", file=sys.stderr)
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools for Cursor Agent"""
        return [
            {
                "name": "get_platform_status",
                "description": "Get comprehensive status of all platform components",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "list_prds",
                "description": "List all PRDs in the system with their status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by status (queue, in-progress, completed, failed)",
                            "enum": ["queue", "in-progress", "completed", "failed"]
                        }
                    }
                }
            },
            {
                "name": "get_prd_details",
                "description": "Get detailed information about a specific PRD",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prd_id": {
                            "type": "string",
                            "description": "The ID of the PRD to retrieve"
                        }
                    },
                    "required": ["prd_id"]
                }
            },
            {
                "name": "create_prd",
                "description": "Create a new PRD in the system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "PRD title"},
                        "description": {"type": "string", "description": "PRD description"},
                        "requirements": {"type": "array", "items": {"type": "string"}, "description": "List of requirements"},
                        "content": {"type": "string", "description": "Full PRD content in markdown"}
                    },
                    "required": ["title", "content"]
                }
            },
            {
                "name": "update_prd_status",
                "description": "Update the status of a PRD",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prd_id": {"type": "string", "description": "PRD ID"},
                        "status": {
                            "type": "string",
                            "enum": ["queue", "in-progress", "completed", "failed"],
                            "description": "New status"
                        }
                    },
                    "required": ["prd_id", "status"]
                }
            },
            {
                "name": "list_agents",
                "description": "List all agents in the system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by agent status",
                            "enum": ["pending", "building", "deployed", "failed"]
                        }
                    }
                }
            },
            {
                "name": "get_agent_details",
                "description": "Get detailed information about a specific agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "Agent ID"}
                    },
                    "required": ["agent_id"]
                }
            },
            {
                "name": "deploy_agent",
                "description": "Deploy an agent to Google Cloud Run",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Name for the agent"},
                        "agent_code": {"type": "string", "description": "Python FastAPI code"},
                        "requirements": {"type": "array", "items": {"type": "string"}, "description": "Python dependencies"},
                        "environment_variables": {"type": "object", "description": "Environment variables"}
                    },
                    "required": ["agent_name", "agent_code"]
                }
            },
            {
                "name": "create_github_repo",
                "description": "Create a new GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Repository name"},
                        "description": {"type": "string", "description": "Repository description"},
                        "private": {"type": "boolean", "description": "Make repository private", "default": False}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_github_repo",
                "description": "Get information about a GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string", "description": "Repository owner"},
                        "repo": {"type": "string", "description": "Repository name"}
                    },
                    "required": ["owner", "repo"]
                }
            },
            {
                "name": "test_database_connection",
                "description": "Test the database connection",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_database_schema",
                "description": "Get the current database schema",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "validate_environment",
                "description": "Validate all environment configuration",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "start_backend_server",
                "description": "Start the backend API server",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "port": {"type": "integer", "description": "Port to run on", "default": 8000}
                    }
                }
            },
            {
                "name": "start_frontend_server",
                "description": "Start the frontend development server",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "port": {"type": "integer", "description": "Port to run on", "default": 3000}
                    }
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return results"""
        try:
            if name == "get_platform_status":
                return await self._get_platform_status()
            elif name == "list_prds":
                return await self._list_prds(arguments.get("status"))
            elif name == "get_prd_details":
                return await self._get_prd_details(arguments["prd_id"])
            elif name == "create_prd":
                return await self._create_prd(arguments)
            elif name == "update_prd_status":
                return await self._update_prd_status(arguments["prd_id"], arguments["status"])
            elif name == "list_agents":
                return await self._list_agents(arguments.get("status"))
            elif name == "get_agent_details":
                return await self._get_agent_details(arguments["agent_id"])
            elif name == "deploy_agent":
                return await self._deploy_agent(arguments)
            elif name == "create_github_repo":
                return await self._create_github_repo(arguments)
            elif name == "get_github_repo":
                return await self._get_github_repo(arguments["owner"], arguments["repo"])
            elif name == "test_database_connection":
                return await self._test_database_connection()
            elif name == "get_database_schema":
                return await self._get_database_schema()
            elif name == "validate_environment":
                return await self._validate_environment()
            elif name == "start_backend_server":
                return await self._start_backend_server(arguments.get("port", 8000))
            elif name == "start_frontend_server":
                return await self._start_frontend_server(arguments.get("port", 3000))
            else:
                return {"error": f"Unknown tool: {name}"}
        
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    async def _get_platform_status(self) -> Dict[str, Any]:
        """Get comprehensive platform status"""
        status = {
            "timestamp": asyncio.get_event_loop().time(),
            "services": {},
            "configuration": {}
        }
        
        # Check Supabase
        if self.supabase_service:
            try:
                # Test connection
                result = await self.supabase_service.execute_query("agents", "select")
                if result.get("success"):
                    status["services"]["supabase"] = {"status": "connected", "tables_accessible": True}
                else:
                    status["services"]["supabase"] = {"status": "error", "error": result.get("error", "Unknown error")}
            except Exception as e:
                status["services"]["supabase"] = {"status": "error", "error": str(e)}
        else:
            status["services"]["supabase"] = {"status": "not_configured"}
        
        # Check GitHub
        if self.github_service:
            try:
                # Test connection
                user = await self.github_service.get_user()
                if "error" not in user:
                    status["services"]["github"] = {"status": "connected", "user": user.get("login", "unknown")}
                else:
                    status["services"]["github"] = {"status": "error", "error": user.get("error", "Unknown error")}
            except Exception as e:
                status["services"]["github"] = {"status": "error", "error": str(e)}
        else:
            status["services"]["github"] = {"status": "not_configured"}
        
        # Check OpenAI
        if self.openai_service:
            try:
                result = await self.openai_service.test_connection()
                if result.get("success"):
                    status["services"]["openai"] = {"status": "connected"}
                else:
                    status["services"]["openai"] = {"status": "error", "error": result.get("error", "Unknown error")}
            except Exception as e:
                status["services"]["openai"] = {"status": "error", "error": str(e)}
        else:
            status["services"]["openai"] = {"status": "not_configured"}
        
        # Check Google Cloud
        if self.gcp_deployer:
            status["services"]["google_cloud"] = {"status": "configured", "project_id": self.config.google_cloud_project_id}
        else:
            status["services"]["google_cloud"] = {"status": "not_configured"}
        
        # Configuration status
        status["configuration"] = {
            "environment": self.config.environment,
            "debug": self.config.debug,
            "database_configured": bool(self.config.database_url),
            "supabase_configured": bool(self.config.supabase_url and self.config.supabase_key),
            "github_configured": bool(self.config.github_token),
            "openai_configured": bool(self.config.openai_api_key),
            "gcp_configured": bool(self.config.google_cloud_project_id)
        }
        
        return status
    
    async def _list_prds(self, status_filter: Optional[str] = None) -> Dict[str, Any]:
        """List PRDs with optional status filter"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.execute_query("prds", "select")
            if result.get("success"):
                prds = result.get("data", [])
                if status_filter:
                    prds = [prd for prd in prds if prd.get("status") == status_filter]
                return {"prds": prds, "count": len(prds)}
            else:
                return {"error": f"Failed to list PRDs: {result.get('error', 'Unknown error')}"}
        except Exception as e:
            return {"error": f"Failed to list PRDs: {str(e)}"}
    
    async def _get_prd_details(self, prd_id: str) -> Dict[str, Any]:
        """Get detailed PRD information"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.client.table("prds").select("*").eq("id", prd_id).execute()
            if result.data:
                return {"prd": result.data[0]}
            else:
                return {"error": f"PRD with ID {prd_id} not found"}
        except Exception as e:
            return {"error": f"Failed to get PRD details: {str(e)}"}
    
    async def _create_prd(self, prd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new PRD"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.client.table("prds").insert(prd_data).execute()
            return {"prd": result.data[0], "message": "PRD created successfully"}
        except Exception as e:
            return {"error": f"Failed to create PRD: {str(e)}"}
    
    async def _update_prd_status(self, prd_id: str, status: str) -> Dict[str, Any]:
        """Update PRD status"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.client.table("prds").update({"status": status}).eq("id", prd_id).execute()
            return {"message": f"PRD {prd_id} status updated to {status}"}
        except Exception as e:
            return {"error": f"Failed to update PRD status: {str(e)}"}
    
    async def _list_agents(self, status_filter: Optional[str] = None) -> Dict[str, Any]:
        """List agents with optional status filter"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            query = self.supabase_service.client.table("agents").select("*")
            if status_filter:
                query = query.eq("status", status_filter)
            
            result = await query.execute()
            return {"agents": result.data, "count": len(result.data)}
        except Exception as e:
            return {"error": f"Failed to list agents: {str(e)}"}
    
    async def _get_agent_details(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed agent information"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            result = await self.supabase_service.client.table("agents").select("*").eq("id", agent_id).execute()
            if result.data:
                return {"agent": result.data[0]}
            else:
                return {"error": f"Agent with ID {agent_id} not found"}
        except Exception as e:
            return {"error": f"Failed to get agent details: {str(e)}"}
    
    async def _deploy_agent(self, deployment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy an agent to Google Cloud Run"""
        if not self.gcp_deployer:
            return {"error": "Google Cloud Run deployer not configured"}
        
        try:
            result = self.gcp_deployer.build_and_deploy(
                agent_name=deployment_data["agent_name"],
                agent_code=deployment_data["agent_code"],
                requirements=deployment_data.get("requirements", []),
                environment_variables=deployment_data.get("environment_variables", {})
            )
            return result
        except Exception as e:
            return {"error": f"Failed to deploy agent: {str(e)}"}
    
    async def _create_github_repo(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GitHub repository"""
        if not self.github_service:
            return {"error": "GitHub service not configured"}
        
        try:
            result = await self.github_service.create_repository(
                name=repo_data["name"],
                description=repo_data.get("description", ""),
                private=repo_data.get("private", False)
            )
            return {"repository": result, "message": "Repository created successfully"}
        except Exception as e:
            return {"error": f"Failed to create repository: {str(e)}"}
    
    async def _get_github_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get GitHub repository information"""
        if not self.github_service:
            return {"error": "GitHub service not configured"}
        
        try:
            result = await self.github_service.get_repository(owner, repo)
            return {"repository": result}
        except Exception as e:
            return {"error": f"Failed to get repository: {str(e)}"}
    
    async def _test_database_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        if self.database_service:
            return await self.database_service.test_connection()
        elif self.supabase_service:
            try:
                result = await self.supabase_service.execute_query("agents", "select")
                if result.get("success"):
                    return {"status": "connected", "message": "Database connection successful"}
                else:
                    return {"error": f"Database connection failed: {result.get('error', 'Unknown error')}"}
            except Exception as e:
                return {"error": f"Database connection failed: {str(e)}"}
        else:
            return {"error": "No database service configured"}
    
    async def _get_database_schema(self) -> Dict[str, Any]:
        """Get database schema information"""
        if not self.supabase_service:
            return {"error": "Supabase service not configured"}
        
        try:
            # Get table information
            tables = ["agents", "prds", "agent_executions"]
            schema = {}
            
            for table in tables:
                try:
                    result = await self.supabase_service.client.table(table).select("*").limit(1).execute()
                    schema[table] = {"exists": True, "sample_data": result.data[0] if result.data else None}
                except Exception as e:
                    schema[table] = {"exists": False, "error": str(e)}
            
            return {"schema": schema}
        except Exception as e:
            return {"error": f"Failed to get database schema: {str(e)}"}
    
    async def _validate_environment(self) -> Dict[str, Any]:
        """Validate environment configuration"""
        validation = {
            "database": {
                "configured": bool(self.config.database_url),
                "url": self.config.database_url[:20] + "..." if self.config.database_url else None
            },
            "supabase": {
                "configured": bool(self.config.supabase_url and self.config.supabase_key),
                "url": self.config.supabase_url[:20] + "..." if self.config.supabase_url else None
            },
            "github": {
                "configured": bool(self.config.github_token),
                "token_length": len(self.config.github_token) if self.config.github_token else 0
            },
            "openai": {
                "configured": bool(self.config.openai_api_key),
                "key_length": len(self.config.openai_api_key) if self.config.openai_api_key else 0
            },
            "google_cloud": {
                "configured": bool(self.config.google_cloud_project_id),
                "project_id": self.config.google_cloud_project_id
            }
        }
        
        return validation
    
    async def _start_backend_server(self, port: int) -> Dict[str, Any]:
        """Start the backend server"""
        import subprocess
        import os
        
        try:
            # Change to project root
            os.chdir(project_root)
            
            # Start the backend server
            process = subprocess.Popen([
                "python", "-m", "uvicorn", 
                "backend.fastapi_app.main:app", 
                "--host", "0.0.0.0", 
                "--port", str(port),
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return {
                "message": f"Backend server starting on port {port}",
                "pid": process.pid,
                "url": f"http://localhost:{port}"
            }
        except Exception as e:
            return {"error": f"Failed to start backend server: {str(e)}"}
    
    async def _start_frontend_server(self, port: int) -> Dict[str, Any]:
        """Start the frontend server"""
        import subprocess
        import os
        
        try:
            # Change to frontend directory
            frontend_dir = project_root / "frontend" / "next-app"
            os.chdir(frontend_dir)
            
            # Start the frontend server
            process = subprocess.Popen([
                "npm", "run", "dev", "--", "--port", str(port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return {
                "message": f"Frontend server starting on port {port}",
                "pid": process.pid,
                "url": f"http://localhost:{port}"
            }
        except Exception as e:
            return {"error": f"Failed to start frontend server: {str(e)}"}

async def main():
    """Main MCP server loop"""
    server = CursorAgentMCPServer()
    
    # Handle MCP protocol messages
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            message = json.loads(line.strip())
            
            if message.get("method") == "tools/list":
                tools = await server.list_tools()
                response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {"tools": tools}
                }
            elif message.get("method") == "tools/call":
                result = await server.call_tool(
                    message["params"]["name"],
                    message["params"].get("arguments", {})
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
        
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id") if 'message' in locals() else None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
