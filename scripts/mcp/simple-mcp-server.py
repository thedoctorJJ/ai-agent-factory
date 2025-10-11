#!/usr/bin/env python3
"""
Simple MCP Server for testing ChatGPT integration
"""

import json
import sys
import os
import requests
from typing import Dict, Any

class SimpleMCPServer:
    def __init__(self):
        self.endcap_api_url = "http://localhost:8000"
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            method = request.get("method")
            
            if method == "get_endcap_status":
                return self.get_endcap_status()
            elif method == "get_prd_template":
                return self.get_prd_template()
            elif method == "create_prd_from_chatgpt":
                return self.create_prd_from_chatgpt(request.get("params", {}))
            else:
                return {
                    "error": f"Unknown method: {method}",
                    "available_methods": ["get_endcap_status", "get_prd_template", "create_prd_from_chatgpt"]
                }
        except Exception as e:
            return {"error": str(e)}
    
    def get_endcap_status(self) -> Dict[str, Any]:
        """Check if AI Agent Factory is running"""
        try:
            response = requests.get(f'{self.endcap_api_url}/api/v1/health', timeout=5)
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "healthy",
                    "message": "AI Agent Factory Agent Factory is running and ready"
                }
            else:
                return {"error": f"AI Agent Factory returned status {response.status_code}"}
        except Exception as e:
            return {"error": f"Failed to connect to AI Agent Factory: {str(e)}"}
    
    def get_prd_template(self) -> Dict[str, Any]:
        """Get PRD template"""
        try:
            response = requests.get(f'{self.endcap_api_url}/api/v1/prds/schema', timeout=5)
            if response.status_code == 200:
                schema = response.json()
                return {
                    "success": True,
                    "prd_template": {
                        "required_sections": ["title", "description", "problem_statement", "target_users", "requirements"],
                        "guidance": "Use this template to structure your PRD"
                    },
                    "message": "PRD template retrieved successfully"
                }
            else:
                return {"error": f"Failed to get template: {response.status_code}"}
        except Exception as e:
            return {"error": f"Failed to get template: {str(e)}"}
    
    def create_prd_from_chatgpt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create PRD in AI Agent Factory"""
        try:
            prd_data = params.get("prd_data", {})
            
            # Create PRD via API
            response = requests.post(
                f'{self.endcap_api_url}/api/v1/prds',
                json=prd_data,
                timeout=10
            )
            
            if response.status_code == 200:
                prd = response.json()
                return {
                    "success": True,
                    "prd_id": prd["id"],
                    "message": "PRD created successfully in AI Agent Factory"
                }
            else:
                return {"error": f"Failed to create PRD: {response.status_code}"}
        except Exception as e:
            return {"error": f"Failed to create PRD: {str(e)}"}

def main():
    server = SimpleMCPServer()
    
    # Read request from stdin
    try:
        request = json.loads(sys.stdin.read())
        response = server.handle_request(request)
        print(json.dumps(response))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
