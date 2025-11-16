-- Simple Fix for Foreign Key Constraint Issue with RLS
-- Run this in Supabase SQL Editor

-- Drop existing policies
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
DROP POLICY IF EXISTS "Service role can do everything on agents" ON agents;

-- Recreate with WITH CHECK clause (allows foreign key checks)
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can do everything on agents" ON agents
    FOR ALL 
    USING (true)
    WITH CHECK (true);

-- Verify policies were created
SELECT 
    tablename,
    policyname,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename IN ('prds', 'agents')
ORDER BY tablename, policyname;

