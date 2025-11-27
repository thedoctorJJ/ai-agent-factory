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
    
    def __init__(self, url: str, service_role_key: str, database_url: Optional[str] = None):
        self.url = url.rstrip('/')
        self.service_role_key = service_role_key
        self.database_url = database_url
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
    
    async def execute_sql(self, sql: str) -> Dict[str, Any]:
        """Execute raw SQL query using direct PostgreSQL connection"""
        # First, try to get DATABASE_URL from environment (MCP config might have it)
        database_url = self.database_url or os.getenv("DATABASE_URL")
        
        if not database_url:
            return {"error": "Database URL not configured. Cannot execute SQL directly."}
        
        try:
            # Try to use psycopg2 if available
            try:
                import psycopg2
                from psycopg2.extras import RealDictCursor
            except ImportError:
                return {
                    "error": "psycopg2 not installed. Install with: pip install psycopg2-binary",
                    "suggestion": "For SQL execution, install psycopg2-binary or use Supabase Dashboard SQL Editor"
                }
            
            # Parse connection string and execute
            # Ensure SSL is enabled for Supabase connections
            if 'sslmode' not in database_url:
                if '?' in database_url:
                    database_url += '&sslmode=require'
                else:
                    database_url += '?sslmode=require'
            
            # Force IPv4 connection to avoid IPv6 connection issues
            import socket
            original_getaddrinfo = socket.getaddrinfo
            
            def getaddrinfo_ipv4(*args, **kwargs):
                """Force IPv4 resolution"""
                results = original_getaddrinfo(*args, **kwargs)
                # Filter to IPv4 only
                ipv4_results = [r for r in results if r[0] == socket.AF_INET]
                # If we have IPv4 results, use them; otherwise fall back to all
                return ipv4_results if ipv4_results else results
            
            # Temporarily override getaddrinfo to prefer IPv4
            socket.getaddrinfo = getaddrinfo_ipv4
            
            try:
                conn = psycopg2.connect(database_url, connect_timeout=10)
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                try:
                    cursor.execute(sql)
                    
                    # Check if it's a SELECT query
                    if sql.strip().upper().startswith('SELECT'):
                        results = cursor.fetchall()
                        # Convert to list of dicts
                        data = [dict(row) for row in results]
                        conn.commit()
                        return {
                            "success": True,
                            "data": data,
                            "row_count": len(data)
                        }
                    else:
                        # For INSERT, UPDATE, DELETE, etc.
                        conn.commit()
                        rows_affected = cursor.rowcount
                        return {
                            "success": True,
                            "message": f"Query executed successfully",
                            "rows_affected": rows_affected
                        }
                except Exception as e:
                    conn.rollback()
                    return {"error": f"SQL execution failed: {str(e)}"}
                finally:
                    cursor.close()
                    conn.close()
            finally:
                # Restore original getaddrinfo
                socket.getaddrinfo = original_getaddrinfo
        
        except Exception as e:
            return {"error": f"Database connection failed: {str(e)}"}
    
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
    
    async def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = "main") -> Dict[str, Any]:
        """Get file content from repository"""
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}'
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "File not found"}
            else:
                return {"error": f"Failed to get file: {response.status_code}"}
        except Exception as e:
            return {"error": f"GitHub operation failed: {str(e)}"}
    
    async def create_or_update_file(self, repo_owner: str, repo_name: str, file_path: str, 
                                   content: str, message: str, branch: str = "main") -> Dict[str, Any]:
        """Create or update a file in the repository"""
        import base64
        
        try:
            # Check if file exists to get its SHA (required for updates)
            existing_file = await self.get_file_content(repo_owner, repo_name, file_path, branch)
            sha = existing_file.get("sha") if "error" not in existing_file else None
            
            # Encode content to base64
            content_bytes = content.encode('utf-8')
            content_base64 = base64.b64encode(content_bytes).decode('utf-8')
            
            # Prepare data for GitHub API
            data = {
                "message": message,
                "content": content_base64,
                "branch": branch
            }
            
            # If file exists, include its SHA for update
            if sha:
                data["sha"] = sha
            
            # Create or update file via GitHub API
            url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
            response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "commit_sha": result.get("commit", {}).get("sha"),
                    "html_url": result.get("content", {}).get("html_url"),
                    "download_url": result.get("content", {}).get("download_url")
                }
            else:
                return {"error": f"Failed to create/update file: {response.status_code} - {response.text}"}
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
