# PRD Discovery Methodology

**Date**: November 16, 2025  
**Issue**: Incomplete PRD discovery process  
**Status**: ✅ **DOCUMENTED** - Methodology improved

---

## 📋 Problem

Initial PRD search only found 2 PRDs by searching for files, but a deeper search revealed 10 PRDs in the system. This indicates the discovery process was not comprehensive enough.

---

## 🔍 Root Cause Analysis

### **What Went Wrong**

1. **File-Only Search**: Initial search only looked for PRD files in the `prds/` directory
2. **Missed Database**: Didn't check the API/database to see what PRDs were actually stored
3. **Missed Scripts**: Didn't check for scripts that create PRDs programmatically
4. **Incomplete Documentation Review**: Didn't check README for PRD creation scripts

### **Why It Happened**

- Assumed PRDs only existed as files
- Didn't understand the dual storage system (files + database)
- Didn't check documentation for PRD creation methods
- Search was too narrow in scope

---

## ✅ Proper PRD Discovery Methodology

**🎯 PRINCIPLE: PRD files in the repository are the source of truth. The database is just storage.**

### **Step 1: Check PRD Files First (Source of Truth)**

**Always start by checking what PRD files exist in the repository:**

```bash
# Use the discovery script
./scripts/prd-management/discover-prds.sh

# Or manually find PRD files
find prds -name "*.md" -type f ! -name "README.md" ! -path "*/templates/*"
```

**Why**: PRD files in the repository are the authoritative source. The database is just a cache/storage mechanism.

### **Step 2: Sync Files to Database (If Needed)**

**If PRD files exist but aren't in the database, sync them:**

```bash
# Sync all PRD files to database
./scripts/prd-management/sync-prds-to-database.sh
```

**Why**: The database needs to be populated from the source files for the application to use them.

### **Step 3: Check Documentation**

**Look for PRD creation scripts and methods:**

```bash
# Search README for PRD-related information
grep -i "prd\|sample" README.md

# Check for PRD creation scripts
find scripts -name "*prd*" -type f
```

**Why**: Documentation often mentions how to create or populate PRDs.

### **Step 4: Check Scripts Directory**

**Look for scripts that create PRDs:**

```bash
# Find PRD-related scripts
find scripts -name "*prd*" -o -name "*sample*" | grep -i prd

# Check for sample data scripts
ls scripts/*sample*.py
```

**Why**: PRDs may be created programmatically via scripts.

### **Step 5: Check File System** (Already done in Step 1)

**Search for PRD files in the repository:**

```bash
# Find all PRD markdown files
find prds -name "*.md" -type f ! -name "README.md" ! -path "*/templates/*"

# Check all PRD directories
ls -la prds/*/
```

**Why**: PRDs may exist as files before being uploaded to the system.

### **Step 6: Check Templates**

**Review PRD templates to understand structure:**

```bash
# Check available templates
ls prds/templates/
cat prds/templates/prd-template-*.md
```

**Why**: Templates show what PRDs should look like and may indicate expected PRDs.

---

## 📊 Complete PRD Discovery Checklist

When searching for PRDs, always:

- [ ] **Check PRD Files** - Run `./scripts/prd-management/discover-prds.sh` (SOURCE OF TRUTH)
- [ ] **Sync to Database** - Run `./scripts/prd-management/sync-prds-to-database.sh` if needed
- [ ] **Check API/Database** - Query `/api/v1/prds` to verify what's loaded
- [ ] **Check Scripts** - Look for `create-sample-prds.py` or similar (creates files, not database entries)
- [ ] **Check Templates** - Review `prds/templates/` for structure
- [ ] **Check Documentation** - Review PRD system documentation
- [ ] **Check Changelog** - Look for PRD-related changes
- [ ] **Check Test Data** - Look in `tests/samples/` for test PRDs

---

## 🎯 Key Learnings

1. **Files are Source of Truth**: PRD files in the repository are authoritative. Database is just storage.
2. **Sync Process**: Files need to be synced to database for the application to use them
3. **Multiple Storage Locations**: PRDs exist as files (source) AND in database (cache)
4. **Scripts Create Files**: Scripts like `create-sample-prds.py` should create FILES first
5. **Discovery Script**: Use `discover-prds.sh` to find all PRD files and their sync status
6. **Comprehensive Search**: Check files first, then sync to database if needed

---

## 🔧 Recommended Improvements

### **For Future Searches**

1. **Start with Files**: Always check PRD files first using `discover-prds.sh`
2. **Sync When Needed**: Use `sync-prds-to-database.sh` to upload files to database
3. **Check Scripts**: Look for scripts that create PRD files (not database entries)
4. **Read Documentation**: Check README and guides for PRD file locations
5. **Verify Sync**: Check API to verify files are synced to database

### **For System Structure**

1. **Files as Source of Truth**: PRD files in repository are authoritative
2. **Database as Cache**: Database is just storage, populated from files
3. **Discovery Script**: `discover-prds.sh` finds all files and sync status
4. **Sync Script**: `sync-prds-to-database.sh` uploads files to database
5. **Documentation**: Clearly document that files are source of truth

---

## 📝 Example: Proper PRD Discovery

```bash
# 1. Discover PRD files (SOURCE OF TRUTH)
./scripts/prd-management/discover-prds.sh

# 2. Sync files to database if needed
./scripts/prd-management/sync-prds-to-database.sh

# 3. Verify what's in database
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds

# 4. Check for creation scripts (they should create FILES)
ls scripts/*prd*.py scripts/*sample*.py

# 5. Check README for PRD file locations
grep -i "prd\|sample" README.md
```

---

**Remember**: PRD files in the repository are the source of truth. The database is just storage. Always check files first!

