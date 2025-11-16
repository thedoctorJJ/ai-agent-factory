# Connect Cursor Agent to Supabase via MCP

**Date**: November 16, 2025  
**Purpose**: Enable direct SQL execution on Supabase from Cursor Agent  
**Status**: ✅ **READY** - SQL execution tool added to MCP server

---

## 🎯 Overview

You can now execute SQL queries directly on Supabase from Cursor Agent, eliminating the need to switch to the Supabase dashboard. This is perfect for:
- Fixing RLS policies
- Checking foreign key constraints
- Running verification queries
- Database maintenance

---

## 🔧 Setup Instructions

### Step 1: Install Dependencies

```bash
cd /Users/jason/Repositories/ai-agent-factory
pip install psycopg2-binary
```

Or if using the MCP requirements:

```bash
pip install -r scripts/mcp/requirements.txt
```

### Step 2: Verify MCP Server Configuration

The MCP server is already configured at:
- **File**: `scripts/mcp/cursor-agent-mcp-server.py`
- **Config**: `config/cursor-agent-mcp-config.json`

### Step 3: Add to Cursor MCP Settings

Add this to your Cursor MCP configuration (`.cursor/mcp.json` or Cursor settings):

```json
{
  "mcpServers": {
    "ai-agent-factory": {
      "command": "python3",
      "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"],
      "env": {
        "SUPABASE_URL": "https://ssdcbhxctakgysnayzeq.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key",
        "DATABASE_URL": "postgresql://postgres:[PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres",
        "GITHUB_TOKEN": "your-github-token",
        "GOOGLE_CLOUD_PROJECT_ID": "agent-factory-474201",
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

**Important**: Replace `[PASSWORD]` in `DATABASE_URL` with your actual Supabase database password.

---

## 🛠️ Available Tools

### New Tool: `execute_supabase_sql`

Execute SQL queries directly on Supabase.

**Usage in Cursor Agent:**
```
execute_supabase_sql
sql: "SELECT tablename, policyname, with_check FROM pg_policies WHERE tablename IN ('prds', 'agents');"
```

**Example Queries:**

1. **Check RLS Policies:**
```sql
SELECT 
    tablename,
    policyname,
    cmd,
    with_check
FROM pg_policies
WHERE tablename IN ('prds', 'agents')
ORDER BY tablename, policyname;
```

2. **Fix Foreign Key RLS Issue:**
```sql
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

3. **Verify Policies:**
```sql
SELECT 
    tablename,
    policyname,
    pg_get_expr(polqual, polrelid) as using_expression,
    pg_get_expr(polwithcheck, polrelid) as with_check_expression
FROM pg_policy
WHERE tablename IN ('prds', 'agents');
```

4. **Check Foreign Key Status:**
```sql
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
  AND tc.table_name = 'agents';
```

---

## ✅ Benefits

1. **No Context Switching**: Run SQL from Cursor Agent
2. **Immediate Results**: See query results instantly
3. **Fix Issues Fast**: Apply RLS fixes without leaving Cursor
4. **Verify Changes**: Check policies and constraints immediately

---

## 🔐 Security Notes

- Uses service role key for authentication
- Direct database connection (requires `DATABASE_URL`)
- Can execute any SQL (use with caution)
- Results are returned directly to Cursor Agent

---

## 📝 Example Workflow

**Fix Foreign Key RLS Issue:**

1. In Cursor Agent, use: `execute_supabase_sql`
2. Run verification query to check current policies
3. Run fix SQL to update policies
4. Verify the fix worked
5. Test linking agent to PRD via API

**All without leaving Cursor!**

---

## 🚨 Troubleshooting

### Issue: "psycopg2 not installed"

**Solution:**
```bash
pip install psycopg2-binary
```

### Issue: "Database URL not configured"

**Solution:**
- Add `DATABASE_URL` to MCP server environment variables
- Format: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`
- Get password from Supabase Dashboard → Settings → Database

### Issue: "Connection refused"

**Solution:**
- Verify Supabase project is not paused
- Check database password is correct
- Ensure IP allowlist allows your connection (if configured)

---

## 🔗 Related Documentation

- `docs/guides/FIX_FOREIGN_KEY_RLS_GUIDE.md` - RLS fix guide
- `docs/guides/VERIFY_RLS_FIX.md` - Verification queries
- `scripts/mcp/cursor-agent-mcp-server.py` - MCP server implementation

---

**Last Updated**: November 16, 2025

