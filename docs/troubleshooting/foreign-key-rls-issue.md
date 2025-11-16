# Foreign Key Constraint Issue with RLS

**Date**: November 16, 2025  
**Status**: ⚠️ **IDENTIFIED** - Root cause found, solution needed

---

## 🐛 Problem

When trying to link an agent to a PRD by setting `agents.prd_id`, Supabase returns a foreign key constraint violation:

```
insert or update on table "agents" violates foreign key constraint "agents_prd_id_fkey"
Key is not present in table "prds"
```

However, the PRD **does exist** and is accessible via the API.

---

## 🔍 Root Cause

This is a known issue with **Row Level Security (RLS)** and foreign key constraints in Supabase:

1. **RLS is enabled** on the `prds` table
2. When Supabase validates a foreign key constraint, it checks if the referenced row exists
3. This check happens in a security context where **RLS policies might prevent seeing the PRD**
4. Even though the service role can read the PRD via API, the foreign key check fails

---

## 📋 Current State

- ✅ PRD exists in database (can be queried via API)
- ✅ Agent exists in database
- ❌ Cannot link them via `prd_id` foreign key
- ❌ This will affect **all future PRDs** if not fixed

---

## 🔧 Potential Solutions

### Solution 1: Fix RLS Policies (Recommended)

Ensure RLS policies allow foreign key constraint checks:

```sql
-- Recreate policies with explicit WITH CHECK clause
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);
```

### Solution 2: Use Application-Level Validation

Instead of relying on database foreign key constraints, validate in the application:

1. Check PRD exists before setting `prd_id`
2. Handle the relationship at the application level
3. Remove or make the foreign key constraint nullable/optional

### Solution 3: Disable RLS (Not Recommended)

Disable RLS on the `prds` table (security risk):

```sql
ALTER TABLE prds DISABLE ROW LEVEL SECURITY;
```

### Solution 4: Use Triggers Instead

Replace foreign key constraint with a trigger that validates the relationship.

---

## 🎯 Recommended Approach

**Use Solution 1 + Solution 2 combination:**

1. Fix RLS policies to ensure foreign key checks work
2. Add application-level validation as a safety net
3. Provide clear error messages when linking fails

---

## 📝 Implementation Steps

1. ✅ Added PRD existence check before setting `prd_id` (in `simple_data_manager.py`)
2. ⏳ Need to fix RLS policies in Supabase dashboard or via migration
3. ⏳ Test linking agent to PRD after RLS fix
4. ⏳ Document the fix

---

## 🔗 Related Issues

- Agent-PRD linking fails for all agents
- Foreign key constraints don't work with RLS enabled
- Future PRDs will have the same issue

---

## 📚 References

- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL Foreign Keys with RLS](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)

---

**Last Updated**: November 16, 2025

