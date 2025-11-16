# Verify RLS Fix Was Applied Correctly

**Date**: November 16, 2025  
**Purpose**: Verify that the RLS policy fix was applied correctly in Supabase

---

## 🔍 Verification Steps

### Step 1: Check Policies Exist

Run this SQL in Supabase SQL Editor:

```sql
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

**Expected Result:**
- Should see policies named "Service role can do everything on prds" and "Service role can do everything on agents"
- Both should have `with_check` showing `true` or a condition that evaluates to true
- `cmd` should show `ALL` or include `INSERT` and `UPDATE`

---

### Step 2: Verify RLS is Enabled

```sql
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE tablename IN ('prds', 'agents')
ORDER BY tablename;
```

**Expected Result:**
- Both tables should show `rls_enabled = true`

---

### Step 3: Check Policy Details

```sql
-- Check the exact policy definition
SELECT 
    tablename,
    policyname,
    pg_get_expr(polqual, polrelid) as using_expression,
    pg_get_expr(polwithcheck, polrelid) as with_check_expression
FROM pg_policy
WHERE tablename IN ('prds', 'agents');
```

**Expected Result:**
- `using_expression` should be `true` or similar
- `with_check_expression` should be `true` or similar (this is critical for foreign keys)

---

## ⚠️ If Policies Are Missing or Incorrect

If the policies don't show up or `with_check` is NULL/empty, re-run the fix:

```sql
-- Drop and recreate
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

---

## 🔧 Alternative: Check Service Role Context

The issue might be that foreign key checks happen in a different security context. Try:

```sql
-- Check if we can see PRDs in the service role context
SET ROLE service_role;
SELECT COUNT(*) FROM prds;
RESET ROLE;
```

---

## 📝 Notes

- RLS policy changes should be immediate, but sometimes take a few seconds
- Foreign key constraint checks happen in the context of the user/role performing the operation
- The `WITH CHECK (true)` clause is essential for foreign key validation

---

**Last Updated**: November 16, 2025

