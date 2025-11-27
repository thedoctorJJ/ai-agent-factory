# PRD Sync Strategy

**Date**: November 27, 2025 (Updated)  
**Purpose**: How PRDs flow from GitHub (cloud source of truth) to database and local files  
**Status**: ✅ **IMPLEMENTED** - GitHub is cloud source of truth, automatic sync to database

---

## 🎯 Sync Strategy Overview

### **Source of Truth: GitHub Repository (`prds/queue/`)**

**GitHub repository is the cloud source of truth for all PRDs.**

**Why GitHub (Not Local Files)**:
- ✅ **Cloud Persistent**: Survives local machine changes, database wipes
- ✅ **Always Accessible**: Available from any machine, any location
- ✅ **Version Controlled**: Complete history of all changes
- ✅ **Automated Sync**: GitHub Actions automatically updates database
- ✅ **External Submissions**: ChatGPT and other tools commit directly to GitHub
- ✅ **Collaborative**: Multiple developers can work simultaneously

**New Workflow**:
```
GitHub Repository (prds/queue/) ← CLOUD SOURCE OF TRUTH
       ↓
GitHub Actions (auto-triggered on push)
       ↓
Database (automatic sync within seconds)
       ↓
Website (shows PRDs immediately)

Local Development:
git pull → Local prds/queue/ (working copy)
```

---

## 📋 Update Order: GitHub First

### **Rule: GitHub → Database → Local**

**All PRD changes go through GitHub first.**

**Why**:
- ✅ GitHub is cloud-persistent (never lost)
- ✅ Automatic database sync (no manual steps)
- ✅ Website updates within seconds
- ✅ Version control tracks all changes
- ✅ Works from anywhere (not tied to local machine)

---

## 🔄 Sync Workflows

### **Method 1: Via ChatGPT (Recommended for New PRDs)**

```
1. Submit PRD via ChatGPT
2. MCP Server commits to GitHub automatically
3. GitHub Actions syncs to database automatically (30 seconds)
4. Website shows new PRD immediately
5. Later: git pull to sync locally (when needed)
```

**No manual steps required!**

### **Method 2: Manual GitHub Commit (For Direct Edits)**

#### **Step 1: Create/Edit PRD Locally**
```bash
# Edit existing PRD file
vim prds/queue/2024-11-16_my-prd.md

# Or create new PRD file
vim prds/queue/2024-11-16_new-feature.md
```

#### **Step 2: Commit to GitHub**
```bash
git add prds/queue/2024-11-16_my-prd.md
git commit -m "feat: Add new PRD for feature X"
git push origin main
```

#### **Step 3: Automatic Sync (No Action Needed)**
- GitHub Actions detects push to `prds/queue/`
- Automatically syncs to database
- Website updates within 30 seconds

### **Method 3: Local Sync (Development/Testing Only)**

```bash
# Manual local sync (if GitHub Actions unavailable)
./scripts/prd-management/sync-prds-to-database.sh
```

**Note**: This is a fallback. Normal workflow doesn't need this.

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

### **Never Update Database Directly**

**Why**:
- ❌ Bypasses GitHub (source of truth)
- ❌ Changes not version controlled
- ❌ Lost on database wipes
- ❌ No backup or history

### **Always Go Through GitHub**

**Why**:
- ✅ GitHub is cloud source of truth
- ✅ Automatic database sync via GitHub Actions
- ✅ Changes tracked in git
- ✅ Survives database wipes
- ✅ Available from anywhere

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
1. **GitHub First** (cloud source of truth)
2. **Automatic Database Sync** (via GitHub Actions)
3. **Local git pull** (when needed for development)

### **Sync Workflow**
1. PRD committed to GitHub (`prds/queue/`)
   - Via ChatGPT (automatic)
   - Via manual git commit
2. GitHub Actions triggers automatically
3. Database syncs within 30 seconds
4. Website shows new PRD immediately
5. `git pull` to sync locally (when needed)

### **Key Principle**
**GitHub repository is the cloud source of truth. Database and local files are derived from GitHub.**

---

## 🔗 Related Documentation

- `docs/troubleshooting/file-based-prd-system.md` - File-based PRD system
- `docs/troubleshooting/prd-discovery-methodology.md` - PRD discovery process
- `scripts/prd-management/` - PRD management scripts

---

**Last Updated**: November 16, 2025

