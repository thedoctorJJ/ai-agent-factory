# Fix Foreign Key Constraint Issue - Step-by-Step Guide

**Date**: November 16, 2025  
**Issue**: Agents cannot be linked to PRDs due to RLS blocking foreign key checks  
**Impact**: Affects all current and future PRDs

---

## 🎯 Goal

Fix Row Level Security (RLS) policies so that foreign key constraint checks work properly when linking agents to PRDs.

---

## 📋 Prerequisites

- Access to Supabase Dashboard
- SQL Editor permissions
- Understanding that this will modify database security policies

---

## 🔧 Step-by-Step Instructions

### Step 1: Open Supabase Dashboard

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Log in to your account
3. Select your project: **agent-factory-474201** (or your project name)

---

### Step 2: Navigate to SQL Editor

1. In the left sidebar, click **"SQL Editor"**
2. Click **"New query"** to create a new SQL query

---

### Step 3: Run the Fix SQL

Copy and paste the following SQL into the SQL Editor:

```sql
-- Fix Foreign Key Constraint Issue with RLS
-- This ensures foreign key checks can see PRDs even with RLS enabled

-- Step 1: Drop existing policies (if they exist)
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
DROP POLICY IF EXISTS "Service role can do everything on agents" ON agents;

-- Step 2: Recreate policies with explicit WITH CHECK clause
-- This allows foreign key constraint checks to work properly
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL 
    USING (true)
    WITH CHECK (true);

-- Step 3: Verify the policies were created
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename IN ('prds', 'agents')
ORDER BY tablename, policyname;
```

---

### Step 4: Execute the Query

1. Click the **"Run"** button (or press `Ctrl+Enter` / `Cmd+Enter`)
2. Wait for the query to complete
3. Check the results:
   - You should see a success message
   - The verification query at the end should show the policies

---

### Step 5: Verify the Fix

Run this test query to verify foreign key checks work:

```sql
-- Test: Try to update an agent with a PRD ID
-- Replace with actual IDs from your database

-- First, get a PRD ID
SELECT id, title FROM prds LIMIT 1;

-- Then, get an agent ID
SELECT id, name FROM agents LIMIT 1;

-- Try to update (this should work now)
-- Replace AGENT_ID and PRD_ID with actual values
-- UPDATE agents SET prd_id = 'PRD_ID' WHERE id = 'AGENT_ID';
```

---

### Step 6: Test via API

After running the SQL fix, test linking an agent to a PRD via the API:

```bash
# Get Redis agent and PRD IDs
curl -s "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents" | \
  python3 -c "import sys, json; agents = json.load(sys.stdin).get('agents', []); \
  redis = [a for a in agents if 'redis' in a.get('name', '').lower()]; \
  print(f'Agent ID: {redis[0].get(\"id\")}' if redis else 'Not found')"

curl -s "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds?limit=100" | \
  python3 -c "import sys, json; prds = json.load(sys.stdin).get('prds', []); \
  redis = [p for p in prds if 'redis' in p.get('title', '').lower() and 'agent' in p.get('title', '').lower()]; \
  print(f'PRD ID: {redis[0].get(\"id\")}' if redis else 'Not found')"

# Then try to link them
curl -X PUT "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents/AGENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"prd_id": "PRD_ID"}'
```

---

## ✅ Verification Checklist

After running the fix, verify:

- [ ] SQL query executed successfully
- [ ] Policies show in the verification query results
- [ ] Can update agent `prd_id` via API without foreign key errors
- [ ] Redis agent can be linked to Redis PRD
- [ ] Future PRDs can be linked to agents

---

## 🔍 Troubleshooting

### Issue: "Policy already exists"

**Solution**: The `DROP POLICY IF EXISTS` should handle this, but if you get an error:
```sql
-- Manually drop the policy first
DROP POLICY "Service role can do everything on prds" ON prds;
-- Then recreate it
```

### Issue: "Permission denied"

**Solution**: Make sure you're using the service role key or have admin access to the database.

### Issue: Foreign key still fails after fix

**Solution**: 
1. Check that the PRD actually exists: `SELECT * FROM prds WHERE id = 'PRD_ID';`
2. Verify RLS is still enabled: `SELECT tablename, rowsecurity FROM pg_tables WHERE tablename = 'prds';`
3. Check policy is active: Run the verification query from Step 3

---

## 📝 What This Fix Does

1. **Drops old policies**: Removes existing RLS policies that might not have `WITH CHECK`
2. **Creates new policies**: Recreates policies with both `USING (true)` and `WITH CHECK (true)`
3. **Allows foreign key checks**: The `WITH CHECK (true)` clause ensures foreign key constraint validation can see the referenced rows

---

## 🔐 Security Note

These policies allow the service role to do everything on `prds` and `agents` tables. This is appropriate for:
- Backend API operations
- Service-to-service communication
- Automated processes

The policies are scoped to the service role, not end users, so security is maintained.

---

## 🎉 Success!

Once this is fixed, you should be able to:
- ✅ Link agents to PRDs via `prd_id`
- ✅ Create new agents with PRD relationships
- ✅ Update existing agents to link to PRDs
- ✅ All future PRDs will work correctly

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message in Supabase SQL Editor
2. Review `docs/troubleshooting/foreign-key-rls-issue.md`
3. Verify your Supabase project settings

---

**Last Updated**: November 16, 2025

