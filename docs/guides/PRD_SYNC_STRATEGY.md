# PRD Sync Strategy

**Date**: November 16, 2025  
**Purpose**: How to keep PRD files and database in sync
**Status**: ✅ **IMPLEMENTED** - Files are source of truth, database is sync target

---

## 🎯 Sync Strategy Overview

### **Source of Truth: PRD Files in Repository**

**PRD files in `prds/queue/` are the source of truth.**

**Why**:
- ✅ Developer-friendly: Easy to edit markdown files
- ✅ Version controlled: Changes tracked in git
- ✅ Single source: One place to manage all PRDs
- ✅ Human readable: Markdown files are easy to review
- ✅ Portable: PRDs can be moved, copied, backed up as files

**Workflow**:
```
1. Update PRD files in repository (source of truth)
2. Sync to database (production)
3. Verify sync
```

---

## 📋 Update Order: Always Files First

### **Rule: Files → Database**

**Always update PRD files FIRST, then sync to database.**

**Why**:
- ✅ Files are source of truth
- ✅ Can review changes in git before syncing
- ✅ Version control tracks all changes
- ✅ Easy rollback if needed
- ✅ Multiple developers can work on files

---

## 🔄 Sync Workflow

### **When PRDs Change**

#### **Step 1: Update PRD Files** (Source of Truth)
```bash
# Edit PRD file
vim prds/queue/2024-11-16_my-prd.md

# Or create new PRD file
vim prds/queue/2024-11-16_new-feature.md
```

#### **Step 2: Sync to Database**
```bash
# Sync all PRD files to database
./scripts/prd-management/sync-prds-to-database.sh
```

#### **Step 3: Verify Sync**
```bash
# Verify PRDs are in sync
./scripts/prd-management/verify-prds-sync.sh
```

---

## 🔧 Sync Scripts

### **Script 1: Sync to Database** (`scripts/prd-management/sync-prds-to-database.sh`)

Syncs all PRD files from repository to database.

**What it does**:
- Reads PRD files from `prds/queue/`
- Checks if PRD exists in database (by title)
- Uploads missing PRDs via API
- Skips PRDs that are already loaded
- Reports what changed

**Usage**:
```bash
./scripts/prd-management/sync-prds-to-database.sh
```

**Note**: This script is automatically called by:
- GitHub Actions workflow (on push to main)
- Git post-commit hook (if installed, on local commits)

### **Script 2: Verify Sync** (`scripts/prd-management/verify-prds-sync.sh`)

Verifies that PRD files and database are in sync.

**What it does**:
- Compares PRD files with database PRDs
- Reports differences
- Shows which PRDs are out of sync
- Identifies duplicates

**Usage**:
```bash
./scripts/prd-management/verify-prds-sync.sh
```

### **Script 3: Setup Git Hook** (`scripts/prd-management/setup-prd-sync-hook.sh`)

Sets up automatic PRD syncing via git post-commit hook.

**What it does**:
- Creates `.git/hooks/post-commit` hook
- Automatically syncs PRDs when PRD files are committed
- Non-blocking (won't fail commit if sync fails)

**Usage**:
```bash
./scripts/prd-management/setup-prd-sync-hook.sh
```

**Disable**:
```bash
rm .git/hooks/post-commit
```

### **Script 4: Pull from Database** (`scripts/prd-management/create-prd-files-from-database.py`)

**Emergency only**: Creates PRD files from database (if files are lost).

**When to use**:
- PRD files are lost
- Need to recover from database backup
- Setting up new development machine

**Usage**:
```bash
python3 scripts/prd-management/create-prd-files-from-database.py
```

---

## 📊 Sync Scenarios

### **Scenario 1: New PRD Added**

**Workflow**:
1. Create PRD file in `prds/queue/YYYY-MM-DD_prd-title.md`
2. Sync to database: `./scripts/prd-management/sync-prds-to-database.sh`
3. Verify sync: `./scripts/prd-management/verify-prds-sync.sh`

### **Scenario 2: Existing PRD Updated**

**Workflow**:
1. Edit PRD file in `prds/queue/`
2. Sync to database: `./scripts/prd-management/sync-prds-to-database.sh`
3. Database will update existing PRD (by title match)
4. Verify sync: `./scripts/prd-management/verify-prds-sync.sh`

### **Scenario 3: PRD Removed**

**Workflow**:
1. Delete PRD file from `prds/queue/`
2. Sync to database: `./scripts/prd-management/sync-prds-to-database.sh`
3. Script will identify PRD as missing and can optionally delete from database
4. Verify sync: `./scripts/prd-management/verify-prds-sync.sh`

---

## 🔐 Important Rules

### **Never Update Database First**

**Why**:
- ❌ Loses source of truth
- ❌ Hard to track changes
- ❌ No version control
- ❌ Difficult to rollback

### **Always Update Files First**

**Why**:
- ✅ Source of truth maintained
- ✅ Changes tracked in git
- ✅ Easy to review before syncing
- ✅ Can collaborate on files

---

## 🤖 Proactive Syncing

### **Automatic Sync Mechanisms**

The AI Agent Factory includes **proactive syncing** to automatically keep PRDs in sync:

#### **1. GitHub Actions Workflow** (Production)
- **Location**: `.github/workflows/sync-prds.yml`
- **Triggers**: 
  - Automatically runs when PRD files in `prds/queue/` are pushed to `main` branch
  - Can be manually triggered via GitHub Actions UI
- **What it does**:
  - Syncs all PRD files to database
  - Verifies sync status
  - Reports results in GitHub Actions logs
- **Status**: ✅ **ACTIVE** - Automatically syncs on every PRD file change

#### **2. Git Post-Commit Hook** (Local Development)
- **Setup**: `./scripts/prd-management/setup-prd-sync-hook.sh`
- **Triggers**: Automatically runs after committing PRD files
- **What it does**:
  - Detects if PRD files were changed in the commit
  - Automatically syncs to database (non-blocking)
  - Provides feedback in terminal
- **Installation**:
  ```bash
  ./scripts/prd-management/setup-prd-sync-hook.sh
  ```
- **Disable**: `rm .git/hooks/post-commit`

#### **3. Manual Sync** (Always Available)
- **Command**: `./scripts/prd-management/sync-prds-to-database.sh`
- **Use when**: 
  - Need to sync immediately
  - Git hook not installed
  - Testing sync functionality

### **Sync Priority**
1. **GitHub Actions** (automatic on push to main) - Primary sync mechanism
2. **Git Hook** (automatic on commit) - Local development convenience
3. **Manual Sync** (on-demand) - Always available as fallback

---

## 📝 Best Practices

### **1. Regular Sync Checks**
```bash
# Weekly: Verify PRDs are in sync
./scripts/prd-management/verify-prds-sync.sh
```

### **2. After Any PRD Change**
- **Automatic**: GitHub Actions will sync when you push to main
- **Local**: Git hook will sync when you commit (if installed)
- **Manual**: `./scripts/prd-management/sync-prds-to-database.sh`

### **3. Before Major Deployments**
```bash
# Verify sync before deploying
./scripts/prd-management/verify-prds-sync.sh
```

### **4. Document PRD Changes**
- Update `CHANGELOG.md` when PRDs change
- Note why PRD was changed
- Document any agent impacts

---

## 🚨 Emergency Procedures

### **If PRD Files are Lost**

1. **Pull from Database** (if available):
   ```bash
   python3 scripts/prd-management/create-prd-files-from-database.py
   ```

2. **Review and Commit**:
   ```bash
   # Review created files
   git add prds/queue/
   git commit -m "Restore PRD files from database"
   ```

### **If Database PRDs are Corrupted**

1. **Sync from Files**:
   ```bash
   ./scripts/prd-management/sync-prds-to-database.sh
   ```

2. **Verify**:
   ```bash
   ./scripts/prd-management/verify-prds-sync.sh
   ```

---

## 📋 Summary

### **Update Order**
1. **Files First** (source of truth)
2. **Then Database** (production)

### **Sync Workflow**
1. Update PRD files in `prds/queue/`
2. Sync to database via API
3. Verify sync
4. Commit file changes to git

### **Key Principle**
**PRD files in repository are the source of truth. Database is a sync target.**

---

## 🔗 Related Documentation

- `docs/troubleshooting/file-based-prd-system.md` - File-based PRD system
- `docs/troubleshooting/prd-discovery-methodology.md` - PRD discovery process
- `scripts/prd-management/` - PRD management scripts

---

**Last Updated**: November 16, 2025

