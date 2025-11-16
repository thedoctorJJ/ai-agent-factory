# File-Based PRD System - Source of Truth

**Date**: November 16, 2025  
**Status**: ✅ **IMPLEMENTED** - Files are now the source of truth

---

## 🎯 Core Principle

**PRD files in the repository are the source of truth. The database is just storage.**

The database is an "appendage" - it's just a cache/storage mechanism for the application to use. All PRDs should exist as files first, then be synced to the database.

---

## 📁 File Structure

PRD files are organized in the `prds/` directory by status:

```
prds/
├── uploaded/          # PRDs uploaded by users
├── standardizing/     # PRDs being standardized
├── review/            # PRDs awaiting review
├── queue/             # PRDs ready for processing (MOST COMMON)
├── in-progress/       # PRDs being processed
├── completed/         # Successfully completed PRDs
├── failed/            # Failed PRDs
├── archive/           # Archived PRDs
└── templates/         # PRD templates
```

**File Naming Convention**: `YYYY-MM-DD_prd-title.md`

---

## 🔧 Available Tools

### **1. Discover PRD Files**

Find all PRD files and check their sync status:

```bash
./scripts/prd-management/discover-prds.sh
```

**What it does**:
- Finds all PRD files in `prds/` directory
- Checks if each file is loaded in the database
- Reports sync status

### **2. Sync Files to Database**

Upload PRD files to the database:

```bash
./scripts/prd-management/sync-prds-to-database.sh
```

**What it does**:
- Finds all PRD files
- Checks if they're in the database
- Uploads missing PRDs via API
- Skips PRDs that are already loaded

### **3. Create Files from Database**

If PRDs exist in database but not as files, create files:

```bash
python3 scripts/prd-management/create-prd-files-from-database.py
```

**What it does**:
- Fetches all PRDs from database
- Creates markdown files for PRDs that don't have files
- Ensures files become the source of truth

### **4. Create Sample PRD Files**

Create sample PRD files (not database entries):

```bash
python3 scripts/create-sample-prds-files.py
```

**What it does**:
- Creates PRD markdown files from sample data
- Files can then be synced to database if needed

---

## 🔄 Workflow

### **Creating a New PRD**

1. **Create PRD File**:
   ```bash
   # Create file in appropriate directory
   vim prds/queue/2024-11-16_my-new-prd.md
   ```

2. **Sync to Database**:
   ```bash
   ./scripts/prd-management/sync-prds-to-database.sh
   ```

### **Finding PRDs**

1. **Discover Files** (source of truth):
   ```bash
   ./scripts/prd-management/discover-prds.sh
   ```

2. **Check Database** (what's loaded):
   ```bash
   curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds
   ```

### **Updating a PRD**

1. **Edit the File**:
   ```bash
   vim prds/queue/2024-11-16_my-prd.md
   ```

2. **Re-sync to Database**:
   ```bash
   ./scripts/prd-management/sync-prds-to-database.sh
   ```

---

## 📊 Current Status

**PRD Files**: 9 files in `prds/queue/`
**In Database**: 9 PRDs loaded
**Sync Status**: ✅ All files synced

---

## 🎯 Benefits

1. **Version Control**: PRD files are in git, so changes are tracked
2. **Source of Truth**: Files are authoritative, database is just storage
3. **Portability**: PRDs can be moved, copied, backed up as files
4. **Human Readable**: PRDs are markdown files, easy to read and edit
5. **Separation of Concerns**: Files for storage, database for application use

---

## ⚠️ Important Notes

1. **Always Edit Files**: Don't edit PRDs directly in the database
2. **Sync After Changes**: Always sync files to database after editing
3. **Check Sync Status**: Use `discover-prds.sh` to verify sync
4. **Files First**: Create files first, then sync to database

---

**Remember**: Files are the source of truth. Database is just storage!

