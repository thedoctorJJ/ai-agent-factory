# MCP Server and Database Health Check

## Overview

The MCP (Model Context Protocol) server is the primary method for accessing the Supabase database from Cursor. This health check ensures that:

1. ✅ MCP server is properly configured
2. ✅ MCP server can be initialized
3. ✅ Database is accessible via MCP server
4. ✅ SQL queries can be executed through MCP

## Running the Health Check

```bash
python3 scripts/health-check-mcp-database.py
```

## What It Checks

### 1. MCP Configuration
- Verifies `~/.cursor/mcp.json` exists and is properly formatted
- Checks that `ai-agent-factory` server is configured
- Validates that required environment variables are set:
  - `DATABASE_URL`
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`

### 2. MCP Server Initialization
- Tests that the MCP server script can be imported
- Verifies the server can be instantiated
- Checks that Supabase service is configured
- Validates database URL is available

### 3. Database Connectivity via MCP
- **Simple Query Test**: Executes `SELECT 1` to verify basic connectivity
- **Table Access**: Tests access to `agents` and `prds` tables
- **RLS Policies**: Verifies RLS policies are correctly configured with `WITH CHECK` clauses

## Expected Results

All checks should pass:
- ✅ MCP Configuration: PASS
- ✅ MCP Server: PASS
- ✅ Database (via MCP): PASS

## Troubleshooting

### If MCP Configuration Fails
1. Check that `~/.cursor/mcp.json` exists
2. Verify the file is valid JSON
3. Ensure `ai-agent-factory` server is configured
4. Check that environment variables are set

### If MCP Server Fails
1. Verify `scripts/mcp/cursor-agent-mcp-server.py` exists
2. Check that Python dependencies are installed
3. Ensure the script is executable
4. Review error messages for specific issues

### If Database Check Fails
1. **Connection Issues**:
   - Check `DATABASE_URL` is correct
   - Verify database password is not a placeholder
   - Ensure IP is not banned in Supabase
   - Check network connectivity

2. **RLS Policy Issues**:
   - Verify RLS policies have `WITH CHECK (true)` clause
   - Check that policies allow service role access
   - See `infra/database/fix-foreign-key-rls-simple.sql` for fix

3. **Table Access Issues**:
   - Verify tables exist in database
   - Check RLS policies allow access
   - Ensure service role key has proper permissions

## Integration with Startup Prompt

This health check is automatically run as part of the startup process (Step 4.0 in `startup-prompt.md`). It ensures that:

- Database operations will work from Cursor
- MCP server is ready for use
- All database connectivity issues are identified early

## Related Files

- **Health Check Script**: `scripts/health-check-mcp-database.py`
- **MCP Server**: `scripts/mcp/cursor-agent-mcp-server.py`
- **MCP Config**: `~/.cursor/mcp.json`
- **Startup Prompt**: `.cursor/startup-prompt.md`
- **RLS Fix SQL**: `infra/database/fix-foreign-key-rls-simple.sql`




