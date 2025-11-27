#!/usr/bin/env python3
"""
HTTP wrapper for MCP Servers
Allows external applications (ChatGPT, Devin, etc.) to communicate with MCP servers via HTTP
"""

import json
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import aiohttp

import importlib.util
import sys
import os
from pathlib import Path

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = Path(current_dir).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, current_dir)

# Import Cursor Agent MCP Server (primary server for all tools)
spec_cursor = importlib.util.spec_from_file_location("cursor_mcp_server", os.path.join(current_dir, "cursor-agent-mcp-server.py"))
cursor_mcp_server = importlib.util.module_from_spec(spec_cursor)
spec_cursor.loader.exec_module(cursor_mcp_server)
CursorAgentMCPServer = cursor_mcp_server.CursorAgentMCPServer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP HTTP Server", version="1.0.0")

# Initialize Cursor Agent MCP Server
mcp_server = CursorAgentMCPServer()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Dict[str, Any] = {}
    error: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    """Root endpoint for MCP server discovery"""
    tools = await mcp_server.list_tools()
    return {
        "name": "AI Agent Factory MCP Server",
        "version": "1.0.0",
        "protocol": "mcp",
        "capabilities": {
            "tools": len(tools)
        },
        "endpoints": {
            "tools": "/mcp/tools",
            "call": "/mcp/call",
            "health": "/health"
        }
    }

@app.post("/")
async def mcp_endpoint(request: Request):
    """
    MCP protocol endpoint for ChatGPT
    Handles MCP requests and returns JSON responses
    """
    try:
        body = await request.json()
        method = body.get("method")
        msg_id = body.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "AI Agent Factory MCP Server",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            tools = await mcp_server.list_tools()
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": tools}
            }
            
        elif method == "tools/call":
            params = body.get("params", {})
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            result = await mcp_server.call_tool(tool_name, tool_args)
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            
    except Exception as e:
        logger.error(f"Error in MCP endpoint: {e}")
        return {
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in locals() else None,
            "error": {"code": -32603, "message": str(e)}
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "mcp-http-server",
        "mcp_server": "cursor-agent-mcp-server",
        "endpoints": {
            "prd_webhook": "/api/v1/prds/incoming",
            "webhook_status": "/webhook/status",
            "mcp_tools": "/mcp/tools"
        }
    }

@app.post("/mcp/call", response_model=MCPResponse)
async def call_mcp_tool(request: MCPRequest):
    """Call an MCP tool"""
    try:
        # Convert the request to the format expected by the MCP server
        mcp_request = {
            "jsonrpc": request.jsonrpc,
            "id": request.id,
            "method": request.method,
            "params": request.params
        }
        
        # Call the Cursor Agent MCP server
        response = await mcp_server.handle_request(mcp_request)
        
        if response:
            return MCPResponse(
                jsonrpc=response.get("jsonrpc", "2.0"),
                id=response.get("id", request.id),
                result=response.get("result", {}),
                error=response.get("error")
            )
        else:
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                result={}
            )
            
    except Exception as e:
        logger.error(f"Error calling MCP tool: {e}")
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            error={
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        )

@app.get("/mcp/tools")
async def list_mcp_tools():
    """List available MCP tools"""
    try:
        # Create a tools/list request
        request = {
            "jsonrpc": "2.0",
            "id": "list_tools",
            "method": "tools/list"
        }
        
        response = await mcp_server.handle_request(request)
        
        if response and "result" in response:
            return response["result"]
        else:
            return {"tools": []}
            
    except Exception as e:
        logger.error(f"Error listing MCP tools: {e}")
        return {"tools": [], "error": str(e)}

@app.get("/mcp/status")
async def get_mcp_status():
    """Get the status of the MCP server"""
    return {
        "server": "cursor-agent-mcp-server",
        "status": "operational",
        "services": {
            "supabase": bool(mcp_server.supabase_service),
            "github": bool(mcp_server.github_service),
            "openai": bool(mcp_server.openai_service),
            "google_cloud": bool(mcp_server.gcp_deployer)
        }
    }

# Webhook endpoint - receives PRDs from external sources (ChatGPT, webhooks, etc.) and forwards to agent factory
class PRDWebhookRequest(BaseModel):
    """Request model for PRD submission via webhook"""
    content: str

@app.post("/api/v1/prds/incoming")
async def submit_prd_via_mcp(request: PRDWebhookRequest):
    """
    Receive PRD from external sources (ChatGPT, webhooks, etc.) and forward to agent factory via MCP server.
    This endpoint allows any external service to submit PRDs through the MCP server.
    
    The MCP server handles delivery to the agent factory backend, ensuring proper processing and storage.
    """
    try:
        logger.info(f"Received PRD via MCP webhook: {len(request.content)} characters")
        
        # Use the Cursor MCP server's submit_prd_from_conversation tool
        result = await mcp_server._submit_prd_from_conversation({
            "prd_markdown": request.content,
            "conversation_content": request.content
        })
        
        if "error" in result:
            logger.error(f"Error submitting PRD: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info(f"PRD submitted successfully: {result.get('prd_id')}")
        return result.get("prd", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error submitting PRD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit PRD: {str(e)}")

@app.get("/webhook/status")
async def webhook_status():
    """Status endpoint for PRD webhook integration"""
    return {
        "status": "ready",
        "service": "mcp-http-server",
        "endpoint": "/api/v1/prds/incoming",
        "description": "PRD webhook endpoint via MCP server - accepts PRDs from external sources and delivers to agent factory",
        "method": "POST",
        "content_type": "application/json",
        "request_format": {
            "content": "string (PRD content in markdown format)"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
