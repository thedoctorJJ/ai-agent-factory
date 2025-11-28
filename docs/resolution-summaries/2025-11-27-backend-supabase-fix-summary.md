# Backend Supabase Connection Fix - Summary
**Date**: November 27, 2025  
**Status**: ⚠️ Partially Fixed - Connection Works, Writes Not Persisting

## Problem

The backend was using in-memory storage instead of Supabase, even in production on Cloud Run.

## Fixes Applied

### ✅ 1. Force Production Mode
- Updated `_get_data_mode()` to always return "production" when `ENVIRONMENT=production`
- Prevents silent fallback to development mode

### ✅ 2. Improved Error Handling
- Added detailed logging for Supabase initialization
- Added error messages when Supabase connection fails
- Added safeguard to prevent in-memory writes in production

### ✅ 3. Debug Endpoint
- Added `/api/v1/debug/data-manager` endpoint
- Shows data manager mode, Supabase connection status, and configuration

### ✅ 4. Better Logging
- Added logging to `create_prd()` to track Supabase inserts
- Logs success/failure of database operations

## Current Status

### ✅ Working
- **Supabase Connection**: Debug endpoint confirms connection is established
  - `mode: "production"`
  - `has_supabase_client: true`
  - `is_connected: true`
- **Configuration**: All Supabase credentials are set correctly
- **Code**: All fixes deployed to Cloud Run

### ❌ Not Working
- **Database Writes**: PRDs are not being saved to Supabase
  - SQL query: `SELECT COUNT(*) FROM prds;` → Returns 0
  - API shows PRDs exist (likely still in-memory or different issue)
- **Duplicate Prevention**: Not working because writes aren't persisting
  - Same file uploaded twice creates different IDs
  - `get_prd_by_hash()` can't find existing PRDs because they're not in database

## Root Cause Analysis

The Supabase client is connected, but writes aren't persisting. Possible causes:

1. **RLS Policies**: Row Level Security policies might be blocking inserts
2. **Transaction Issues**: Inserts might be failing silently
3. **Permission Issues**: Service role key might not have insert permissions
4. **Schema Mismatch**: PRD data structure might not match database schema

## Next Steps

### 1. Check RLS Policies
```sql
SELECT tablename, policyname, cmd, with_check 
FROM pg_policies 
WHERE tablename = 'prds';
```

If policies are missing or incorrect:
```sql
DROP POLICY IF EXISTS "Service role can do everything on prds" ON prds;
CREATE POLICY "Service role can do everything on prds" ON prds
    FOR ALL 
    USING (true)
    WITH CHECK (true);
```

### 2. Check Cloud Run Logs
```bash
gcloud run services logs read ai-agent-factory-backend \
  --region us-central1 \
  --limit 100 | grep -i -E "(insert|supabase|error|prd)"
```

Look for:
- "Inserting PRD into Supabase"
- "ERROR inserting PRD"
- Any Supabase-related errors

### 3. Test Direct Insert
Try inserting a PRD directly via SQL to verify schema:
```sql
INSERT INTO prds (id, title, description, content_hash, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Test PRD',
  'Test description',
  'test_hash_123',
  NOW(),
  NOW()
);
```

### 4. Verify Service Role Key Permissions
Ensure the service role key has proper permissions to insert into the `prds` table.

## Files Modified

1. ✅ `backend/fastapi_app/utils/simple_data_manager.py`
   - Force production mode when `ENVIRONMENT=production`
   - Improved error handling and logging
   - Added safeguard against in-memory writes in production

2. ✅ `backend/fastapi_app/routers/health.py`
   - Added `/api/v1/debug/data-manager` endpoint

## Testing

### Debug Endpoint
```bash
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/debug/data-manager
```

**Expected Output:**
```json
{
  "data_manager": {
    "mode": "production",
    "has_supabase_client": true,
    "is_connected": true
  },
  "supabase_config": {
    "url_set": true,
    "service_role_key_set": true
  }
}
```

### Duplicate Prevention Test
```bash
# Upload same file twice
curl -X POST "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/upload" \
  -F "file=@prds/queue/test-prd.md"

# Should return same ID on second upload
```

## Conclusion

The backend is now correctly configured to use Supabase in production, and the connection is established. However, database writes are not persisting, which prevents duplicate prevention from working. The next step is to investigate why inserts are failing (likely RLS policies or permissions).

---

**Status**: Connection fixed, writes need investigation.

