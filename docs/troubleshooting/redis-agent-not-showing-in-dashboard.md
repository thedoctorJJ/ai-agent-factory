# Redis Agent Not Showing in Dashboard - Fixed

**Date**: November 13, 2025  
**Status**: ✅ Fixed  
**Severity**: Medium (Dashboard display issue)  
**Affected Service**: Frontend Dashboard

## 📋 Summary

The Redis Caching Layer Agent was successfully created and registered in the database, but it was not appearing in the web app dashboard. The issue was caused by two problems:

1. **Agent Not Registered**: The agent existed but wasn't registered in the Supabase database
2. **Frontend Backend URL Mismatch**: The frontend Next.js config was pointing to an incorrect backend URL

## 🔍 Problem Description

### Symptoms
- Redis agent was deployed and running at `https://redis-caching-agent-fdqqqinvyq-uc.a.run.app`
- Agent health check was working correctly
- `/api/v1/agents` endpoint was returning empty array `[]`
- Dashboard showed "No agents found" despite agent being deployed

### Root Cause

**Issue 1: Agent Not in Database**
- The Redis agent was deployed but never registered in the Supabase `agents` table
- The agents endpoint correctly returned an empty array because no agents were in the database

**Issue 2: Frontend Backend URL Mismatch**
- The frontend `next.config.js` had an incorrect backend URL fallback
- Old URL: `https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app`
- Correct URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app`
- This would cause the frontend proxy to fail if the environment variable wasn't set

## ✅ Solution

### Step 1: Register the Redis Agent

Ran the registration script to add the agent to the database:

```bash
python3 scripts/register-redis-agent-production.py
```

**Result**: Agent successfully registered with ID `7d0c1e4d-c24c-49a7-81be-9ec8fb252fa5`

### Step 2: Fix Frontend Backend URL

Updated `frontend/next-app/next.config.js` to use the correct backend URL:

```javascript
// Before
? 'https://ai-agent-factory-backend-fdqqqinvyq-uc.a.run.app'

// After  
? 'https://ai-agent-factory-backend-952475323593.us-central1.run.app'
```

### Verification

After fixes:
- ✅ API endpoint returns agent: `GET /api/v1/agents` returns 1 agent
- ✅ Frontend proxy working: Frontend can fetch agent data
- ✅ Agent data structure correct: All fields properly formatted

## 🧪 Testing

### Before Fix
```bash
$ curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents
{"agents":[],"total":0,"page":1,"size":100,"has_next":false}
```

### After Fix
```bash
$ curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents
{
  "agents": [{
    "id": "7d0c1e4d-c24c-49a7-81be-9ec8fb252fa5",
    "name": "Redis Caching Layer Agent",
    ...
  }],
  "total": 1,
  ...
}
```

## 📝 Related Files

- **Fixed**: `frontend/next-app/next.config.js` - Updated backend URL
- **Script**: `scripts/register-redis-agent-production.py` - Agent registration script
- **Service**: `backend/fastapi_app/services/agent_service.py` - Agent creation service
- **Database**: Supabase `agents` table

## 🔄 Deployment

### Status
- ✅ Agent registered in database
- ✅ Frontend config updated
- ⏳ **Pending**: Frontend redeployment needed to pick up config change

### Deployment Steps
1. ✅ Registered Redis agent via production script
2. ✅ Updated frontend Next.js config with correct backend URL
3. ⏳ **Next**: Redeploy frontend to Google Cloud Run to apply config change

### Frontend Redeployment

The frontend needs to be rebuilt and redeployed for the config change to take effect:

```bash
# Build and deploy frontend
cd frontend/next-app
# Follow your frontend deployment process
```

## 📚 Lessons Learned

1. **Agent Registration**: Deployed agents must be explicitly registered in the database to appear in the dashboard
2. **URL Consistency**: Always verify backend URLs match across all configuration files
3. **Environment Variables**: Use environment variables for backend URLs to avoid hardcoded mismatches
4. **Testing**: Always test the full flow: deployment → registration → API → frontend display

## 🔗 Related Issues

- Agents endpoint was previously broken (see `agents-endpoint-internal-server-error.md`)
- This issue was discovered after fixing the agents endpoint

## 📅 Timeline

- **2025-11-13**: Issue discovered - Redis agent not showing in dashboard
- **2025-11-13**: Root cause identified - agent not registered + wrong backend URL
- **2025-11-13**: Agent registered successfully
- **2025-11-13**: Frontend config updated
- **2025-11-13**: Frontend redeployment pending

---

**Fixed By**: AI Assistant  
**Reviewed By**: Pending  
**Deployed**: Agent registered ✅, Frontend config updated ✅, Frontend redeployment pending ⏳

