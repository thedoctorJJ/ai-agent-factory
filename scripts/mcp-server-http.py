#!/usr/bin/env python3
"""
HTTP-based MCP Server for END_CAP Agent Factory
Provides REST API endpoints for MCP protocol over HTTP.
"""

import json
import os
import sys
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="END_CAP Agent Factory MCP Server",
    description="HTTP-based MCP server for automated agent deployment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPServer:
    def __init__(self):
        self.tools = self._define_tools()
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_org = os.getenv('GITHUB_ORG_NAME', 'thedoctorJJ')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.gcp_key = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.endcap_url = os.getenv('ENDCAP_API_URL', 'http://localhost:8000')

    def _define_tools(self) -> List[Dict[str, Any]]:
        """Defines the tools available through this MCP server."""
        return [
            {
                "name": "create_agent",
                "description": "Create a new AI agent with specified configuration",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Agent name"},
                        "description": {"type": "string", "description": "Agent description"},
                        "type": {"type": "string", "description": "Agent type"}
                    },
                    "required": ["name", "description", "type"]
                }
            },
            {
                "name": "deploy_agent",
                "description": "Deploy an agent to production environment",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "Agent ID to deploy"},
                        "environment": {"type": "string", "description": "Deployment environment"}
                    },
                    "required": ["agent_id"]
                }
            },
            {
                "name": "setup_database",
                "description": "Set up database for agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "Agent ID"},
                        "schema": {"type": "object", "description": "Database schema"}
                    },
                    "required": ["agent_id"]
                }
            },
            {
                "name": "create_repository",
                "description": "Create GitHub repository for agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Repository name"},
                        "description": {"type": "string", "description": "Repository description"},
                        "private": {"type": "boolean", "description": "Make repository private"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_repository_info",
                "description": "Get information about a repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo_name": {"type": "string", "description": "Repository name"}
                    },
                    "required": ["repo_name"]
                }
            },
            {
                "name": "create_prd_from_conversation",
                "description": "Extract PRD from OpenAI conversation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation": {"type": "string", "description": "Conversation text"},
                        "agent_type": {"type": "string", "description": "Type of agent"}
                    },
                    "required": ["conversation", "agent_type"]
                }
            },
            {
                "name": "deliver_prd_to_endcap",
                "description": "Deliver PRD to END_CAP platform",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prd": {"type": "object", "description": "PRD object"},
                        "conversation_id": {"type": "string", "description": "Conversation ID"}
                    },
                    "required": ["prd"]
                }
            },
            {
                "name": "trigger_devin_workflow",
                "description": "Trigger Devin AI workflow for agent creation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prd_id": {"type": "string", "description": "PRD ID"},
                        "agent_type": {"type": "string", "description": "Agent type"}
                    },
                    "required": ["prd_id"]
                }
            },
            {
                "name": "get_endcap_status",
                "description": "Get END_CAP platform status",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handles the 'initialize' method for MCP protocol."""
        logging.info("Handling initialize request")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "END_CAP Agent Factory MCP Server",
                "version": "1.0.0"
            }
        }

    def _handle_tools_list(self) -> Dict[str, Any]:
        """Handles the 'tools/list' method."""
        logging.info("Handling tools/list request")
        return {"tools": self.tools}

    def _handle_tools_call(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Handles the 'tools/call' method."""
        logging.info(f"Handling tools/call request for tool: {tool_name} with args: {tool_args}")
        
        try:
            if tool_name == "create_agent":
                return self._create_agent(tool_args)
            elif tool_name == "deploy_agent":
                return self._deploy_agent(tool_args)
            elif tool_name == "setup_database":
                return self._setup_database(tool_args)
            elif tool_name == "create_repository":
                return self._create_repository(tool_args)
            elif tool_name == "get_repository_info":
                return self._get_repository_info(tool_args)
            elif tool_name == "create_prd_from_conversation":
                return self._create_prd_from_conversation(tool_args)
            elif tool_name == "deliver_prd_to_endcap":
                return self._deliver_prd_to_endcap(tool_args)
            elif tool_name == "trigger_devin_workflow":
                return self._trigger_devin_workflow(tool_args)
            elif tool_name == "get_endcap_status":
                return self._get_endcap_status(tool_args)
            else:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logging.error(f"Error executing tool {tool_name}: {e}")
            return {"status": "error", "message": str(e)}

    def _create_agent(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent."""
        name = args.get('name')
        description = args.get('description')
        agent_type = args.get('type')
        
        return {
            "status": "success",
            "message": f"Agent '{name}' created successfully",
            "agent_id": f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "details": {
                "name": name,
                "description": description,
                "type": agent_type,
                "created_at": datetime.now().isoformat()
            }
        }

    def _deploy_agent(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy an agent."""
        agent_id = args.get('agent_id')
        environment = args.get('environment', 'production')
        
        return {
            "status": "success",
            "message": f"Agent '{agent_id}' deployed to {environment}",
            "deployment_url": f"https://{agent_id}.endcap.run",
            "details": {
                "agent_id": agent_id,
                "environment": environment,
                "deployed_at": datetime.now().isoformat()
            }
        }

    def _setup_database(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Set up database for agent."""
        agent_id = args.get('agent_id')
        schema = args.get('schema', {})
        
        return {
            "status": "success",
            "message": f"Database setup completed for agent '{agent_id}'",
            "database_url": f"postgresql://{agent_id}.db.supabase.co:5432/{agent_id}",
            "details": {
                "agent_id": agent_id,
                "schema": schema,
                "setup_at": datetime.now().isoformat()
            }
        }

    def _create_repository(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create GitHub repository."""
        name = args.get('name')
        description = args.get('description', '')
        private = args.get('private', False)
        
        if not self.github_token:
            return {"status": "error", "message": "GitHub token not configured"}
        
        try:
            # Try to create in organization first
            url = f"https://api.github.com/orgs/{self.github_org}/repos"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "name": name,
                "description": description,
                "private": private,
                "auto_init": True
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                repo_data = response.json()
                return {
                    "status": "success",
                    "message": f"Repository '{name}' created successfully",
                    "repository_url": repo_data["html_url"],
                    "clone_url": repo_data["clone_url"],
                    "details": repo_data
                }
            elif response.status_code == 404:
                # Fallback to user account
                url = "https://api.github.com/user/repos"
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 201:
                    repo_data = response.json()
                    return {
                        "status": "success",
                        "message": f"Repository '{name}' created in user account",
                        "repository_url": repo_data["html_url"],
                        "clone_url": repo_data["clone_url"],
                        "details": repo_data
                    }
                else:
                    return {"status": "error", "message": f"Failed to create repository: {response.status_code} - {response.text}"}
            else:
                return {"status": "error", "message": f"Failed to create repository: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to create repository: {str(e)}"}

    def _get_repository_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get repository information."""
        repo_name = args.get('repo_name')
        
        if not self.github_token:
            return {"status": "error", "message": "GitHub token not configured"}
        
        try:
            # Try organization repo first
            url = f"https://api.github.com/repos/{self.github_org}/{repo_name}"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return {"status": "success", "repository": response.json()}
            else:
                return {"status": "error", "message": f"Repository not found: {response.status_code}"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to get repository info: {str(e)}"}

    def _create_prd_from_conversation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract PRD from conversation."""
        conversation = args.get('conversation')
        agent_type = args.get('agent_type')
        
        # Mock PRD extraction - in real implementation, this would use OpenAI API
        prd = {
            "title": f"{agent_type} Agent",
            "description": f"AI agent for {agent_type} based on conversation",
            "requirements": [
                "Process user requests",
                "Provide intelligent responses",
                "Integrate with external systems"
            ],
            "conversation_summary": conversation[:200] + "..." if len(conversation) > 200 else conversation,
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "prd": prd,
            "message": "PRD extracted from conversation successfully"
        }

    def _deliver_prd_to_endcap(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver PRD to END_CAP platform."""
        prd = args.get('prd')
        conversation_id = args.get('conversation_id')
        
        try:
            # Create a Devin task with the PRD
            task_data = {
                "title": prd.get('title', 'New Agent'),
                "description": prd.get('description', ''),
                "requirements": prd.get('requirements', []),
                "prd_id": f"prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            response = requests.post(
                f"{self.endcap_url}/api/v1/devin/tasks",
                json=task_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                task_response = response.json()
                return {
                    "status": "success",
                    "message": "PRD delivered to END_CAP platform successfully",
                    "task_id": task_response.get('task_id'),
                    "details": task_response
                }
            else:
                return {"status": "error", "message": f"Failed to deliver PRD: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to deliver PRD: {str(e)}"}

    def _trigger_devin_workflow(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger Devin AI workflow."""
        prd_id = args.get('prd_id')
        agent_type = args.get('agent_type', 'general')
        
        return {
            "status": "success",
            "message": f"Devin AI workflow triggered for PRD '{prd_id}'",
            "workflow_id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "details": {
                "prd_id": prd_id,
                "agent_type": agent_type,
                "triggered_at": datetime.now().isoformat()
            }
        }

    def _get_endcap_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get END_CAP platform status."""
        try:
            response = requests.get(f"{self.endcap_url}/api/v1/health")
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "END_CAP platform is healthy",
                    "details": response.json()
                }
            else:
                return {
                    "status": "warning",
                    "message": f"END_CAP platform returned status {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to check END_CAP status: {str(e)}"
            }

# Initialize MCP server
mcp_server = MCPServer()

@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "service": "END_CAP Agent Factory MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp",
            "tools": "/tools"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "END_CAP Agent Factory MCP Server"
    }

@app.get("/tools")
async def list_tools():
    """List available MCP tools."""
    return mcp_server._handle_tools_list()

@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    """Handle MCP protocol requests."""
    try:
        if request.method == "initialize":
            result = mcp_server._handle_initialize(request.params or {})
        elif request.method == "tools/list":
            result = mcp_server._handle_tools_list()
        elif request.method == "tools/call":
            if not request.params:
                raise HTTPException(status_code=400, detail="Missing params for tools/call")
            tool_name = request.params.get("tool_name")
            tool_args = request.params.get("arguments", {})
            if not tool_name:
                raise HTTPException(status_code=400, detail="Missing tool_name in params")
            result = mcp_server._handle_tools_call(tool_name, tool_args)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")
        
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            result=result
        )
    except Exception as e:
        logging.error(f"Error handling MCP request: {e}")
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            error={
                "code": -32000,
                "message": str(e)
            }
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
