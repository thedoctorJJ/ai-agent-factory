#!/usr/bin/env python3
"""
Simple service implementations for Cursor Agent MCP Server
"""

import os
import json
import requests
import subprocess
from typing import Dict, Any, Optional, List

class SimpleSupabaseService:
    """Simple Supabase service for basic operations"""
    
    def __init__(self, url: str, service_role_key: str):
        self.url = url.rstrip('/')
        self.service_role_key = service_role_key
        self.headers = {
            'apikey': service_role_key,
            'Authorization': f'Bearer {service_role_key}',
            'Content-Type': 'application/json'
        }
    
    async def execute_query(self, table: str, operation: str = "select", data: Optional[Dict] = None, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a simple query on a Supabase table"""
        try:
            url = f"{self.url}/rest/v1/{table}"
            
            if operation == "select":
                response = requests.get(url, headers=self.headers)
            elif operation == "insert":
                response = requests.post(url, headers=self.headers, json=data)
            elif operation == "update":
                response = requests.patch(url, headers=self.headers, json=data)
            else:
                return {"error": f"Unsupported operation: {operation}"}
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"Request failed: {response.status_code} - {response.text}"}
        
        except Exception as e:
            return {"error": f"Supabase operation failed: {str(e)}"}
    
    # Add client property for compatibility
    @property
    def client(self):
        return self

class SimpleGitHubService:
    """Simple GitHub service for basic operations"""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    async def get_user(self) -> Dict[str, Any]:
        """Get current user information"""
        try:
            response = requests.get('https://api.github.com/user', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get user: {response.status_code}"}
        except Exception as e:
            return {"error": f"GitHub operation failed: {str(e)}"}
    
    async def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
        """Create a new repository"""
        try:
            data = {
                "name": name,
                "description": description,
                "private": private,
                "auto_init": True
            }
            response = requests.post('https://api.github.com/user/repos', headers=self.headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                return {"error": f"Failed to create repository: {response.status_code} - {response.text}"}
        except Exception as e:
            return {"error": f"GitHub operation failed: {str(e)}"}
    
    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        try:
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}', headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get repository: {response.status_code}"}
        except Exception as e:
            return {"error": f"GitHub operation failed: {str(e)}"}

class SimpleOpenAIService:
    """Simple OpenAI service for basic operations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection"""
        try:
            response = requests.get('https://api.openai.com/v1/models', headers=self.headers)
            if response.status_code == 200:
                return {"success": True, "message": "OpenAI API connection successful"}
            else:
                return {"error": f"OpenAI API test failed: {response.status_code}"}
        except Exception as e:
            return {"error": f"OpenAI operation failed: {str(e)}"}

class SimpleDatabaseService:
    """Simple database service for basic operations"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        try:
            # Simple connection test using psql if available
            result = subprocess.run([
                'psql', self.database_url, '-c', 'SELECT 1;'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {"success": True, "message": "Database connection successful"}
            else:
                return {"error": f"Database connection failed: {result.stderr}"}
        except subprocess.TimeoutExpired:
            return {"error": "Database connection timeout"}
        except FileNotFoundError:
            return {"error": "psql not found - cannot test database connection"}
        except Exception as e:
            return {"error": f"Database test failed: {str(e)}"}
