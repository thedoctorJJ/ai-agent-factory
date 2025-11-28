# Backend Supabase Connection Issue
**Date**: November 27, 2025  
**Status**: ⚠️ In Progress - Backend Using In-Memory Storage

## Problem

The backend is using in-memory storage instead of Supabase, even though:
- ✅ Secrets are deployed via Secrets Manager
- ✅ Health check shows Supabase as "configured"
- ✅ Environment variables are set

**Evidence:**
- SQL query: `SELECT COUNT(*) FROM prds;` → Returns 0
- API query: `/api/v1/prds` → Returns 2 PRDs
- Duplicate prevention not working (creates duplicates)

## Root Cause

The `SimpleDataManager` initializes at module load time. If Supabase connection fails during initialization, it silently falls back to development mode (in-memory storage).

## Fixes Applied

1. ✅ Updated `_get_data_mode()` to check `ENVIRONMENT=production` first
2. ✅ Updated `_init_supabase()` to prefer service role key
3. ✅ Added logging to track initialization
4. ✅ Deployed secrets via Secrets Manager
5. ✅ Redeployed backend with fixes

## Current Status

- **Backend Code**: Fixed and deployed
- **Secrets**: Deployed via Secrets Manager
- **Connection**: Still using in-memory storage (not connecting to Supabase)

## Next Steps

### Option 1: Check Cloud Run Logs
```bash
gcloud run services logs read ai-agent-factory-backend \
  --region us-central1 \
  --limit 100 | grep -i -E "(supabase|data manager|mode|production|development)"
```

Look for:
- "Initializing SimpleDataManager with mode:"
- "Connected to Supabase"
- "Failed to initialize Supabase"
- Any Supabase connection errors

### Option 2: Verify Secrets Are Accessible

Check if the service can access secrets:
```bash
# Check service configuration
gcloud run services describe ai-agent-factory-backend \
  --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)"
```

### Option 3: Add Debug Endpoint

Add a debug endpoint to check data manager status:
```python
@router.get("/api/v1/debug/data-manager")
async def debug_data_manager():
    return {
        "mode": data_manager.mode,
        "is_connected": data_manager.is_connected(),
        "has_supabase": data_manager.supabase is not None,
        "supabase_url": config.supabase_url[:30] + "..." if config.supabase_url else None,
        "supabase_key_set": bool(config.supabase_key or config.supabase_service_role_key)
    }
```

### Option 4: Force Production Mode

Set `DATA_MODE=production` explicitly in Cloud Run:
```bash
gcloud run services update ai-agent-factory-backend \
  --region us-central1 \
  --set-env-vars="DATA_MODE=production,ENVIRONMENT=production"
```

## Files Modified

1. ✅ `backend/fastapi_app/utils/simple_data_manager.py`
   - Updated `_get_data_mode()` to check ENVIRONMENT first
   - Updated `_init_supabase()` to use service role key
   - Added error handling and logging

## Testing

After fixing the connection:

1. **Verify Supabase Connection**:
   ```bash
   curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/debug/data-manager
   ```
   Should show: `"mode": "production"`, `"has_supabase": true`

2. **Test Database Write**:
   ```bash
   # Upload a PRD
   curl -X POST "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/upload" \
     -F "file=@prds/queue/2024-01-15_database-integration-supabase.md"
   
   # Check if it's in Supabase
   # SQL: SELECT COUNT(*) FROM prds;
   ```

3. **Test Duplicate Prevention**:
   ```bash
   # Upload same file twice - should return same ID
   ```

---

**Status**: Backend code is fixed, but connection to Supabase needs verification. Check logs to see why initialization is failing.

