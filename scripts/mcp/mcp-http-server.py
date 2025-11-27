#!/usr/bin/env python3
"""
HTTP wrapper for MCP Servers
Allows external applications (ChatGPT, Devin, etc.) to communicate with MCP servers via HTTP
"""

import json
import asyncio
import logging
from fastapi import FastAPI, HTTPException
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

# Import Devin MCP Server
spec = importlib.util.spec_from_file_location("devin_mcp_server", os.path.join(current_dir, "devin-mcp-server.py"))
devin_mcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(devin_mcp_server)
DevinMCPServer = devin_mcp_server.DevinMCPServer

# Import Cursor MCP Server for PRD submission
spec_cursor = importlib.util.spec_from_file_location("cursor_mcp_server", os.path.join(current_dir, "cursor-agent-mcp-server.py"))
cursor_mcp_server = importlib.util.module_from_spec(spec_cursor)
spec_cursor.loader.exec_module(cursor_mcp_server)
CursorAgentMCPServer = cursor_mcp_server.CursorAgentMCPServer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP HTTP Server", version="1.0.0")

# Initialize both MCP servers
devin_mcp_server = DevinMCPServer()
cursor_mcp_server = CursorAgentMCPServer()

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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "mcp-http-server",
        "endpoints": {
            "prd_webhook": "/api/v1/prds/incoming",
            "webhook_status": "/webhook/status",
            "mcp_tools": "/mcp/tools",
            "devin_cache": "/mcp/cache/status"
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
        
        # Call the Devin MCP server
        response = await devin_mcp_server.handle_request(mcp_request)
        
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
        
        response = await devin_mcp_server.handle_request(request)
        
        if response and "result" in response:
            return response["result"]
        else:
            return {"tools": []}
            
    except Exception as e:
        logger.error(f"Error listing MCP tools: {e}")
        return {"tools": [], "error": str(e)}

@app.get("/mcp/cache/status")
async def get_cache_status():
    """Get the status of the MCP server cache"""
    return {
        "prd_cache_size": len(devin_mcp_server._prd_cache),
        "agent_library_cache_size": len(devin_mcp_server._agent_library_cache),
        "cached_prds": list(devin_mcp_server._prd_cache.keys())
    }

@app.delete("/mcp/cache/clear")
async def clear_cache():
    """Clear the MCP server cache"""
    devin_mcp_server._prd_cache.clear()
    devin_mcp_server._agent_library_cache.clear()
    return {"message": "Cache cleared successfully"}

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
        result = await cursor_mcp_server._submit_prd_from_conversation({
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
