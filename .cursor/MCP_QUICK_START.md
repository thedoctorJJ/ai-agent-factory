# Quick Start: Using MCP Server to Fix RLS

## ✅ Setup Complete!

The MCP server is configured. **Restart Cursor** to activate it.

## 🚀 After Restarting Cursor

Once Cursor is restarted, you can use the MCP server to fix the RLS issue and link the Redis agent:

### Step 1: Fix RLS Policies

Ask Cursor Agent:
```
Use the execute_supabase_sql tool to fix RLS policies. Run this SQL:

DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
DROP POLICY IF EXISTS "Service role can do everything on agents" ON agents;

CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL 
    USING (true)
    WITH CHECK (true);
```

### Step 2: Link Redis Agent to PRD

After RLS is fixed, link the agent:
```
Use the API to update the Redis agent (ID: 6c3dec86-457f-42e0-b04a-e7994607e133) 
to link it to the Redis PRD (ID: e1e6747f-ddfc-4ce8-9d41-a714cf9d545c)
```

Or use curl:
```bash
curl -X PUT "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents/6c3dec86-457f-42e0-b04a-e7994607e133" \
  -H "Content-Type: application/json" \
  -d '{"prd_id": "e1e6747f-ddfc-4ce8-9d41-a714cf9d545c"}'
```

## 📋 Configuration Location

- **Project Config**: `.cursor/mcp.json` (created)
- **MCP Server**: `scripts/mcp/cursor-agent-mcp-server.py`
- **Auto-loads from**: `config/env/.env.local`

## ✅ Verification

After restarting Cursor, test with:
```
execute_supabase_sql
sql: "SELECT COUNT(*) FROM prds;"
```

If this works, the MCP server is active!








