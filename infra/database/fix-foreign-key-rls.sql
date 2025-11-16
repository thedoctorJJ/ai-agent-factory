-- Fix Foreign Key Constraint Issues with RLS
-- This script ensures that foreign key constraints work properly with RLS enabled

-- The issue: When RLS is enabled, foreign key constraint checks might fail
-- because the constraint check happens in a context where RLS policies prevent
-- seeing the referenced row, even though the service role can access it.

-- Solution 1: Ensure RLS policies allow foreign key checks
-- Foreign key checks need to be able to see the referenced row

-- Check current RLS status
DO $$
BEGIN
    -- Verify RLS is enabled
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables 
        WHERE tablename = 'prds' 
        AND rowsecurity = true
    ) THEN
        RAISE NOTICE 'RLS is not enabled on prds table';
    END IF;
END $$;

-- Ensure the service role policy allows foreign key checks
-- The existing policy "Service role can do everything on prds" should work,
-- but we need to make sure it's applied correctly

-- Recreate the policy to ensure it's correct
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);

-- Also ensure agents table policy is correct
DROP POLICY IF EXISTS "Service role can do everything on agents" ON agents;
CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL 
    USING (true)
    WITH CHECK (true);

-- Alternative: If the above doesn't work, we might need to temporarily
-- disable RLS for foreign key checks, or use a different approach

-- Note: Supabase uses the service role key for API operations,
-- which should bypass RLS, but foreign key checks might still fail.
-- This is a known issue with Supabase RLS and foreign keys.

-- If the issue persists, we may need to:
-- 1. Use a trigger instead of a foreign key constraint
-- 2. Disable RLS on the prds table (not recommended for security)
-- 3. Use application-level validation instead of database constraints

