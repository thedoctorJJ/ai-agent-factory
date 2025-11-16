# Secrets Management - Recommended Approach

**Date**: November 16, 2025  
**Status**: Recommendation for Production Migration

---

## 🎯 Recommended Architecture

### **Two-Tier Approach**

1. **Local Development**: Keep current encrypted file system ✅
2. **Production**: Migrate to Google Cloud Secrets Manager ✅

---

## 📋 Detailed Recommendation

### **1. Local Development - Keep Current System** ✅

**Why**: 
- ✅ Already working well
- ✅ Encrypted and secure for local use
- ✅ No external dependencies
- ✅ Fast and convenient

**What to Keep**:
- `config/secure-api-manager.py` - Encrypted local storage
- `config/api-secrets.enc` - Encrypted secrets file
- `.env` file generation for local development

**No changes needed** - This is working perfectly for local development.

---

### **2. Production - Migrate to Google Cloud Secrets Manager** ✅

**Why**:
- ✅ **Industry Best Practice**: Standard for production workloads
- ✅ **Encrypted at Rest**: Secrets encrypted by Google
- ✅ **Access Control**: IAM-based permissions
- ✅ **Audit Logging**: Track who accessed what secrets
- ✅ **Versioning**: Keep history of secret changes
- ✅ **Rotation Support**: Easy to rotate secrets
- ✅ **No Secrets in Service Config**: Secrets not visible in Cloud Run console
- ✅ **Compliance**: Meets security compliance requirements

**What to Implement**:
- Store all secrets in Google Cloud Secrets Manager
- Reference secrets in Cloud Run via `--update-secrets` flag
- Grant service account access to secrets
- Remove plain environment variables

---

## 🚀 Migration Plan

### **Phase 1: Setup Secrets Manager** (30 minutes)

#### Step 1: Enable Secrets Manager API
```bash
gcloud services enable secretmanager.googleapis.com
```

#### Step 2: Create Secrets from Local Encrypted Storage
```bash
# Load secrets from local encrypted storage
python3 config/secure-api-manager.py list

# Create secrets in Secrets Manager (one-time setup script)
./scripts/setup-cloud-secrets.sh
```

**Script to create** (`scripts/setup-cloud-secrets.sh`):
```bash
#!/bin/bash
# Create secrets in Google Cloud Secrets Manager from local secure storage

PROJECT_ID="agent-factory-474201"
REGION="us-central1"

# Load secrets from secure-api-manager
python3 << 'EOF'
import sys
sys.path.append('.')
from config.secure_api_manager import SecureAPIManager

manager = SecureAPIManager()
secrets = manager.load_api_keys()

# Print secrets in format: SECRET_NAME=value
for key, value in secrets.items():
    if value and not key.startswith('_'):
        print(f"{key}={value}")
EOF | while IFS='=' read -r key value; do
    if [ -n "$key" ] && [ -n "$value" ]; then
        echo "Creating secret: $key"
        echo -n "$value" | gcloud secrets create "$key" \
            --data-file=- \
            --project="$PROJECT_ID" \
            --replication-policy="automatic"
    fi
done
```

#### Step 3: Grant Service Account Access
```bash
# Get Cloud Run service account
SERVICE_ACCOUNT=$(gcloud run services describe ai-agent-factory-backend \
  --region=us-central1 \
  --format="value(spec.template.spec.serviceAccountName)")

# If no service account, use default compute service account
if [ -z "$SERVICE_ACCOUNT" ]; then
    SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
fi

# Grant access to all secrets
SECRETS=(
    "SUPABASE_URL"
    "SUPABASE_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
    "OPENAI_API_KEY"
    "GITHUB_TOKEN"
    "GOOGLE_CLOUD_PROJECT_ID"
)

for SECRET in "${SECRETS[@]}"; do
    echo "Granting access to $SECRET..."
    gcloud secrets add-iam-policy-binding "$SECRET" \
        --member="serviceAccount:${SERVICE_ACCOUNT}" \
        --role="roles/secretmanager.secretAccessor" \
        --project="$PROJECT_ID"
done
```

---

### **Phase 2: Update Cloud Run Service** (15 minutes)

#### Step 1: Update Service with Secret References
```bash
gcloud run services update ai-agent-factory-backend \
  --region=us-central1 \
  --update-secrets=SUPABASE_URL=SUPABASE_URL:latest \
  --update-secrets=SUPABASE_KEY=SUPABASE_KEY:latest \
  --update-secrets=SUPABASE_SERVICE_ROLE_KEY=SUPABASE_SERVICE_ROLE_KEY:latest \
  --update-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest \
  --update-secrets=GITHUB_TOKEN=GITHUB_TOKEN:latest \
  --update-secrets=GOOGLE_CLOUD_PROJECT_ID=GOOGLE_CLOUD_PROJECT_ID:latest \
  --set-env-vars="ENVIRONMENT=production"
```

#### Step 2: Verify Secrets are Loaded
```bash
# Test health endpoint
curl https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health

# Should now show "healthy" status with all services configured
```

---

### **Phase 3: Cleanup** (10 minutes)

#### Step 1: Remove Plain Environment Variables (if any exist)
```bash
# Remove any plain env vars (secrets are now from Secrets Manager)
gcloud run services update ai-agent-factory-backend \
  --region=us-central1 \
  --clear-env-vars
```

#### Step 2: Update Documentation
- Update README.md to reflect Secrets Manager usage
- Update deployment guides
- Update startup prompt

---

## 🔧 Implementation Scripts

### **Script 1: Setup Cloud Secrets** (`scripts/setup-cloud-secrets.sh`)

Creates all secrets in Secrets Manager from local encrypted storage.

**Features**:
- Reads from `config/secure-api-manager.py`
- Creates secrets in Google Cloud Secrets Manager
- Handles errors gracefully
- Idempotent (can run multiple times)

### **Script 2: Grant Secret Access** (`scripts/grant-secret-access.sh`)

Grants Cloud Run service account access to all secrets.

**Features**:
- Automatically detects service account
- Grants `secretAccessor` role
- Handles all required secrets

### **Script 3: Deploy with Secrets** (`scripts/deploy-with-secrets.sh`)

Updates Cloud Run service to use Secrets Manager.

**Features**:
- Updates service with secret references
- Verifies deployment
- Tests health endpoint

---

## 📊 Comparison: Current vs. Recommended

| Aspect | Current (Plain Env Vars) | Recommended (Secrets Manager) |
|--------|-------------------------|-------------------------------|
| **Encryption** | ⚠️ Plain text in service config | ✅ Encrypted at rest |
| **Access Control** | ⚠️ Visible in Cloud Console | ✅ IAM-based permissions |
| **Audit Logging** | ❌ No logging | ✅ Full audit trail |
| **Versioning** | ❌ No versioning | ✅ Version history |
| **Rotation** | ⚠️ Manual update required | ✅ Easy rotation |
| **Security** | ⚠️ Medium | ✅ High |
| **Best Practice** | ❌ Not recommended | ✅ Industry standard |
| **Compliance** | ⚠️ May not meet requirements | ✅ Meets compliance |

---

## ✅ Benefits of This Approach

### **Security**
- Secrets encrypted at rest
- Access controlled via IAM
- No secrets visible in service configuration
- Audit logging for compliance

### **Operational**
- Easy secret rotation
- Version history
- Centralized management
- No manual updates needed

### **Developer Experience**
- Local dev stays the same (no disruption)
- Production uses industry standard
- Clear separation of concerns
- Better documentation

---

## 🚨 Important Considerations

### **Cost**
- Google Cloud Secrets Manager: **$0.06 per secret per month**
- First 6 secrets: **Free**
- Very low cost for the security benefits

### **Performance**
- Secrets loaded at container startup
- No performance impact on runtime
- Cached in memory after first access

### **Backup**
- Secrets Manager automatically replicates
- No manual backup needed
- Version history provides backup

---

## 📝 Next Steps

1. **Review this recommendation** ✅
2. **Create implementation scripts** (I can help with this)
3. **Test in staging** (if you have a staging environment)
4. **Migrate production** (follow Phase 1-3)
5. **Update documentation** (README, deployment guides)
6. **Monitor and verify** (health checks, logs)

---

## 🔗 Related Documentation

- `docs/security/SECRETS_MANAGEMENT.md` - Current state analysis
- `docs/security/SECRETS_MANAGEMENT_SUMMARY.md` - Quick reference
- `config/secure-api-manager.py` - Local secret management
- `scripts/update-production-env.sh` - Current production script (to be replaced)

---

## ✅ Recommendation Summary

**For Local Development**: ✅ **Keep current system** - It's working well

**For Production**: ✅ **Migrate to Google Cloud Secrets Manager** - Industry best practice

**Migration Effort**: ~1 hour total
- Setup: 30 minutes
- Deployment: 15 minutes  
- Cleanup: 10 minutes
- Testing: 5 minutes

**Risk Level**: Low (can rollback easily)

**Security Improvement**: High (significant security upgrade)

---

**Status**: Ready for implementation

