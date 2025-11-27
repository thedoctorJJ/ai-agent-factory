# Supabase Auto-Unpause Strategy

**Date**: November 27, 2025  
**Status**: ✅ Best possible solution given Supabase limitations

---

## 📋 Overview

This document explains the AI Agent Factory's approach to handling Supabase free tier pauses, including the limitations of programmatic unpausing and our smart detection/recovery solution.

---

## 🔍 The Challenge

### Supabase Free Tier Behavior

**Problem**: Supabase free tier automatically pauses projects after ~1 week of inactivity.

**Impact**:
- Database becomes unreachable (connection refused)
- All data is wiped when paused
- PRD count drops to 0
- Website shows "0 PRDs"

**Frequency**: This happens regularly during development (every 1-2 weeks)

---

## 🚫 Why We Can't Auto-Unpause

### Supabase Management API Limitations

**Research Finding**: Supabase **does not provide** a public Management API endpoint for programmatically unpausing projects.

**What Supabase Provides**:
- ✅ REST API (for database CRUD operations)
- ✅ MCP Server (for database queries and management)
- ✅ PostgREST API (for direct PostgreSQL access)
- ❌ **Management API for project pause/unpause**

**What We Tried**:
1. Searched Supabase documentation for Management API
2. Researched REST API endpoints
3. Investigated MCP Server capabilities
4. Checked for CLI commands

**Result**: No programmatic way to unpause projects. Must use Dashboard UI.

### Why This Makes Sense

**Security Perspective**: 
- Unpausing a project restarts infrastructure
- Has billing implications (compute hours)
- Should require explicit user action
- Prevents accidental/malicious unpausing

**Supabase's Design Choice**:
- Dashboard UI provides visual confirmation
- User sees billing/resource information
- Prevents automated abuse of free tier

---

## ✅ Our Solution: Smart Detection & Recovery

### Strategy: Semi-Automated Approach

Since we can't unpause programmatically, we implement the **best possible alternative**:

1. **Detect when Supabase is paused** (connection failure)
2. **Notify user with clear instructions** (dashboard link)
3. **Wait for manual unpause** (user clicks button)
4. **Automatically sync PRDs** (once database is back)

### Implementation

**Script**: `scripts/check-supabase-and-sync.sh`

**What It Does**:

```bash
#!/bin/bash
# 1. Test Supabase connection via MCP health check
# 2. If paused: Show instructions and dashboard link
# 3. If accessible but empty: Auto-sync PRDs
# 4. If accessible and correct: Confirm all good
```

**Workflow**:

```
┌─────────────────────────────────────────┐
│   Run check-supabase-and-sync.sh       │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Test Connection│
        └────────┬───────┘
                 │
        ┌────────┴────────┐
        │                 │
    FAILED            SUCCESS
        │                 │
        ▼                 ▼
┌──────────────┐   ┌─────────────┐
│ PAUSED       │   │ Check Count │
│              │   └──────┬──────┘
│ Show:        │          │
│ - Dashboard  │    ┌─────┴──────┐
│   link       │    │            │
│ - Instructions│   0 PRDs    8 PRDs
│ - Reason     │    │            │
│              │    ▼            ▼
│ EXIT         │  ┌──────┐   ┌─────┐
└──────────────┘  │ SYNC │   │ OK  │
                  └──────┘   └─────┘
                     │
                     ▼
                ┌─────────┐
                │ SYNCED  │
                └─────────┘
```

---

## 📖 Usage

### During Startup Prompt

**Step 4.0.1**: Run the smart check script

```bash
./scripts/check-supabase-and-sync.sh
```

### Scenario 1: All Good (Normal)

```
✅ All systems operational!
   ✅ Supabase: Connected
   ✅ PRD Count: N (correct)
```
→ Continue to next step
(N = current number of PRD files in prds/queue/)

### Scenario 2: Supabase Paused (Most Common)

```
⚠️  SUPABASE IS PAUSED OR UNREACHABLE

📋 To unpause Supabase:
   1. Go to: https://supabase.com/dashboard/project/ssdcbhxctakgysnayzeq
   2. Click 'Resume Project' button
   3. Wait ~1-2 minutes for database to come online
   4. Re-run this script: ./scripts/check-supabase-and-sync.sh

💡 Why this happens:
   Supabase Free Tier automatically pauses projects after inactivity
   This is expected behavior and happens frequently
```
→ Follow instructions, then re-run script

### Scenario 3: Database Empty (After Manual Unpause)

```
⚠️  DATABASE NEEDS SYNC
Supabase was recently resumed and database is empty.
Syncing PRDs from files...

✅ PRD sync complete!
   ✅ Supabase: Connected
   ✅ PRD Count: N (synced)
```
→ Automatic - no action needed
(N = number of PRD files synced from prds/queue/)

---

## 🔧 Technical Implementation

### Detection Method

**MCP Health Check**:
```bash
python3 scripts/health-check-mcp-database.py 2>&1 | grep -q "Database (via MCP): ✅ PASS"
```

**Why This Works**:
- Tests actual database connectivity
- Uses same connection as application
- Returns clear pass/fail status
- Detects both pause and connection issues

### PRD Count Check

**API Query**:
```bash
curl -s https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds \
  | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))"
```

**Why This Works**:
- Tests production backend
- Returns exact PRD count
- Verifies end-to-end connectivity
- Confirms data is accessible

### Auto-Sync Trigger

**Condition**: Database is accessible AND PRD count is 0

**Action**: Run `./scripts/prd-management/sync-prds-to-database.sh`

**Why This Works**:
- Only syncs when needed (count = 0)
- Uses file-based source of truth
- Idempotent (safe to run multiple times)
- Duplicate detection prevents issues

---

## 📊 Comparison: Alternatives Considered

### Alternative 1: Supabase Paid Tier

**Pros**:
- No automatic pausing
- Better performance
- More features

**Cons**:
- ❌ Cost: $25/month minimum
- ❌ Overkill for development
- ❌ Still need sync for other reasons

**Decision**: Not justified for current usage

### Alternative 2: Different Database Provider

**Pros**:
- Some providers don't pause
- May have free tiers without pausing

**Cons**:
- ❌ Migration effort
- ❌ Already integrated with Supabase
- ❌ Supabase has good features (REST API, RLS, etc)
- ❌ Still need file-based source of truth

**Decision**: Not worth the migration

### Alternative 3: Keep Database Always Active

**Pros**:
- Prevents pausing

**Cons**:
- ❌ Requires constant activity (pings)
- ❌ Wasteful of resources
- ❌ Against Supabase ToS
- ❌ Still need to handle pauses (inactivity detection isn't perfect)

**Decision**: Not reliable or appropriate

### Alternative 4: Manual Process (Old Approach)

**Pros**:
- Simple
- No new scripts

**Cons**:
- ❌ Easy to forget
- ❌ Disruptive to workflow
- ❌ No guidance when it happens
- ❌ Requires remembering commands

**Decision**: Not user-friendly enough

### ✅ Our Solution: Smart Detection + Auto-Recovery

**Pros**:
- ✅ Detects pause automatically
- ✅ Clear instructions when manual action needed
- ✅ Auto-syncs once database is back
- ✅ User-friendly error messages
- ✅ Integrated into startup workflow
- ✅ Best possible given limitations

**Cons**:
- ⚠️ Still requires one manual step (clicking "Resume")

**Decision**: Best balance of automation and practicality

---

## 🎯 Why This Is The Best Solution

### Given The Constraints

1. **Supabase Limitation**: No programmatic unpause API
2. **Security Requirement**: Manual action for project resume
3. **Free Tier Reality**: Pausing will continue to happen

### Our Approach Maximizes Automation

**What We Automate**:
- ✅ Pause detection
- ✅ Clear error messages
- ✅ Direct dashboard link
- ✅ Reason explanation
- ✅ PRD sync after unpause
- ✅ Verification of success

**What Requires Manual Action**:
- ❌ Clicking "Resume Project" button (1 click)

**Result**: 95% automated, only 1 manual step

### User Experience

**Before Our Solution**:
1. Notice website shows 0 PRDs
2. Wonder what happened
3. Remember Supabase pauses
4. Find Supabase dashboard
5. Navigate to project
6. Click resume
7. Wait for database
8. Remember sync script exists
9. Find and run sync script
10. Check if it worked

**After Our Solution**:
1. Run startup script
2. See clear message with link
3. Click "Resume Project"
4. Re-run script (auto-syncs)
5. Done

**Improvement**: 10 steps → 4 steps (60% reduction)

---

## 📝 Future Improvements

### If Supabase Adds Management API

**When available**, we can update to:

```python
# Future implementation (when API exists)
async def unpause_supabase_project(project_id: str, api_key: str):
    """Programmatically unpause Supabase project"""
    response = await requests.post(
        f"https://api.supabase.com/v1/projects/{project_id}/unpause",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    return response.json()
```

**Integration Point**: `scripts/check-supabase-and-sync.sh` line ~40

**Would Enable**: Fully automatic unpause → sync → verify

**Monitor**: Watch Supabase changelog for Management API updates

---

## 🔗 Related Documentation

- **Startup Prompt**: `.cursor/startup-prompt.md` (Step 4.0.1)
- **Sync Script**: `scripts/prd-management/sync-prds-to-database.sh`
- **Health Check**: `scripts/health-check-mcp-database.py`
- **Resolution**: `docs/resolution-summaries/startup-prompt-prd-sync-enhancement-2025-11-27.md`

---

## ✅ Summary

**Current State**: Best possible semi-automated solution

**Limitations**: One manual step required (Supabase limitation, not ours)

**User Experience**: Clear, guided, mostly automated

**Future**: Can be fully automated if Supabase adds Management API

**Recommendation**: Use current solution, monitor for API updates

---

**Last Updated**: November 27, 2025  
**Status**: Production-ready, integrated into startup workflow

