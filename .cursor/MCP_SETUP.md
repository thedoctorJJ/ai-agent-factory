# MCP Server Setup for Cursor

## ✅ Configuration Complete!

The MCP server is now configured for Cursor. Here's what was set up:

### Files Created:
- `.cursor/mcp.json` - Cursor MCP configuration file
- MCP server script: `scripts/mcp/cursor-agent-mcp-server.py`

### Dependencies Installed:
- ✅ `psycopg2-binary` - For SQL execution

## 🔄 Next Steps

### 1. Restart Cursor
**Important**: You must restart Cursor for the MCP server to be loaded.

1. Quit Cursor completely (Cmd+Q on Mac)
2. Reopen Cursor
3. The MCP server should now be available

### 2. Verify MCP Server is Loaded

After restarting, you should see the MCP server in Cursor's MCP panel, or you can test it by asking Cursor Agent to use the `execute_supabase_sql` tool.

### 3. Test the MCP Server

Try this command in Cursor Agent:
```
Use the execute_supabase_sql tool to run: SELECT COUNT(*) FROM prds;
```

## 🛠️ Available MCP Tools

The MCP server provides these tools:

- `execute_supabase_sql` - Execute SQL queries directly on Supabase
- `get_platform_status` - Get comprehensive platform status
- `list_prds` - List all PRDs
- `list_agents` - List all agents
- `get_agent_details` - Get agent information
- `create_github_repo` - Create GitHub repositories
- And more...

## 📝 How It Works

The MCP server automatically loads configuration from:
- `config/env/.env.local` - Your existing secrets file
- No manual environment variable configuration needed!

## 🔧 Troubleshooting

If the MCP server doesn't work after restarting:

1. **Check Cursor Settings**: 
   - Open Cursor Settings
   - Look for "MCP" or "Model Context Protocol" settings
   - Verify the server is listed

2. **Check Logs**:
   - Cursor may show MCP server errors in the output panel
   - Look for any Python import errors

3. **Verify Python Path**:
   - The MCP server uses `python3` from your system
   - Make sure Python 3 is available in your PATH

4. **Test Manually**:
   ```bash
   python3 /Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py
   ```
   (This should start the MCP server in stdio mode)

## ✅ Ready to Use!

Once Cursor is restarted, you can use the MCP server to:
- Fix RLS policies
- Execute SQL queries
- Manage PRDs and agents
- And much more!








