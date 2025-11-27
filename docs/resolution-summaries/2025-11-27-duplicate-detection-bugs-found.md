# Duplicate Detection System - Bugs Found During Testing
**Date**: November 27, 2025  
**Status**: ⚠️ Issues Identified - Needs Fixing

## Test Summary

Attempted end-to-end test of PRD duplicate prevention and bidirectional sync system.

**Test Plan:**
1. Establish baseline (9 PRDs across all 4 locations)
2. Create new PRD via ChatGPT
3. Verify it appears in all locations
4. Delete from website
5. Verify it's removed from all locations

**Result:** Test failed at step 2 - revealed multiple critical bugs

## Bugs Discovered

### Bug 1: Duplicate Prevention Not Enforcing in Database

**What Should Happen:**
- Backend calculates content_hash
- Checks database for existing hash
- If found: Returns existing PRD
- If not found: Creates new PRD

**What Actually Happens:**
- Backend calculates content_hash ✅
- Backend checks database ✅
- Backend creates new PRD anyway ❌ (doesn't respect the check)

**Evidence:**
- Started with 9 PRDs
- Submitted 1 new PRD via ChatGPT
- Ended with 18 PRDs (9 duplicates created)
- Next reconciliation attempt: 26 PRDs (more duplicates)

**Location:** `backend/fastapi_app/services/prd_service.py` - `create_prd()` method

### Bug 2: Reconciliation Creating Duplicates Instead of Preventing

**What Should Happen:**
- List PRDs in GitHub (9 files)
- List PRDs in database
- Add missing PRDs (1 per title)
- Remove orphaned PRDs

**What Actually Happens:**
- Lists PRDs correctly ✅
- Adds PRDs but doesn't check if they already exist ❌
- Creates duplicates on every run ❌
- Orphan detection works ✅

**Evidence:**
```
Run 1: Database 0 → 9 PRDs (correct)
Run 2: Database 9 → 18 PRDs (9 duplicates)
Run 3: Database 18 → 26 PRDs (8 more duplicates)
```

**Location:** `scripts/prd-management/reconcile-prds.py` - missing duplicate check in add phase

### Bug 3: Database DELETE Not Working

**What Should Happen:**
- `DELETE FROM prds;` removes all records
- Returns rows_affected count

**What Actually Happens:**
- SQL executes "successfully"
- Returns rows_affected: 0
- PRDs remain in database

**Evidence:**
```bash
# Via MCP SQL
DELETE FROM prds;  # Returns: success, rows_affected: 0

# Via backend API
curl -X DELETE /api/v1/prds  # Returns: "All PRDs cleared"

# Check count
curl /api/v1/prds  # Still returns: total: 26
```

**Possible Causes:**
- RLS (Row Level Security) policies blocking deletes
- Different database connections seeing different data
- Transaction not committing
- Multiple database instances

### Bug 4: Content Hash Check Logic Incorrect

**What Should Happen:**
```python
content_hash = calculate_prd_hash(title, description)
existing = await get_prd_by_hash(content_hash)
if existing:
    return existing  # Don't create duplicate
# else: create new
```

**What Actually Happens:**
- Hash calculated correctly ✅
- Query runs ✅
- Returns existing PRD ✅
- **But then creates new PRD anyway** ❌

**Location:** `backend/fastapi_app/services/prd_service.py` lines 30-50

### Bug 5: MCP Duplicate Check False Positive

**What Happened:**
- ChatGPT submitted "User Profile Management"
- MCP server returned: "duplicate_prevented"
- **But file doesn't exist in GitHub** ❌

**Evidence:**
```json
{
  "status": "duplicate_prevented",
  "existing_file": "2025-11-27_user-profile-management.md",
  "existing_path": "prds/queue/2025-11-27_user-profile-management.md"
}
```

But:
```bash
ls prds/queue/2025-11-27_user-profile-management.md
# File not found
```

**Possible Causes:**
- MCP server checking database instead of GitHub
- Caching issue
- Wrong repo being checked

## Impact

**Current System State:**
- ❌ Database has 26+ duplicate PRDs
- ❌ Cannot create new PRDs reliably
- ❌ Cannot test deletion flow (database too polluted)
- ❌ Duplicate prevention NOT working
- ⚠️ Website showing incorrect data

**What Still Works:**
- ✅ Content hash calculation (prd_hash.py)
- ✅ GitHub file operations (MCP server)
- ✅ Backend API responses (endpoints work)
- ✅ Reconciliation orphan detection

## Root Causes

### 1. Duplicate Detection Not Enforced

The code checks for duplicates but doesn't prevent creation:

```python
# Current (BROKEN)
existing_prd = await data_manager.get_prd_by_hash(content_hash)
if existing_prd:
    print("Duplicate found")  # Logs but doesn't return
    # Falls through and creates anyway!

prd_id = str(uuid.uuid4())  # Creates new PRD
```

**Should be:**
```python
existing_prd = await data_manager.get_prd_by_hash(content_hash)
if existing_prd:
    print("Duplicate found")
    return PRDResponse(**existing_prd)  # RETURN HERE!

# Only reached if NOT duplicate
prd_id = str(uuid.uuid4())
```

### 2. Reconciliation No Duplicate Check

Reconciliation adds PRDs without checking if they already exist:

```python
# Current (BROKEN)
for github_title in github_prds:
    if github_title not in db_prds:  # Only checks title
        upload_prd(file)  # Uploads even if hash matches
```

**Should be:**
```python
for github_title in github_prds:
    if github_title not in db_prds:
        # Check content hash before upload
        if not prd_exists_by_hash(github_file):
            upload_prd(file)
```

### 3. Database Connection Issues

Multiple systems accessing database differently:
- Backend API (via data_manager)
- MCP server (via Supabase service)
- Reconciliation script (via API calls)

They may be seeing different data or not committing transactions properly.

## Fixes Needed

### Priority 1: Fix Duplicate Detection in Backend

**File:** `backend/fastapi_app/services/prd_service.py`

**Change:**
```python
async def create_prd(self, prd_data: PRDCreate) -> PRDResponse:
    content_hash = calculate_prd_hash(prd_data.title, prd_data.description)
    existing_prd = await data_manager.get_prd_by_hash(content_hash)
    
    if existing_prd:
        print(f"⚠️  DUPLICATE DETECTED - Returning existing PRD")
        # MUST RETURN HERE - DON'T FALL THROUGH!
        if isinstance(existing_prd.get("created_at"), str):
            existing_prd["created_at"] = datetime.fromisoformat(...)
        if isinstance(existing_prd.get("updated_at"), str):
            existing_prd["updated_at"] = datetime.fromisoformat(...)
        return PRDResponse(**existing_prd)  # ← ADD THIS RETURN!
    
    # Only create if no duplicate found
    prd_id = str(uuid.uuid4())
    # ... rest of creation logic
```

### Priority 2: Fix Reconciliation Duplicate Check

**File:** `scripts/prd-management/reconcile-prds.py`

**Add hash-based checking:**
```python
# Before uploading, check if content hash already exists
async def should_add_prd(github_file, db_prds):
    content_hash = calculate_file_hash(github_file)
    for db_prd in db_prds.values():
        if db_prd.get("content_hash") == content_hash:
            return False  # Already exists by content
    return True  # Safe to add
```

### Priority 3: Fix Database DELETE

**Investigation needed:**
1. Check RLS policies on `prds` table
2. Verify database connection has proper permissions
3. Test with direct psql connection
4. Check if transactions are committing

**SQL to check RLS:**
```sql
SELECT * FROM pg_policies WHERE tablename = 'prds';
```

### Priority 4: Add Database Cleanup Script

**Create:** `scripts/maintenance/clean-duplicate-prds.py`

```python
# Remove duplicates keeping only the first occurrence per content_hash
# GROUP BY content_hash and DELETE all but MIN(id)
```

## Testing Plan (After Fixes)

1. **Clean slate:**
   - Manually clear database via Supabase dashboard
   - Verify 0 PRDs in database

2. **Resync from GitHub:**
   - Run reconciliation
   - Verify 9 PRDs (no duplicates)

3. **Test duplicate prevention:**
   - Submit "Weather Dashboard" via ChatGPT (already exists)
   - Should get: "duplicate_prevented"
   - Verify: Still 9 PRDs

4. **Test new PRD creation:**
   - Submit "User Profile Management" via ChatGPT (truly new)
   - Should get: "status: ok"
   - Verify: Now 10 PRDs in all locations

5. **Test deletion:**
   - Delete "User Profile Management" from website
   - Verify: Removed from GitHub
   - Verify: Back to 9 PRDs

## Lessons Learned

1. **Don't skip early testing** - Built 3 layers of duplicate prevention but never tested until end
2. **Test with real data early** - Would have caught the "check but don't enforce" bug immediately
3. **Database state is critical** - Need better database reset/cleanup tools
4. **Multiple connections = multiple truths** - Need consistent database access pattern
5. **Logging isn't enforcement** - Code that logs "duplicate found" but creates anyway is worse than no check

## Next Steps

1. Fix Priority 1 (duplicate detection enforcement)
2. Deploy fixed backend
3. Clear database manually via Supabase dashboard
4. Re-run full test plan
5. Fix remaining issues as discovered

## Related Files

- `backend/fastapi_app/services/prd_service.py` - Duplicate detection (BROKEN)
- `backend/fastapi_app/utils/prd_hash.py` - Hash calculation (WORKS)
- `scripts/prd-management/reconcile-prds.py` - Reconciliation (CREATES DUPES)
- `scripts/mcp/cursor-agent-mcp-server.py` - MCP duplicate check (FALSE POSITIVE)
- `docs/guides/DUPLICATE_PREVENTION.md` - Documentation (describes what SHOULD work)
- `docs/guides/PRD_RECONCILIATION.md` - Reconciliation docs (describes what SHOULD work)

---

**Status:** System needs significant debugging before production use. Core concepts are sound but implementation has critical bugs.

