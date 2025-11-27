# PRD Consistency System

**Date**: November 27, 2025  
**Purpose**: Ensure PRD count consistency across entire workflow with no duplicates  
**Status**: 🔨 **IN DESIGN**

---

## 🎯 Problem Statement

PRD count inconsistency has been a persistent issue:
- Duplicates created during sync
- Database count doesn't match file count
- Multiple sync processes running simultaneously
- No idempotency guarantees

**Root Cause**: No single source of identity across the system.

---

## ✅ Solution: Unique PRD Identification System

### **1. File-Based Identity (UUID from Content Hash)**

Every PRD gets a unique ID based on its **content hash**:

```python
import hashlib
import uuid

def generate_prd_id(title: str, description: str) -> str:
    """Generate deterministic UUID from PRD title and description"""
    content = f"{title.lower().strip()}:{description[:200].lower().strip()}"
    hash_bytes = hashlib.sha256(content.encode()).digest()
    return str(uuid.UUID(bytes=hash_bytes[:16]))
```

**Benefits**:
- ✅ Same content = Same ID (deterministic)
- ✅ Works across all systems
- ✅ No database lookup needed
- ✅ Prevents duplicates by design

---

### **2. Filename Convention with ID**

**New Format**: `YYYY-MM-DD_slug_UUID.md`

**Example**:
```
2025-11-27_weather-dashboard_a1b2c3d4-e5f6-7890-abcd-ef1234567890.md
```

**Benefits**:
- ✅ Filename itself prevents duplicates
- ✅ Easy to identify unique PRDs
- ✅ Git will show conflicts if duplicate exists

---

### **3. Database Uniqueness Constraints**

**Update Supabase Schema**:

```sql
-- Add unique constraint on content hash
ALTER TABLE prds ADD COLUMN content_hash VARCHAR(64) UNIQUE;

-- Create index for fast lookup
CREATE INDEX idx_prds_content_hash ON prds(content_hash);

-- Create index on title (normalized)
CREATE INDEX idx_prds_title_normalized ON prds(LOWER(TRIM(title)));
```

**Backend Enforcement**:
```python
async def create_prd(prd_data: PRDCreate):
    # Calculate content hash
    content_hash = calculate_content_hash(prd_data.title, prd_data.description)
    
    # Check if exists by hash
    existing = await db.get_prd_by_hash(content_hash)
    if existing:
        return existing  # Return existing, don't create duplicate
    
    # Create with hash
    prd_data.content_hash = content_hash
    return await db.insert_prd(prd_data)
```

---

### **4. GitHub Actions Idempotency**

**Update Workflow**:
```yaml
- name: Sync PRDs with Idempotency Check
  run: |
    # Only sync files changed in this commit
    CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r ${{ github.sha }} | grep '^prds/queue/')
    
    if [ -z "$CHANGED_FILES" ]; then
      echo "No PRD files changed, skipping sync"
      exit 0
    fi
    
    # Sync only changed files
    python3 scripts/prd-management/sync-changed-prds.py "$CHANGED_FILES"
```

**Benefits**:
- ✅ Only syncs what changed
- ✅ No full re-sync on every push
- ✅ Faster execution

---

### **5. Sync Process with Reconciliation**

**New Sync Script**: `sync-prds-with-reconciliation.py`

```python
def sync_with_reconciliation():
    """Sync PRDs with full reconciliation"""
    
    # 1. Get source of truth (GitHub)
    github_prds = get_prds_from_github()
    
    # 2. Get current database state
    db_prds = get_prds_from_database()
    
    # 3. Calculate differences
    github_ids = {prd.id for prd in github_prds}
    db_ids = {prd.id for prd in db_prds}
    
    to_add = github_ids - db_ids      # In GitHub, not in DB
    to_remove = db_ids - github_ids   # In DB, not in GitHub
    
    # 4. Reconcile
    for prd_id in to_add:
        upload_prd(github_prds[prd_id])
    
    for prd_id in to_remove:
        delete_prd(prd_id)
    
    # 5. Verify
    final_count = count_database_prds()
    assert final_count == len(github_prds), f"Count mismatch: {final_count} != {len(github_prds)}"
    
    return {
        "github_count": len(github_prds),
        "db_count": final_count,
        "added": len(to_add),
        "removed": len(to_remove),
        "status": "synced"
    }
```

---

### **6. MCP Server Changes**

**Update ChatGPT PRD Submission**:

```python
async def _submit_prd_from_conversation(self, arguments: Dict[str, Any]):
    # Parse content to extract title and description
    title, description = parse_prd_content(content)
    
    # Generate deterministic ID
    prd_id = generate_prd_id(title, description)
    
    # Generate filename with ID
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date_str}_{slug}_{prd_id}.md"
    
    # Check if file already exists in GitHub
    existing = await github.get_file(f"prds/queue/{filename}")
    if existing and "error" not in existing:
        return {
            "status": "exists",
            "message": "PRD already exists (duplicate content)",
            "file_path": f"prds/queue/{filename}",
            "prd_id": prd_id
        }
    
    # Commit to GitHub
    # ...rest of code
```

---

### **7. Health Check Endpoint**

**New Endpoint**: `/api/v1/prds/consistency-check`

```python
@router.get("/prds/consistency-check")
async def check_prd_consistency():
    """Check PRD consistency across all sources"""
    
    # Count in database
    db_count = await db.count_prds()
    
    # Count unique by content hash
    unique_count = await db.count_unique_prds_by_hash()
    
    # Get GitHub file count (if available)
    github_count = await github.count_prd_files() if github else None
    
    duplicates = db_count - unique_count
    
    return {
        "database_total": db_count,
        "database_unique": unique_count,
        "github_files": github_count,
        "duplicates": duplicates,
        "in_sync": db_count == unique_count and (github_count is None or db_count == github_count),
        "status": "healthy" if duplicates == 0 else "degraded"
    }
```

---

### **8. Automated Cleanup Job**

**Daily Cleanup Script**: `scripts/maintenance/cleanup-duplicate-prds.py`

```python
async def cleanup_duplicates():
    """Remove duplicate PRDs, keeping oldest by creation date"""
    
    # Find duplicates by content hash
    duplicates = await db.find_duplicate_prds()
    
    removed = 0
    for group in duplicates:
        # Keep the oldest
        keep = min(group, key=lambda p: p.created_at)
        to_remove = [p for p in group if p.id != keep.id]
        
        for prd in to_remove:
            await db.delete_prd(prd.id)
            removed += 1
    
    return {
        "removed": removed,
        "remaining": await db.count_prds()
    }
```

**Cron Job** (GitHub Actions):
```yaml
name: Daily PRD Cleanup
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup Duplicates
        run: python3 scripts/maintenance/cleanup-duplicate-prds.py
```

---

## 📊 Verification Points

### **At Every Stage**:

1. **ChatGPT Submission**
   - ✅ Generate content hash
   - ✅ Check if file exists in GitHub
   - ✅ Return existing if duplicate

2. **GitHub Commit**
   - ✅ Filename includes UUID
   - ✅ Git will reject if exact filename exists

3. **GitHub Actions**
   - ✅ Only sync changed files
   - ✅ Calculate hash before upload

4. **Database Insert**
   - ✅ Check content_hash uniqueness
   - ✅ Return existing if found
   - ✅ Unique constraint prevents duplicates

5. **Website Display**
   - ✅ Show consistency status
   - ✅ Alert if counts don't match

---

## 🔄 Migration Plan

### **Phase 1: Add Content Hash Column**
```bash
# 1. Update database schema
./scripts/setup/add-content-hash-column.sql

# 2. Backfill hashes for existing PRDs
python3 scripts/maintenance/backfill-content-hashes.py

# 3. Add unique constraint
./scripts/setup/add-unique-constraint.sql
```

### **Phase 2: Update All Code**
- Backend: Add hash calculation to PRD creation
- MCP Server: Include hash in GitHub commits
- Sync Scripts: Use hash for duplicate detection

### **Phase 3: Rename Existing Files**
```bash
# Add UUIDs to existing filenames
python3 scripts/maintenance/rename-prds-with-ids.py
```

### **Phase 4: Enable Verification**
- Deploy health check endpoint
- Add to startup prompt
- Enable daily cleanup job

---

## 🎯 Success Criteria

After implementation:
- ✅ GitHub file count = Database count (always)
- ✅ Zero duplicates in database
- ✅ Idempotent sync (can run multiple times safely)
- ✅ Content hash prevents duplicate submissions
- ✅ Health check shows "in_sync: true"

---

## 🚀 Implementation Priority

**High Priority** (Fix Now):
1. Add content_hash column to database
2. Update backend duplicate detection
3. Fix current duplicates

**Medium Priority** (This Week):
4. Update MCP server to use content hash
5. Add health check endpoint
6. Update sync scripts

**Low Priority** (Nice to Have):
7. Rename files with UUIDs
8. Daily cleanup job
9. Enhanced monitoring

---

**Status**: Ready for implementation. Should I proceed?

