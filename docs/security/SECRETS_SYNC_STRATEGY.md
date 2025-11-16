# Secrets Sync Strategy

**Date**: November 16, 2025  
**Purpose**: How to keep local encrypted storage and Google Cloud Secrets Manager in sync

---

## 🎯 Sync Strategy Overview

### **Source of Truth: Local Encrypted Storage**

**Local encrypted storage (`config/api-secrets.enc`) is the source of truth.**

**Why**:
- ✅ Developer-friendly: Easy to update locally
- ✅ Version controlled workflow: Changes tracked in git (encrypted file)
- ✅ Single source: One place to manage all secrets
- ✅ Backup: Encrypted file can be backed up easily

**Workflow**:
```
1. Update local encrypted storage (source of truth)
2. Sync to Google Cloud Secrets Manager (production)
3. Verify sync
```

---

## 📋 Update Order: Always Local First

### **Rule: Local → Production**

**Always update local encrypted storage FIRST, then sync to production.**

**Why**:
- ✅ Local is source of truth
- ✅ Can test locally before deploying
- ✅ Version control tracks changes
- ✅ Easy rollback if needed

---

## 🔄 Sync Workflow

### **When Secrets Change**

#### **Step 1: Update Local Storage** (Source of Truth)
```bash
# Option A: Import from file
python3 config/secure-api-manager.py import config/env/.env.local

# Option B: Manual update (edit .env.local, then import)
# Edit config/env/.env.local
python3 config/secure-api-manager.py import config/env/.env.local
```

#### **Step 2: Sync to Production**
```bash
# Sync all secrets to Google Cloud Secrets Manager
./scripts/sync-secrets-to-cloud.sh
```

#### **Step 3: Verify Sync**
```bash
# Verify secrets are in sync
./scripts/verify-secrets-sync.sh
```

---

## 🔧 Sync Scripts

### **Script 1: Sync to Cloud** (`scripts/sync-secrets-to-cloud.sh`)

Syncs all secrets from local encrypted storage to Google Cloud Secrets Manager.

**What it does**:
- Reads from `config/secure-api-manager.py`
- Updates existing secrets or creates new ones
- Preserves version history in Secrets Manager
- Reports what changed

**Usage**:
```bash
./scripts/sync-secrets-to-cloud.sh
```

### **Script 2: Verify Sync** (`scripts/verify-secrets-sync.sh`)

Verifies that local and cloud secrets are in sync.

**What it does**:
- Compares local secrets with cloud secrets
- Reports differences
- Shows which secrets are out of sync

**Usage**:
```bash
./scripts/verify-secrets-sync.sh
```

### **Script 3: Pull from Cloud** (`scripts/pull-secrets-from-cloud.sh`)

**Emergency only**: Pulls secrets from cloud to local (if local is lost).

**When to use**:
- Local encrypted file is lost
- Need to recover from cloud backup
- Setting up new development machine

**Usage**:
```bash
./scripts/pull-secrets-from-cloud.sh
```

---

## 📊 Sync Scenarios

### **Scenario 1: New Secret Added**

**Workflow**:
1. Add secret to `config/env/.env.local`
2. Import to local encrypted storage: `python3 config/secure-api-manager.py import config/env/.env.local`
3. Sync to cloud: `./scripts/sync-secrets-to-cloud.sh`
4. Grant access: `./scripts/grant-secret-access.sh` (if new secret)
5. Update Cloud Run: `./scripts/deploy-with-secrets.sh` (if needed)

### **Scenario 2: Existing Secret Updated**

**Workflow**:
1. Update secret in `config/env/.env.local`
2. Import to local encrypted storage: `python3 config/secure-api-manager.py import config/env/.env.local`
3. Sync to cloud: `./scripts/sync-secrets-to-cloud.sh`
4. Cloud Run automatically uses latest version (if using `:latest`)

### **Scenario 3: Secret Rotated (e.g., API key expired)**

**Workflow**:
1. Get new secret value
2. Update in `config/env/.env.local`
3. Import to local: `python3 config/secure-api-manager.py import config/env/.env.local`
4. Sync to cloud: `./scripts/sync-secrets-to-cloud.sh`
5. Verify: `./scripts/verify-secrets-sync.sh`
6. Test: Check health endpoint

### **Scenario 4: Secret Removed**

**Workflow**:
1. Remove from `config/env/.env.local`
2. Import to local: `python3 config/secure-api-manager.py import config/env/.env.local`
3. **Don't delete from cloud** (keep for history/rollback)
4. Remove from Cloud Run service if no longer needed

---

## 🔐 Security Considerations

### **Never Update Cloud First**

**Why**:
- ❌ Loses source of truth
- ❌ Hard to track changes
- ❌ No version control
- ❌ Difficult to rollback

### **Always Update Local First**

**Why**:
- ✅ Source of truth maintained
- ✅ Changes tracked in git
- ✅ Easy to test locally
- ✅ Can review before deploying

---

## 📝 Best Practices

### **1. Regular Sync Checks**
```bash
# Weekly: Verify secrets are in sync
./scripts/verify-secrets-sync.sh
```

### **2. After Any Secret Change**
```bash
# Always sync after updating local secrets
./scripts/sync-secrets-to-cloud.sh
```

### **3. Before Major Deployments**
```bash
# Verify sync before deploying
./scripts/verify-secrets-sync.sh
```

### **4. Document Secret Changes**
- Update `CHANGELOG.md` when secrets change
- Note why secret was changed
- Document any service impacts

---

## 🚨 Emergency Procedures

### **If Local Storage is Lost**

1. **Pull from Cloud** (if available):
   ```bash
   ./scripts/pull-secrets-from-cloud.sh
   ```

2. **Recreate from Cloud Secrets**:
   ```bash
   # Export secrets from cloud
   # Import to local storage
   ```

### **If Cloud Secrets are Corrupted**

1. **Sync from Local**:
   ```bash
   ./scripts/sync-secrets-to-cloud.sh
   ```

2. **Verify**:
   ```bash
   ./scripts/verify-secrets-sync.sh
   ```

---

## 🔄 Automated Sync (Future Enhancement)

### **Option 1: Pre-commit Hook**
- Sync to cloud before committing changes
- Ensures cloud is always up to date

### **Option 2: CI/CD Pipeline**
- Sync secrets as part of deployment pipeline
- Automated verification

### **Option 3: Scheduled Sync**
- Daily/weekly sync check
- Alert if out of sync

---

## 📋 Summary

### **Update Order**
1. **Local First** (source of truth)
2. **Then Cloud** (production)

### **Sync Workflow**
1. Update `config/env/.env.local`
2. Import to local encrypted storage
3. Sync to Google Cloud Secrets Manager
4. Verify sync
5. Update Cloud Run if needed

### **Key Principle**
**Local encrypted storage is the source of truth. Cloud is a sync target.**

---

## 🔗 Related Documentation

- `docs/security/SECRETS_MANAGEMENT_RECOMMENDATION.md` - Overall strategy
- `docs/security/SECRETS_MANAGEMENT.md` - Current state
- `config/secure-api-manager.py` - Local secret management

---

**Last Updated**: November 16, 2025

