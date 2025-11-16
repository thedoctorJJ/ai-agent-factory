# Secrets Management - Quick Reference

**Last Updated**: November 16, 2025

---

## 🎯 Key Principle

**Local encrypted storage (`config/api-secrets.enc`) is the source of truth.**

**Always update local first, then sync to cloud.**

---

## 📋 Common Workflows

### **Update a Secret**

```bash
# 1. Edit local file
vim config/env/.env.local

# 2. Import to encrypted storage
python3 config/secure-api-manager.py import config/env/.env.local

# 3. Sync to cloud
./scripts/sync-secrets-to-cloud.sh

# 4. Verify
./scripts/verify-secrets-sync.sh
```

### **Add a New Secret**

```bash
# 1. Add to local file
echo "NEW_SECRET=value" >> config/env/.env.local

# 2. Import to encrypted storage
python3 config/secure-api-manager.py import config/env/.env.local

# 3. Sync to cloud
./scripts/sync-secrets-to-cloud.sh

# 4. Grant access (if needed for Cloud Run)
./scripts/grant-secret-access.sh

# 5. Update Cloud Run (if needed)
./scripts/deploy-with-secrets.sh
```

### **Verify Secrets are in Sync**

```bash
./scripts/verify-secrets-sync.sh
```

### **Emergency: Restore from Cloud**

```bash
# Only if local storage is lost!
./scripts/pull-secrets-from-cloud.sh
```

---

## 🔄 Update Order

### **Always: Local → Cloud**

1. ✅ Update local encrypted storage (source of truth)
2. ✅ Sync to Google Cloud Secrets Manager
3. ✅ Verify sync
4. ✅ Update Cloud Run if needed

### **Never: Cloud → Local** (except emergency)

- ❌ Don't update cloud first
- ❌ Don't use cloud as source of truth
- ✅ Only pull from cloud if local is lost

---

## 📊 Sync Status

### **Check Sync Status**
```bash
./scripts/verify-secrets-sync.sh
```

**Output**:
- ✅ In sync: Secrets match
- ⚠️ Different: Values don't match
- ❌ Not in cloud: Secret missing in cloud
- ⚠️ In cloud but not local: Extra secret in cloud

---

## 🔧 Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `sync-secrets-to-cloud.sh` | Sync local → cloud | After updating local secrets |
| `verify-secrets-sync.sh` | Check sync status | Before deployments, weekly checks |
| `pull-secrets-from-cloud.sh` | Pull cloud → local | Emergency only (local lost) |
| `setup-cloud-secrets.sh` | Initial setup | First time setup |
| `grant-secret-access.sh` | Grant access | After creating new secrets |
| `deploy-with-secrets.sh` | Deploy to Cloud Run | After syncing secrets |

---

## 🚨 Important Rules

1. **Local is source of truth** - Always update local first
2. **Sync after changes** - Always sync to cloud after updating local
3. **Verify before deploy** - Check sync status before deployments
4. **Document changes** - Update CHANGELOG when secrets change
5. **Never commit secrets** - Secrets are encrypted and gitignored

---

## 📝 Example: Rotating an API Key

```bash
# 1. Get new API key
NEW_KEY="sk-new-key-here"

# 2. Update local file
sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$NEW_KEY/" config/env/.env.local

# 3. Import to encrypted storage
python3 config/secure-api-manager.py import config/env/.env.local

# 4. Sync to cloud
./scripts/sync-secrets-to-cloud.sh

# 5. Verify
./scripts/verify-secrets-sync.sh

# 6. Test (Cloud Run uses latest version automatically)
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health
```

---

## 🔗 Full Documentation

- **Sync Strategy**: `docs/security/SECRETS_SYNC_STRATEGY.md`
- **Recommendation**: `docs/security/SECRETS_MANAGEMENT_RECOMMENDATION.md`
- **Current State**: `docs/security/SECRETS_MANAGEMENT.md`

---

**Remember**: Local first, then cloud! 🔄

