# PRD Management - Quick Reference

**Last Updated**: November 16, 2025

---

## 🎯 Key Principle

**PRD files in `prds/queue/` are the source of truth.**

**Always update files first, then sync to database.**

---

## 📋 Common Workflows

### **Add a New PRD**

```bash
# 1. Create PRD file
vim prds/queue/2024-11-16_new-feature.md

# 2. Sync to database
./scripts/prd-management/sync-prds-to-database.sh

# 3. Verify
./scripts/prd-management/verify-prds-sync.sh
```

### **Update an Existing PRD**

```bash
# 1. Edit PRD file
vim prds/queue/2024-11-16_existing-prd.md

# 2. Sync to database
./scripts/prd-management/sync-prds-to-database.sh

# 3. Verify
./scripts/prd-management/verify-prds-sync.sh
```

### **Verify PRDs are in Sync**

```bash
./scripts/prd-management/verify-prds-sync.sh
```

### **Emergency: Restore Files from Database**

```bash
# Only if PRD files are lost!
python3 scripts/prd-management/create-prd-files-from-database.py
```

---

## 🔄 Update Order

### **Always: Files → Database**

1. ✅ Update PRD files in `prds/queue/` (source of truth)
2. ✅ Sync to database via API
3. ✅ Verify sync
4. ✅ Commit file changes to git

### **Never: Database → Files** (except emergency)

- ❌ Don't update database first
- ❌ Don't use database as source of truth
- ✅ Only pull from database if files are lost

---

## 📊 Sync Status

### **Check Sync Status**
```bash
./scripts/prd-management/verify-prds-sync.sh
```

**Output**:
- ✅ In sync: PRD files match database
- ⚠️ Missing in database: PRD file not uploaded
- ⚠️ In database but no file: PRD in database without file
- ⚠️ Duplicates: Multiple PRDs with same title

---

## 🔧 Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `sync-prds-to-database.sh` | Sync files → database | After updating PRD files |
| `verify-prds-sync.sh` | Verify sync status | Check if files and database match |
| `discover-prds.sh` | Find all PRD files | Discover PRDs in repository |
| `create-prd-files-from-database.py` | Create files from database | Emergency recovery only |

---

## 📝 File Structure

```
prds/
└── queue/              # Source of truth (PRD files here)
    ├── 2024-01-15_database-integration-supabase.md
    ├── 2024-10-27_redis-caching-layer-agent.md
    └── ...
```

---

## ⚠️ Important Rules

1. **Files are Source of Truth**: Always edit PRD files, not database
2. **Sync After Changes**: Always run sync script after editing files
3. **Verify Regularly**: Check sync status weekly
4. **Commit Changes**: Commit PRD file changes to git

---

## 🔗 Related Documentation

- `docs/guides/PRD_SYNC_STRATEGY.md` - Full sync strategy
- `docs/troubleshooting/file-based-prd-system.md` - File-based system
- `scripts/prd-management/` - All PRD management scripts

---

**Remember**: Files are the source of truth. Database is just storage!

