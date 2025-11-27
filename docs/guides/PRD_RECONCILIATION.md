# PRD Reconciliation System

## Overview

The PRD Reconciliation System ensures that **GitHub always wins** as the source of truth. The database automatically syncs to match GitHub in all scenarios: additions, deletions, and content updates.

## The Golden Rule

```
📌 GitHub is ALWAYS the source of truth
    ↓
🔄 Database syncs TO match GitHub (automatically)
    ↓
🌐 Website reflects Database
    ↓
💻 Local syncs FROM GitHub (via git pull)
```

## What Gets Reconciled

### ✅ **1. Additions (PRD in GitHub, not in Database)**
- **Detection**: PRD file exists in `prds/queue/` but not in database
- **Action**: Uploads PRD to database
- **Example**: You commit a new PRD to GitHub → Auto-added to database

### ✅ **2. Deletions (PRD in Database, not in GitHub)**
- **Detection**: PRD exists in database but file deleted from `prds/queue/`
- **Action**: Deletes PRD from database
- **Example**: You delete a PRD file from GitHub → Auto-deleted from database

### ✅ **3. Updates (Content Changed in GitHub)**
- **Detection**: PRD file content differs from database version
- **Action**: Replaces database version with GitHub version
- **Example**: You edit a PRD in GitHub → Database updated with new content

### ⚠️ **4. Duplicates in GitHub (Same Title)**
- **Detection**: Multiple files with identical titles
- **Action**: Only first one is added to database
- **Manual Fix Required**: Delete duplicate files from GitHub

## How It Works

### Automatic Reconciliation (GitHub Actions)

**Trigger**: Any push to `prds/queue/` folder
**Time**: Within 30 seconds
**Workflow**: `.github/workflows/sync-prds.yml`

```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'prds/queue/**'
```

### Manual Reconciliation (Testing/Fallback)

```bash
python3 scripts/prd-management/reconcile-prds.py
```

## Reconciliation Process

```
Step 1: Remove Orphaned PRDs
├─ Compare database PRDs to GitHub files
├─ Delete any PRD in database not in GitHub
└─ Reports: "Deleted: X PRD(s)"

Step 2: Add Missing PRDs
├─ Compare GitHub files to database PRDs
├─ Upload any PRD in GitHub not in database
└─ Reports: "Added: X PRD(s)"

Step 3: Update Changed PRDs (NEW)
├─ Compare file content for matching titles
├─ Detect content differences
├─ Delete old version + Upload new version
└─ Reports: "Updated: X PRD(s)"

Verification
├─ Count PRDs in GitHub vs Database
└─ Confirm they match exactly
```

## Example Scenarios

### Scenario 1: Edit PRD Content

**Action**:
```bash
# Edit the file in GitHub (or locally then push)
vim prds/queue/2025-11-27_weather-dashboard.md
git add prds/queue/2025-11-27_weather-dashboard.md
git commit -m "Update Weather Dashboard requirements"
git push origin main
```

**Result**:
```
🔄 Step 3: Updating PRDs where content differs...
   🔍 'Weather Dashboard' has different content - updating from GitHub
   ✅ Deleted: Weather Dashboard (old version)
   ✅ Added: Weather Dashboard (new version)
   ✅ Updated: Weather Dashboard

✅ Database now has updated content from GitHub
```

### Scenario 2: Delete PRD

**Action**:
```bash
git rm prds/queue/2025-11-27_old-prd.md
git commit -m "Remove obsolete PRD"
git push origin main
```

**Result**:
```
🗑️  Step 1: Removing PRDs not in GitHub...
   🔍 'Old PRD' exists in database but not in GitHub
   ✅ Deleted: Old PRD

✅ Database cleaned up automatically
```

### Scenario 3: Add New PRD

**Action**:
```bash
# Create new PRD file
echo "# New Feature\n\n## Description\n..." > prds/queue/2025-11-27_new-feature.md
git add prds/queue/2025-11-27_new-feature.md
git commit -m "Add new feature PRD"
git push origin main
```

**Result**:
```
➕ Step 2: Adding missing PRDs from GitHub...
   🔍 'New Feature' exists in GitHub but not in database
   ✅ Added: New Feature (ID: abc-123)

✅ New PRD appears on website within 30 seconds
```

### Scenario 4: Duplicate Files in GitHub

**Action**:
```bash
# Accidentally created duplicates
ls prds/queue/
  2025-11-27_weather-dashboard.md
  2025-11-27_weather-dashboard-copy.md  # Duplicate!
```

**Result**:
```
➕ Step 2: Adding missing PRDs from GitHub...
   🔍 'Weather Dashboard' exists in GitHub but not in database
   ✅ Added: Weather Dashboard (ID: abc-123)
   
⚠️  Only 1 of 2 files added (both have same title)

Manual fix needed:
git rm prds/queue/2025-11-27_weather-dashboard-copy.md
git commit -m "Remove duplicate PRD"
git push
```

## Monitoring & Verification

### Check Reconciliation Status

```bash
# View GitHub Actions logs
https://github.com/thedoctorJJ/ai-agent-factory/actions

# Manual reconciliation (local)
python3 scripts/prd-management/reconcile-prds.py
```

### Verify Sync Status

```bash
# Count PRDs in each location
echo "GitHub: $(ls prds/queue/*.md | grep -v README | wc -l)"
echo "Database: $(curl -s https://[backend]/api/v1/prds | jq '.total')"
echo "Local: $(ls prds/queue/*.md | grep -v README | wc -l)"

# Should all be the same number
```

### Check for Duplicates

```bash
# Check database for duplicate titles
curl -s https://[backend]/api/v1/prds | \
  jq '.prds | group_by(.title) | map(select(length > 1))'

# Check GitHub for duplicate filenames
cd prds/queue/
for file in *.md; do echo "$file"; head -1 "$file"; done | grep -A1 "^#"
```

## Configuration

### Environment Variables

```bash
# Backend URL (for manual reconciliation)
export BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"
```

### GitHub Actions Settings

Located in `.github/workflows/sync-prds.yml`:
- Triggers on `prds/queue/` changes
- Uses Python 3.11
- Requires `requests` package
- Runs reconciliation script

## Troubleshooting

### Problem: Database Has Extra PRDs

**Symptom**: Database count > GitHub file count

**Cause**: Orphaned PRDs not cleaned up

**Fix**:
```bash
python3 scripts/prd-management/reconcile-prds.py
# Will delete orphaned PRDs automatically
```

### Problem: Database Missing PRDs

**Symptom**: Database count < GitHub file count

**Cause**: Sync failed or PRD files not processed

**Fix**:
```bash
python3 scripts/prd-management/reconcile-prds.py
# Will add missing PRDs automatically
```

### Problem: Outdated Content in Database

**Symptom**: Website shows old version of PRD

**Cause**: Content updated in GitHub but database not updated

**Fix**:
```bash
python3 scripts/prd-management/reconcile-prds.py
# Will detect content difference and update automatically
```

### Problem: Duplicates in GitHub

**Symptom**: Multiple files with same title

**Cause**: Manual file creation or ChatGPT submitted twice

**Fix**:
```bash
# Manually remove duplicate files
git rm prds/queue/duplicate-file.md
git commit -m "Remove duplicate PRD"
git push
```

## Summary: GitHub Always Wins

| Scenario | GitHub | Database Before | Database After | Auto-Fixed? |
|----------|--------|-----------------|----------------|-------------|
| **New PRD added to GitHub** | Has file | Missing | Added | ✅ Yes (30s) |
| **PRD deleted from GitHub** | No file | Has PRD | Deleted | ✅ Yes (30s) |
| **PRD content updated in GitHub** | Updated | Old version | Updated | ✅ Yes (30s) |
| **Duplicate files in GitHub** | 2 files | 0 or 1 | 1 | ⚠️ Manual cleanup |
| **PRD only in Database** | No file | Has PRD | Deleted | ✅ Yes (30s) |

**Bottom Line**: Make changes in GitHub, everything else syncs automatically. GitHub is the complete source of truth for ALL operations.

## Related Documentation

- `docs/resolution-summaries/2025-11-27-prd-reconciliation-system.md` - Implementation details
- `docs/guides/PRD_SYNC_STRATEGY.md` - Sync strategy overview
- `docs/guides/CHATGPT_PRD_WORKFLOW.md` - ChatGPT integration
- `.cursor/startup-prompt.md` - Daily workflow reference

