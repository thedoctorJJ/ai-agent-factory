#!/usr/bin/env python3
"""
Supabase Manager for Cursor Agent Integration
This module provides comprehensive Supabase database management capabilities
"""

import os
import json
import requests
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

class SupabaseManager:
    """Enhanced Supabase manager with security and database management tools"""
    
    def __init__(self, url: str, service_role_key: str):
        self.url = url.rstrip('/')
        self.service_role_key = service_role_key
        self.headers = {
            'apikey': service_role_key,
            'Authorization': f'Bearer {service_role_key}',
            'Content-Type': 'application/json'
        }
    
    async def check_table_security(self, table_name: str) -> Dict[str, Any]:
        """Check RLS status and security policies for a table"""
        try:
            # Check if table exists and is accessible
            response = requests.get(f"{self.url}/rest/v1/{table_name}?select=*&limit=1", headers=self.headers)
            
            security_info = {
                "table_name": table_name,
                "exists": False,
                "accessible": False,
                "rls_enabled": False,
                "policies": [],
                "permissions": {},
                "error": None
            }
            
            if response.status_code == 200:
                security_info["exists"] = True
                security_info["accessible"] = True
                security_info["permissions"]["read"] = True
                security_info["permissions"]["write"] = True
            elif response.status_code == 401:
                security_info["error"] = "Unauthorized - Check API key permissions"
            elif response.status_code == 403:
                security_info["error"] = "Forbidden - RLS policies may be blocking access"
                security_info["rls_enabled"] = True
            elif response.status_code == 404:
                security_info["error"] = "Table not found"
            else:
                security_info["error"] = f"HTTP {response.status_code}: {response.text}"
            
            return security_info
            
        except Exception as e:
            return {
                "table_name": table_name,
                "exists": False,
                "accessible": False,
                "error": str(e)
            }
    
    async def fix_table_security(self, table_name: str, disable_rls: bool = True) -> Dict[str, Any]:
        """Fix security issues for a table"""
        try:
            # First check current status
            security_check = await self.check_table_security(table_name)
            
            if security_check.get("accessible"):
                return {
                    "success": True,
                    "message": f"Table {table_name} is already accessible",
                    "current_status": security_check
                }
            
            # Try to fix by disabling RLS
            if disable_rls:
                # Note: This would require direct SQL execution
                # For now, we'll provide the SQL commands
                sql_commands = [
                    f"ALTER TABLE {table_name} DISABLE ROW LEVEL SECURITY;",
                    f"GRANT ALL PRIVILEGES ON TABLE {table_name} TO postgres;",
                    f"GRANT ALL PRIVILEGES ON TABLE {table_name} TO service_role;"
                ]
                
                return {
                    "success": False,
                    "requires_manual_action": True,
                    "message": f"Table {table_name} has security restrictions",
                    "sql_commands": sql_commands,
                    "instructions": [
                        "1. Go to Supabase Dashboard → SQL Editor",
                        "2. Run the provided SQL commands",
                        "3. Test the table access again"
                    ],
                    "current_status": security_check
                }
            
            return {
                "success": False,
                "message": f"Could not automatically fix security for {table_name}",
                "current_status": security_check
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_database_schema(self) -> Dict[str, Any]:
        """Get comprehensive database schema information"""
        try:
            # Get information about all tables
            tables = ["agents", "prds", "devin_tasks", "audit_logs", "system_metrics"]
            schema_info = {}
            
            for table in tables:
                security_info = await self.check_table_security(table)
                schema_info[table] = security_info
            
            return {
                "success": True,
                "schema": schema_info,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def test_database_connection(self) -> Dict[str, Any]:
        """Test database connection and basic operations"""
        try:
            # Test basic connection
            response = requests.get(f"{self.url}/rest/v1/", headers=self.headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Database connection successful",
                    "url": self.url,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Connection failed: HTTP {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_sql_query(self, query: str) -> Dict[str, Any]:
        """Execute a SQL query (if supported by the environment)"""
        try:
            # Note: Direct SQL execution requires special permissions
            # This is a placeholder for future implementation
            return {
                "success": False,
                "message": "Direct SQL execution not available through REST API",
                "suggestion": "Use Supabase Dashboard SQL Editor for direct queries",
                "query": query
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_security_recommendations(self) -> Dict[str, Any]:
        """Get security recommendations based on current database state"""
        try:
            schema_info = await self.get_database_schema()
            
            recommendations = []
            issues = []
            
            for table_name, info in schema_info.get("schema", {}).items():
                if not info.get("exists"):
                    issues.append(f"Table {table_name} does not exist")
                elif not info.get("accessible"):
                    issues.append(f"Table {table_name} is not accessible")
                    recommendations.append(f"Fix RLS policies for {table_name}")
                elif info.get("rls_enabled"):
                    recommendations.append(f"Review RLS policies for {table_name}")
            
            return {
                "success": True,
                "issues": issues,
                "recommendations": recommendations,
                "schema_status": schema_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Example usage and testing
async def main():
    """Test the Supabase manager"""
    # This would be called with actual credentials in production
    print("Supabase Manager - Database Security Tools")
    print("=" * 50)
    
    # Example usage (replace with actual credentials)
    # manager = SupabaseManager("https://your-project.supabase.co", "your-service-role-key")
    # 
    # # Check agents table security
    # agents_security = await manager.check_table_security("agents")
    # print(f"Agents table security: {agents_security}")
    # 
    # # Get full schema info
    # schema = await manager.get_database_schema()
    # print(f"Database schema: {schema}")
    
    print("Supabase Manager ready for integration with Cursor Agent")

if __name__ == "__main__":
    asyncio.run(main())
