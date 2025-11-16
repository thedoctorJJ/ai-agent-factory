# MCP Server Quick Start - Supabase SQL Execution

**Date**: November 16, 2025  
**Purpose**: Quick setup to enable SQL execution from Cursor Agent

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependency

```bash
pip install psycopg2-binary
```

### Step 2: Get Database URL

1. Go to **Supabase Dashboard** → **Settings** → **Database**
2. Find **"Connection string"** → **"URI"**
3. Copy the connection string (format: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`)
4. Replace `[PASSWORD]` with your actual database password

### Step 3: Add to Cursor MCP Config

Add `DATABASE_URL` to your MCP server environment in Cursor settings:

```json
{
  "mcpServers": {
    "ai-agent-factory": {
      "command": "python3",
      "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"],
      "env": {
        "SUPABASE_URL": "https://ssdcbhxctakgysnayzeq.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key",
        "DATABASE_URL": "postgresql://postgres:YOUR_PASSWORD@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres",
        "GITHUB_TOKEN": "your-github-token",
        "GOOGLE_CLOUD_PROJECT_ID": "agent-factory-474201"
      }
    }
  }
}
```

**Important**: Replace `YOUR_PASSWORD` with your actual Supabase database password.

---

## ✅ Test It

After restarting Cursor, you can now use:

```
execute_supabase_sql
sql: "SELECT COUNT(*) FROM prds;"
```

---

## 🎯 Use Cases

- ✅ Fix RLS policies without leaving Cursor
- ✅ Check foreign key constraints
- ✅ Verify database state
- ✅ Run any SQL query

---

**Full Guide**: `docs/guides/CURSOR_MCP_SUPABASE_SETUP.md`

