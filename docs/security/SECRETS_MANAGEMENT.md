# Secrets Management in AI Agent Factory

**Last Updated**: November 16, 2025

---

## 📋 Current State

The AI Agent Factory uses **different secret management approaches** for local development and production, which can be confusing. This document clarifies the current state and recommended approach.

**Note**: The README.md states "All production environment variables configured" and mentions using the "secure configuration system" for production, but this is **not accurate**. The README describes the local development secure configuration system, but production actually uses a different approach (or in some cases, no approach at all).

---

## 🔐 Secret Management Approaches

### 1. **Local Development** - Encrypted File Storage

**Location**: `config/api-secrets.enc`  
**Tool**: `config/secure-api-manager.py`  
**Method**: AES encryption with master key

**How it works**:
- Secrets stored in encrypted file: `config/api-secrets.enc`
- Master key: `config/.master-key` (never committed to git)
- Tool: `python3 config/secure-api-manager.py`
- Creates working `.env` file for local development

**Usage**:
```bash
# Import secrets from file
python3 config/secure-api-manager.py import config/env/.env.local

# Create working .env file
python3 config/secure-api-manager.py create

# List stored secrets (masked)
python3 config/secure-api-manager.py list
```

**Security**:
- ✅ Encrypted at rest
- ✅ Restrictive file permissions (600)
- ✅ Never committed to git
- ❌ Only for local development
- ❌ Not used in production

---

### 2. **Production (Current)** - Plain Environment Variables

**Location**: Google Cloud Run service configuration  
**Method**: Direct environment variables via `gcloud run services update`  
**Script**: `scripts/update-production-env.sh`

**How it works**:
- Script reads from local `secure-api-manager` (encrypted file)
- Decrypts secrets locally
- Sets environment variables directly on Cloud Run service via `gcloud run services update --set-env-vars`
- Variables stored as plain text in Cloud Run service configuration

**Current State**:
- ⚠️ **Only `ENVIRONMENT=production` is currently set** (verified via `gcloud run services describe`)
- ⚠️ Other secrets are **NOT currently configured** in production
- ⚠️ The `scripts/update-production-env.sh` script exists but **hasn't been run**
- ⚠️ This is why health checks show "missing" (but endpoints work because...?)

**What README Says vs. Reality**:
- **README Claims**: "All production environment variables configured" (line 31, 83, 182)
- **README Claims**: "Updated Cloud Run service with all required environment variables using secure config" (line 325)
- **Reality**: Only `ENVIRONMENT=production` is set, script hasn't been executed

**Usage**:
```bash
./scripts/update-production-env.sh
```

**Security**:
- ✅ Stored in Google Cloud (not in code)
- ⚠️ Plain text in Cloud Run service config
- ⚠️ Visible in Cloud Console
- ⚠️ Not using Google Secrets Manager

---

### 3. **Production (Intended)** - Google Cloud Secrets Manager

**Location**: `infra/google-cloud.yaml`  
**Method**: Cloud Secrets Manager via `secretKeyRef`  
**Status**: ⚠️ **NOT CURRENTLY IMPLEMENTED**

**How it should work**:
```yaml
env:
- name: SUPABASE_URL
  valueFrom:
    secretKeyRef:
      name: supabase-secrets
      key: url
```

**Required Steps** (not yet done):
1. Create secrets in Google Cloud Secrets Manager
2. Grant Cloud Run service account access to secrets
3. Deploy using YAML configuration with `secretKeyRef`

**Security**:
- ✅ Encrypted at rest
- ✅ Access controlled via IAM
- ✅ Audit logging
- ✅ Versioning support
- ✅ Best practice for production

---

## 🔍 Current Production Status

### What's Actually Deployed

```bash
# Check current environment variables
gcloud run services describe ai-agent-factory-backend \
  --region=us-central1 \
  --format="yaml(spec.template.spec.containers[0].env)"
```

**Result**: Only `ENVIRONMENT=production` is set

**Verified**: November 16, 2025 - Confirmed via `gcloud` command

### Why Endpoints Still Work

This is the confusing part! The endpoints work because:
1. **Supabase**: May be using default connection or service account
2. **OpenAI**: Not actually being used (or using fallback)
3. **GitHub**: Not actually being used (or using service account)
4. **Google Cloud**: Using default project credentials

**OR** the secrets might be set via:
- Service account default credentials
- Cloud Run metadata service
- Some other mechanism we haven't identified

---

## 🎯 Recommended Approach

### For Production: Use Google Cloud Secrets Manager

**Why**:
- ✅ Industry best practice
- ✅ Encrypted and access-controlled
- ✅ Audit logging
- ✅ Versioning
- ✅ No secrets in service configuration

**Steps to Implement**:

1. **Create Secrets in Secrets Manager**:
```bash
# Create secrets
echo -n "your-supabase-url" | gcloud secrets create supabase-url --data-file=-
echo -n "your-supabase-key" | gcloud secrets create supabase-key --data-file=-
echo -n "your-openai-key" | gcloud secrets create openai-api-key --data-file=-
echo -n "your-github-token" | gcloud secrets create github-token --data-file=-
```

2. **Grant Access to Cloud Run Service Account**:
```bash
# Get service account
SERVICE_ACCOUNT=$(gcloud run services describe ai-agent-factory-backend \
  --region=us-central1 \
  --format="value(spec.template.spec.serviceAccountName)")

# Grant access
gcloud secrets add-iam-policy-binding supabase-url \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

3. **Update Cloud Run Service**:
```bash
gcloud run services update ai-agent-factory-backend \
  --region=us-central1 \
  --update-secrets=SUPABASE_URL=supabase-url:latest,SUPABASE_KEY=supabase-key:latest
```

4. **Or Use YAML with secretKeyRef** (requires Cloud Run for Anthos or GKE)

---

## 📝 Migration Plan

### Phase 1: Document Current State ✅
- [x] Document current secret management approaches
- [x] Identify what's actually deployed

### Phase 2: Implement Secrets Manager
- [ ] Create secrets in Google Cloud Secrets Manager
- [ ] Grant service account access
- [ ] Update deployment scripts
- [ ] Test in staging

### Phase 3: Migrate Production
- [ ] Migrate existing secrets to Secrets Manager
- [ ] Update Cloud Run service configuration
- [ ] Verify all services work
- [ ] Remove plain env vars

### Phase 4: Update Documentation
- [ ] Update deployment guides
- [ ] Update startup prompt
- [ ] Update troubleshooting docs

---

## 🔧 Tools and Scripts

### Local Development
- `config/secure-api-manager.py` - Encrypted local secret storage
- `scripts/config/env-manager.sh` - Environment file management

### Production Deployment
- `scripts/update-production-env.sh` - Sets plain env vars (current)
- `infra/google-cloud.yaml` - YAML with secretKeyRef (intended, not used)

### Recommended New Scripts
- `scripts/setup-cloud-secrets.sh` - Create secrets in Secrets Manager
- `scripts/deploy-with-secrets.sh` - Deploy using Secrets Manager

---

## ⚠️ Important Notes

1. **Current Production**: Secrets are NOT properly configured (despite README claims)
2. **Health Checks**: Show "missing" because env vars aren't set (but services may work via other means)
3. **Security**: Plain env vars in Cloud Run are less secure than Secrets Manager
4. **Best Practice**: Should migrate to Secrets Manager for production
5. **Documentation Gap**: README.md claims production is configured, but it's not accurate
6. **Script Available**: `scripts/update-production-env.sh` exists to set env vars but hasn't been run

---

## 🔗 Related Documentation

- `docs/security/SECURITY.md` - General security practices
- `docs/deployment/06-deployment-guide.md` - Deployment guide
- `config/secure-api-manager.py` - Local secret management tool
- `scripts/update-production-env.sh` - Current production deployment script

---

## ✅ Next Steps

1. **Investigate**: Why endpoints work if secrets aren't set
2. **Implement**: Google Cloud Secrets Manager for production
3. **Migrate**: Move from plain env vars to Secrets Manager
4. **Document**: Update all deployment documentation

---

**Status**: 🔴 **NEEDS ATTENTION** - Production secrets not properly configured

