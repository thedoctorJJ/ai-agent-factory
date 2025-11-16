# Secrets Management Setup - Explained

**Date**: November 16, 2025  
**Status**: ✅ **FULLY OPERATIONAL**

---

## 🎯 Overview

The AI Agent Factory uses a **two-tier secrets management system** that separates local development from production, with local encrypted storage as the source of truth.

---

## 🏗️ Architecture

### **Two-Tier System**

```
┌─────────────────────────────────────────────────────────┐
│  LOCAL DEVELOPMENT (Source of Truth)                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │ config/env/.env.local                              │  │
│  │   ↓                                                │  │
│  │ config/secure-api-manager.py                       │  │
│  │   ↓                                                │  │
│  │ config/api-secrets.enc (AES Encrypted)            │  │
│  │   ↓                                                │  │
│  │ .env (for local app use)                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        │ SYNC (one-way: local → cloud)
                        ↓
┌─────────────────────────────────────────────────────────┐
│  PRODUCTION (Google Cloud)                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Google Cloud Secrets Manager                       │  │
│  │   - Encrypted at rest                             │  │
│  │   - IAM access control                             │  │
│  │   - Version history                               │  │
│  │   ↓                                                │  │
│  │ Cloud Run Service                                  │  │
│  │   - Secrets injected as env vars                   │  │
│  │   - Auto-updates with :latest                      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Components Explained

### **1. Local Development Layer**

#### **config/env/.env.local**
- **Purpose**: Human-readable source file
- **Contains**: All API keys and secrets in plain text
- **Security**: Gitignored, never committed
- **Usage**: Edit this file when you need to update secrets

#### **config/secure-api-manager.py**
- **Purpose**: Encryption/decryption tool
- **Function**: 
  - Encrypts secrets from `.env.local` → `api-secrets.enc`
  - Decrypts secrets from `api-secrets.enc` → `.env`
  - Manages master encryption key
- **Commands**:
  - `import` - Encrypt and store secrets
  - `create` - Generate `.env` file for app
  - `list` - Show stored secrets (masked)
  - `validate` - Check configuration

#### **config/api-secrets.enc**
- **Purpose**: Encrypted storage (source of truth)
- **Format**: AES-encrypted binary file
- **Security**: 
  - Encrypted with master key
  - File permissions: 600 (owner read/write only)
  - Never committed to git
- **Contains**: All secrets in encrypted form

#### **.env** (project root)
- **Purpose**: Working file for local application
- **Generated**: Automatically by `secure-api-manager.py`
- **Usage**: Application reads from this file
- **Security**: Gitignored, regenerated as needed

---

### **2. Production Layer**

#### **Google Cloud Secrets Manager**
- **Purpose**: Secure cloud storage for production secrets
- **Location**: Google Cloud Platform
- **Security Features**:
  - Encrypted at rest by Google
  - IAM-based access control
  - Audit logging
  - Version history
- **Secrets Stored**: 20 secrets (all from local storage)

#### **Cloud Run Service**
- **Purpose**: Application runtime
- **Secret Integration**: 
  - Secrets referenced via `--update-secrets` flag
  - Injected as environment variables at runtime
  - Uses `:latest` version (auto-updates)
- **Service Account**: Has `secretAccessor` role for all secrets

---

## 🔄 Workflow: How It Works

### **Initial Setup** (One-time)

```bash
# 1. Create secrets in Google Cloud Secrets Manager
./scripts/setup-cloud-secrets.sh
#   - Reads from local encrypted storage
#   - Creates secrets in Secrets Manager
#   - Result: 20 secrets created

# 2. Grant Cloud Run service account access
./scripts/grant-secret-access.sh
#   - Gets service account from Cloud Run
#   - Grants secretAccessor role
#   - Result: Service can read secrets

# 3. Deploy Cloud Run with secrets
./scripts/deploy-with-secrets.sh
#   - Updates service with secret references
#   - Deploys new revision
#   - Result: App running with secrets
```

### **Daily Workflow: Updating a Secret**

```bash
# Step 1: Update local (source of truth)
vim config/env/.env.local
# Edit the secret value

# Step 2: Encrypt and store locally
python3 config/secure-api-manager.py import config/env/.env.local
# Result: api-secrets.enc updated

# Step 3: Sync to cloud
./scripts/sync-secrets-to-cloud.sh
# Result: Secret updated in Secrets Manager

# Step 4: Verify sync
./scripts/verify-secrets-sync.sh
# Result: Confirms local and cloud match

# Step 5: Cloud Run auto-updates (uses :latest)
# No deployment needed - Cloud Run uses latest version automatically
```

---

## 🔐 Security Model

### **Local Development**
- **Encryption**: AES encryption with master key
- **Storage**: Encrypted file (`api-secrets.enc`)
- **Access**: File permissions (600) - owner only
- **Git**: Never committed (gitignored)

### **Production**
- **Encryption**: Google-managed encryption at rest
- **Storage**: Google Cloud Secrets Manager
- **Access**: IAM roles (service account has `secretAccessor`)
- **Audit**: All access logged
- **Versioning**: Full version history

### **Sync Process**
- **Direction**: One-way (local → cloud)
- **Method**: Scripts read from encrypted storage, write to cloud
- **Verification**: Script compares local vs cloud values
- **Security**: No secrets in transit (gcloud handles encryption)

---

## 📊 Current State

### **What's Deployed**

**Local**:
- ✅ 20 secrets in encrypted storage
- ✅ Master key configured
- ✅ `.env` file generated for local use

**Cloud**:
- ✅ 20 secrets in Google Cloud Secrets Manager
- ✅ Service account has access to all secrets
- ✅ Cloud Run service using secrets
- ✅ Health check: "healthy"
- ✅ All services: "configured"

**Sync Status**:
- ✅ All 20 secrets in sync
- ✅ Local and cloud match exactly

---

## 🎯 Key Principles

### **1. Source of Truth**
- **Local encrypted storage** (`config/api-secrets.enc`) is the source of truth
- Cloud is a **sync target**, not the source
- Always update local first, then sync to cloud

### **2. Update Order**
- ✅ **Correct**: Local → Cloud
- ❌ **Wrong**: Cloud → Local (except emergency recovery)

### **3. Security**
- Secrets never in git
- Encrypted at rest (local and cloud)
- Access controlled (file permissions + IAM)
- Audit logging (cloud)

### **4. Automation**
- Scripts handle sync automatically
- Cloud Run uses `:latest` (auto-updates)
- Verification scripts ensure consistency

---

## 🔧 Available Tools

### **Local Management**
- `config/secure-api-manager.py` - Encrypt/decrypt secrets
- `scripts/config/env-manager.sh` - Environment file management

### **Cloud Setup** (one-time)
- `scripts/setup-cloud-secrets.sh` - Create secrets in cloud
- `scripts/grant-secret-access.sh` - Grant service account access
- `scripts/deploy-with-secrets.sh` - Deploy with secrets

### **Sync & Verification**
- `scripts/sync-secrets-to-cloud.sh` - Sync local → cloud
- `scripts/verify-secrets-sync.sh` - Verify sync status
- `scripts/pull-secrets-from-cloud.sh` - Emergency recovery

---

## 📝 Example: Rotating an API Key

**Scenario**: OpenAI API key expired, need to rotate

```bash
# 1. Get new API key from OpenAI
NEW_KEY="sk-new-key-here"

# 2. Update local file (source of truth)
sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$NEW_KEY/" config/env/.env.local

# 3. Encrypt and store locally
python3 config/secure-api-manager.py import config/env/.env.local
# Output: ✅ API keys encrypted and stored securely

# 4. Sync to cloud
./scripts/sync-secrets-to-cloud.sh
# Output: 🔄 OPENAI_API_KEY: Updating (value changed)
#         ✅ Updated

# 5. Verify sync
./scripts/verify-secrets-sync.sh
# Output: ✅ OPENAI_API_KEY: In sync

# 6. Cloud Run automatically uses new key (uses :latest)
# No deployment needed!

# 7. Test
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health
# Should show: "openai": "configured"
```

**Time**: ~2 minutes  
**Steps**: 5 commands  
**Result**: Key rotated in local and production

---

## 🚨 Important Notes

### **Do's**
- ✅ Always update local first
- ✅ Sync to cloud after local updates
- ✅ Verify sync before deployments
- ✅ Use scripts for all operations
- ✅ Keep master key safe (backup)

### **Don'ts**
- ❌ Never update cloud first
- ❌ Never commit secrets to git
- ❌ Never share master key
- ❌ Never edit `api-secrets.enc` directly
- ❌ Never skip sync verification

---

## 🔗 Related Documentation

- **Quick Reference**: `docs/security/SECRETS_QUICK_REFERENCE.md`
- **Sync Strategy**: `docs/security/SECRETS_SYNC_STRATEGY.md`
- **Recommendation**: `docs/security/SECRETS_MANAGEMENT_RECOMMENDATION.md`
- **Current State**: `docs/security/SECRETS_MANAGEMENT.md`

---

## ✅ Summary

**What We Have**:
- Local encrypted storage (source of truth)
- Google Cloud Secrets Manager (production)
- Automated sync scripts
- Verification tools
- Complete documentation

**How It Works**:
1. Edit secrets in `config/env/.env.local`
2. Encrypt with `secure-api-manager.py`
3. Sync to cloud with `sync-secrets-to-cloud.sh`
4. Cloud Run automatically uses latest versions

**Result**:
- ✅ Secure (encrypted at rest)
- ✅ Automated (scripts handle sync)
- ✅ Verified (sync status checked)
- ✅ Production-ready (fully operational)

---

**Last Updated**: November 16, 2025  
**Status**: ✅ **FULLY OPERATIONAL**

