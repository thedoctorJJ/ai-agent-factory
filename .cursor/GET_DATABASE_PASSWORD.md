# Get Database Password from Supabase Dashboard

## Step-by-Step Instructions

### Step 1: Get Database Password from Supabase Dashboard

1. **Go to Supabase Dashboard**
   - URL: https://supabase.com/dashboard
   - Login to your account

2. **Select Your Project**
   - Project: `ssdcbhxctakgysnayzeq` (or find it in your project list)

3. **Navigate to Database Settings**
   - Click **"Settings"** in the left sidebar
   - Click **"Database"** in the settings menu

4. **Get Connection String**
   - Scroll down to **"Connection string"** section
   - Find **"URI"** tab
   - Copy the connection string
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres`

### Step 2: Update MCP Configuration

1. **Open MCP Config File**
   ```bash
   code ~/.cursor/mcp.json
   # Or use your preferred editor
   ```

2. **Update DATABASE_URL**
   - Find the `DATABASE_URL` in the `env` section
   - Replace the placeholder password with the actual password from Step 1
   - Example:
     ```json
     "DATABASE_URL": "postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres"
     ```

3. **Save the file**

### Step 3: Restart Cursor

1. **Quit Cursor completely** (Cmd+Q on Mac)
2. **Reopen Cursor**
3. The MCP server will now use the correct DATABASE_URL

### Step 4: Test the MCP Server

After restarting, test with:
```
Use the execute_supabase_sql tool to run: SELECT COUNT(*) FROM prds;
```

## What to Copy from Dashboard

When you're in the Database settings, you'll see something like:

**Connection string → URI:**
```
postgresql://postgres:[YOUR-PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres
```

Copy the **entire string** including the password (the part in brackets `[YOUR-PASSWORD]` will be your actual password).

## Quick Reference

- **Dashboard URL**: https://supabase.com/dashboard
- **Project**: `ssdcbhxctakgysnayzeq`
- **Config File**: `~/.cursor/mcp.json`
- **What to Update**: `DATABASE_URL` in the `env` section







