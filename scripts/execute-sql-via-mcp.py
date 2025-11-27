#!/usr/bin/env python3
"""
Execute SQL via MCP server code
This uses the same code as the MCP server to execute SQL directly
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the MCP server class
from scripts.mcp.cursor_agent_mcp_server import CursorAgentMCPServer

async def execute_sql(sql: str):
    """Execute SQL using MCP server"""
    server = CursorAgentMCPServer()
    result = await server.call_tool("execute_supabase_sql", {"sql": sql})
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 execute-sql-via-mcp.py '<SQL_QUERY>'")
        sys.exit(1)
    
    sql = sys.argv[1]
    result = asyncio.run(execute_sql(sql))
    print(json.dumps(result, indent=2))








