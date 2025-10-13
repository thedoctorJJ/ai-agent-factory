#!/usr/bin/env python3
"""
HTTP wrapper for the Devin MCP Server
Allows our application to communicate with the MCP server via HTTP
"""

import json
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

import importlib.util
import sys
import os

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the module with hyphen in filename
spec = importlib.util.spec_from_file_location("devin_mcp_server", os.path.join(current_dir, "devin-mcp-server.py"))
devin_mcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(devin_mcp_server)
DevinMCPServer = devin_mcp_server.DevinMCPServer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Devin MCP HTTP Server", version="1.0.0")

# Initialize the MCP server
mcp_server = DevinMCPServer()

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
    return {"status": "healthy", "service": "devin-mcp-http-server"}

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
        
        # Call the MCP server
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

@app.get("/mcp/cache/status")
async def get_cache_status():
    """Get the status of the MCP server cache"""
    return {
        "prd_cache_size": len(mcp_server._prd_cache),
        "agent_library_cache_size": len(mcp_server._agent_library_cache),
        "cached_prds": list(mcp_server._prd_cache.keys())
    }

@app.delete("/mcp/cache/clear")
async def clear_cache():
    """Clear the MCP server cache"""
    mcp_server._prd_cache.clear()
    mcp_server._agent_library_cache.clear()
    return {"message": "Cache cleared successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
