"""
MCP Integration Router
Handles communication between our application and the MCP server
"""

import requests
import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoadPRDRequest(BaseModel):
    prd_id: str

class MCPResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] = {}

@router.post("/mcp/load-prd", response_model=MCPResponse)
async def load_prd_to_mcp(request: LoadPRDRequest):
    """Load PRD data into the MCP server cache"""
    try:
        # Get the MCP server URL from environment
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8001')
        
        # First, get the PRD data from our database
        prd_response = requests.get(f"http://localhost:8000/api/v1/prds/{request.prd_id}")
        if prd_response.status_code != 200:
            raise HTTPException(
                status_code=404, 
                detail=f"PRD not found: {request.prd_id}"
            )
        
        prd_data = prd_response.json()
        
        # Send the PRD data to the MCP server
        mcp_request = {
            "jsonrpc": "2.0",
            "id": "load_prd_request",
            "method": "tools/call",
            "params": {
                "name": "load_prd_data",
                "arguments": {
                    "prd_id": request.prd_id
                }
            }
        }
        
        # Call the MCP server
        mcp_response = requests.post(
            f"{mcp_server_url}/mcp/call",
            json=mcp_request,
            headers={"Content-Type": "application/json"}
        )
        
        if mcp_response.status_code == 200:
            mcp_result = mcp_response.json()
            return MCPResponse(
                success=True,
                message=f"PRD '{prd_data.get('title', 'Unknown')}' loaded into MCP server cache",
                data={
                    "prd_id": request.prd_id,
                    "prd_title": prd_data.get('title'),
                    "mcp_response": mcp_result
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load PRD into MCP server: {mcp_response.status_code}"
            )
            
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="MCP server is not available. Please ensure it's running."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading PRD to MCP: {str(e)}"
        )

@router.get("/mcp/status")
async def get_mcp_status():
    """Get the status of the MCP server"""
    try:
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8001')
        
        # Try to ping the MCP server
        response = requests.get(f"{mcp_server_url}/health", timeout=5)
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "MCP server is running",
                "url": mcp_server_url
            }
        else:
            return {
                "success": False,
                "message": f"MCP server responded with status {response.status_code}",
                "url": mcp_server_url
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "MCP server is not available",
            "url": mcp_server_url if 'mcp_server_url' in locals() else "unknown"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking MCP server: {str(e)}",
            "url": mcp_server_url if 'mcp_server_url' in locals() else "unknown"
        }
