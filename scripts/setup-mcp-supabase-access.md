# Setup MCP Server to Access Supabase

## Current Status

✅ **MCP Server Configured**: `.cursor/mcp.json` and `~/.cursor/mcp.json`  
✅ **Dependencies Installed**: `psycopg2-binary`  
✅ **Code Updated**: MCP server now checks environment variables for DATABASE_URL  
⚠️ **Issue**: DATABASE_URL has placeholder password `postgres:postgres`

## Solution: Get Database Password via Management API

### Step 1: Get Supabase Personal Access Token

1. Go to: https://supabase.com/dashboard/account/tokens
2. Click "Generate New Token"
3. Copy the token
4. Set it as environment variable:
   ```bash
   export SUPABASE_ACCESS_TOKEN='your-token-here'
   ```

### Step 2: Retrieve Database Password

Run the script:
```bash
python3 scripts/get-db-password-via-management-api.py
```

This will:
- Use the Management API to get your database password
- Display the full DATABASE_URL with the correct password

### Step 3: Update MCP Configuration

Update `~/.cursor/mcp.json` with the correct DATABASE_URL:
```json
{
  "mcpServers": {
    "ai-agent-factory": {
      "command": "python3",
      "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"],
      "env": {
        "DATABASE_URL": "postgresql://postgres:ACTUAL_PASSWORD@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres",
        ...
      }
    }
  }
}
```

### Step 4: Restart Cursor

After updating the config, restart Cursor to load the new DATABASE_URL.

## Alternative: Use Supabase CLI

If you prefer CLI:
```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Login
supabase login

# Get database password
supabase projects api-keys --project-ref ssdcbhxctakgysnayzeq
```

## How It Works

The MCP server code has been updated to:
1. Check `os.getenv("DATABASE_URL")` first (from MCP config)
2. Fall back to `config.database_url` (from .env.local)
3. Use the Supabase Python client with service role key for table operations
4. Use direct PostgreSQL connection (psycopg2) for SQL execution

Once DATABASE_URL has the correct password, the `execute_supabase_sql` tool will work!







