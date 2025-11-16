# Supabase DNS Resolution Issue

**Date**: November 16, 2025
**Status**: ✅ **RESOLVED** - Supabase project unpaused, DNS resolving correctly
**Impact**: Agent registration and database operations now working

---

## 🔍 Issue Summary

The Supabase URL configured in Google Cloud Secrets Manager (`https://ssdcbhxctakgysnayzeq.supabase.co`) is not resolving in DNS, causing all database operations to fail with `[Errno -2] Name or service not known` errors.

## 🐛 Root Cause

DNS lookup for `ssdcbhxctakgysnayzeq.supabase.co` returns `NXDOMAIN`, indicating the domain does not exist. This could mean:

1. **Supabase Project Deleted/Paused**: The Supabase project may have been deleted, paused, or suspended
2. **Incorrect URL**: The URL in the secret may be incorrect or outdated
3. **DNS Propagation**: Unlikely, but possible DNS propagation delay (though this would be unusual for a production domain)

## 📊 Evidence

### DNS Test Results
```bash
$ nslookup ssdcbhxctakgysnayzeq.supabase.co
Server:		2001:4860:4860::8844
Address:	2001:4860:4860::8844#53

** server can't find ssdcbhxctakgysnayzeq.supabase.co: NXDOMAIN
```

### Error Logs
```
httpx.ConnectError: [Errno -2] Name or service not known
```

### Current Configuration
- **Secret Name**: `SUPABASE_URL`
- **Value**: `https://ssdcbhxctakgysnayzeq.supabase.co`
- **Location**: Google Cloud Secrets Manager
- **Used By**: Cloud Run service `ai-agent-factory-backend`

## ✅ Solutions Implemented

### 1. Enhanced Error Handling
- Added retry logic with exponential backoff in `SimpleDataManager`
- Improved error messages to identify DNS/network issues
- Added connection testing during initialization

### 2. Better Logging
- More detailed error messages
- Clear indication of DNS resolution failures
- Retry attempt tracking

## 🔧 Required Actions

### Immediate Actions

1. **Verify Supabase Project Status**
   - Log into [Supabase Dashboard](https://supabase.com/dashboard)
   - Check if project `ssdcbhxctakgysnayzeq` exists
   - Verify project is active (not paused or deleted)

2. **Get Correct Supabase URL**
   - If project exists, get the correct URL from Supabase dashboard
   - Format should be: `https://[project-ref].supabase.co`
   - Verify the URL resolves in DNS

3. **Update Google Cloud Secret**
   ```bash
   # Update the SUPABASE_URL secret with correct value
   echo -n "https://[correct-project-ref].supabase.co" | \
     gcloud secrets versions add SUPABASE_URL --data-file=- \
     --project=agent-factory-474201
   ```

4. **Verify Supabase Keys**
   - Ensure `SUPABASE_KEY` (anon key) is correct
   - Ensure `SUPABASE_SERVICE_ROLE_KEY` is correct
   - Both should match the Supabase project

### If Project Doesn't Exist

1. **Create New Supabase Project**
   - Go to [Supabase Dashboard](https://supabase.com/dashboard)
   - Create a new project
   - Note the project URL and API keys

2. **Apply Database Schema**
   - Run `infra/database/schema.sql` in Supabase SQL Editor
   - Verify all tables are created

3. **Update All Secrets**
   ```bash
   # Update SUPABASE_URL
   echo -n "https://[new-project-ref].supabase.co" | \
     gcloud secrets versions add SUPABASE_URL --data-file=-
   
   # Update SUPABASE_KEY
   echo -n "[new-anon-key]" | \
     gcloud secrets versions add SUPABASE_KEY --data-file=-
   
   # Update SUPABASE_SERVICE_ROLE_KEY
   echo -n "[new-service-role-key]" | \
     gcloud secrets versions add SUPABASE_SERVICE_ROLE_KEY --data-file=-
   ```

4. **Restart Cloud Run Service**
   ```bash
   gcloud run services update ai-agent-factory-backend \
     --region=us-central1 \
     --project=agent-factory-474201
   ```

## 🧪 Verification Steps

After updating the Supabase URL:

1. **Test DNS Resolution**
   ```bash
   nslookup [new-project-ref].supabase.co
   # Should return valid IP addresses
   ```

2. **Test Supabase Connection**
   ```bash
   curl -H "apikey: [anon-key]" \
        -H "Authorization: Bearer [anon-key]" \
        "https://[new-project-ref].supabase.co/rest/v1/"
   # Should return 200 OK
   ```

3. **Test Backend Health**
   ```bash
   curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health
   # Should show Supabase connection as healthy
   ```

4. **Test Agent Registration**
   ```bash
   python3 scripts/register-redis-agent-production.py
   # Should successfully register the agent
   ```

## 📝 Code Changes

### Files Modified
- `backend/fastapi_app/utils/simple_data_manager.py`
  - Added retry logic with exponential backoff
  - Enhanced error handling for DNS/network errors
  - Added connection testing during initialization

### Improvements
- Better error messages identifying DNS issues
- Retry logic for transient network errors
- Connection validation during startup

## 🔗 Related Documentation

- [Supabase Setup Guide](../../docs/getting-started/03-setup-guide.md)
- [Deployment Guide](../../docs/deployment/06-deployment-guide.md)
- [Secrets Management](../../docs/security/SECRETS_MANAGEMENT.md)

## 📊 Impact

### Before Fix
- All database operations failing
- Agent registration impossible
- No clear error messages
- No retry logic

### After Fix (Code)
- Better error messages
- Retry logic for transient errors
- Clear identification of DNS issues

### After Fix (Configuration)
- Database operations working
- Agent registration successful
- System fully operational

## 🎯 Resolution

✅ **RESOLVED** - All steps completed:

1. ✅ Code improvements deployed
2. ✅ Supabase project status verified (was paused, now active)
3. ✅ Supabase URL confirmed correct (no changes needed)
4. ✅ Connectivity tested and verified
5. ✅ Agent registration successful

**Root Cause**: Supabase project was paused, causing DNS resolution to fail. After unpausing the project, all connectivity was restored.

**Final Status**: All systems operational. Redis agent successfully registered in AI Agent Factory.

