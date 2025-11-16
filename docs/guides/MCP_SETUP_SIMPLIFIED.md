# MCP Server Setup - Simplified (Secrets Already Available)

**Date**: November 16, 2025  
**Status**: ✅ **Secrets Already Configured** - Minimal setup needed

---

## ✅ Good News!

**All Supabase secrets are already configured!**

- ✅ `SUPABASE_URL` - Available
- ✅ `SUPABASE_SERVICE_ROLE_KEY` - Available  
- ✅ `DATABASE_URL` - Available

The MCP server uses the same `Config` class that loads from your existing environment files, so **no manual secret configuration is needed!**

---

## 🔧 Minimal Setup Required

### Step 1: Install SQL Execution Dependency

```bash
pip install psycopg2-binary
```

This enables the `execute_supabase_sql` tool.

### Step 2: Verify MCP Server is Configured in Cursor

The MCP server should already be configured. If not, add it to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "ai-agent-factory": {
      "command": "python3",
      "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"]
    }
  }
}
```

**Note**: No need to add `env` section - the MCP server automatically loads from your existing `.env.local` file!

### Step 3: Restart Cursor

Restart Cursor to load the updated MCP server with SQL execution capability.

---

## ✅ That's It!

The MCP server will automatically:
- ✅ Load `SUPABASE_URL` from your config
- ✅ Load `SUPABASE_SERVICE_ROLE_KEY` from your config
- ✅ Load `DATABASE_URL` from your config
- ✅ Use all existing secrets

**No manual secret configuration needed!**

---

## 🧪 Test It

After restarting Cursor, use:

```
execute_supabase_sql
sql: "SELECT COUNT(*) FROM prds;"
```

---

## 📝 Why This Works

The MCP server (`cursor-agent-mcp-server.py`) uses:
```python
from backend.fastapi_app.config import Config
```

This same `Config` class that your backend uses, which automatically loads from:
1. `config/env/.env.local` (your existing secrets file)
2. `.env` (project root)
3. Environment variables

So all your existing secrets are automatically available!

---

**Last Updated**: November 16, 2025

