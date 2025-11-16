# Cursor Startup Script - AI Agent Factory

## 🎯 Objective

You are starting a new session on the **AI Agent Factory** project. Your first task is to thoroughly understand the application, its current state, configuration, and any documented issues. Follow these steps systematically:

---

## 🔐 CRITICAL: Secrets Management Briefing

**⚠️ READ THIS FIRST - Before making any changes to secrets or configuration**

### **Secrets Management Strategy**

The AI Agent Factory uses a **two-tier secrets management approach**:

1. **Local Development**: Encrypted file storage (`config/api-secrets.enc`)
2. **Production**: Google Cloud Secrets Manager

### **⚠️ IMPORTANT RULES**

1. **Source of Truth**: Local encrypted storage (`config/api-secrets.enc`) is the **source of truth**
2. **Update Order**: **ALWAYS update local first, then sync to cloud**
   - ✅ Local → Cloud (correct)
   - ❌ Cloud → Local (wrong, except emergency recovery)
3. **Never Update Cloud First**: Cloud is a sync target, not the source
4. **Sync After Changes**: Always sync to cloud after updating local secrets

### **Secrets Management Workflow**

**When updating secrets:**
```bash
# 1. Update local (source of truth)
vim config/env/.env.local
python3 config/secure-api-manager.py import config/env/.env.local

# 2. Sync to cloud
./scripts/sync-secrets-to-cloud.sh

# 3. Verify sync
./scripts/verify-secrets-sync.sh
```

**When checking secrets:**
```bash
# Verify local and cloud are in sync
./scripts/verify-secrets-sync.sh
```

### **Key Documentation**

- **Quick Reference**: `docs/security/SECRETS_QUICK_REFERENCE.md`
- **Sync Strategy**: `docs/security/SECRETS_SYNC_STRATEGY.md`
- **Full Details**: `docs/security/SECRETS_MANAGEMENT_RECOMMENDATION.md`

### **⚠️ Before Making Any Secret Changes**

1. **Read the secrets documentation first**
2. **Understand the update order** (local → cloud)
3. **Verify current sync status** before making changes
4. **Never commit secrets** (they're encrypted and gitignored)

**Remember**: Local is source of truth. Always update local first, then sync to cloud.

---

## 📋 CRITICAL: PRD Management Briefing

**⚠️ READ THIS - Before making any changes to PRDs**

### **PRD Management Strategy**

The AI Agent Factory uses a **file-based PRD system**:

1. **Source of Truth**: PRD files in `prds/queue/`
2. **Database**: Supabase (sync target only)

### **⚠️ IMPORTANT RULES**

1. **Source of Truth**: PRD files in `prds/queue/` are the **source of truth**
2. **Update Order**: **ALWAYS update files first, then sync to database**
   - ✅ Files → Database (correct)
   - ❌ Database → Files (wrong, except emergency recovery)
3. **Never Update Database First**: Database is a sync target, not the source
4. **Sync After Changes**: Always sync to database after updating PRD files

### **PRD Management Workflow**

**When updating PRDs:**
```bash
# 1. Update PRD file (source of truth)
vim prds/queue/2024-11-16_my-prd.md

# 2. Sync to database
./scripts/prd-management/sync-prds-to-database.sh

# 3. Verify sync
./scripts/prd-management/verify-prds-sync.sh
```

**When checking PRDs:**
```bash
# Verify files and database are in sync
./scripts/prd-management/verify-prds-sync.sh
```

### **Key Documentation**

- **Quick Reference**: `docs/guides/PRD_QUICK_REFERENCE.md`
- **Sync Strategy**: `docs/guides/PRD_SYNC_STRATEGY.md`
- **File System**: `docs/troubleshooting/file-based-prd-system.md`

### **⚠️ Before Making Any PRD Changes**

1. **Read the PRD documentation first**
2. **Understand the update order** (files → database)
3. **Verify current sync status** before making changes
4. **Always commit PRD file changes** to git

**Remember**: Files are source of truth. Always update files first, then sync to database.

---

## 📋 Step 1: Understand What This Application Does

### 1.1 Read the README
- **File**: `README.md` (project root)
- **Action**: Read the entire README file carefully
- **Focus on**:
  - Project purpose and description
  - Live production URLs and status
  - Architecture overview
  - Technology stack
  - Key features and capabilities
  - Recent updates and fixes

### 1.2 Scan Key Documentation Files
Read these files to understand the application structure:
- `docs/architecture/01-architecture-overview.md` - System architecture
- `docs/getting-started/quick-start.md` - Quick start guide
- `docs/guides/04-prd-system.md` - PRD system documentation
- `docs/guides/05-agent-management.md` - Agent management system
- `CHANGELOG.md` - Recent changes and updates

### 1.3 Examine Project Structure
Scan the entire file structure to identify key components:

**Backend**:
- `backend/fastapi_app/main.py` - Main FastAPI application
- `backend/fastapi_app/routers/` - API route handlers
- `backend/fastapi_app/services/` - Business logic services
- `backend/fastapi_app/models/` - Data models
- `backend/fastapi_app/utils/` - Utility functions

**Frontend**:
- `frontend/next-app/` - Next.js frontend application
- `frontend/next-app/types/` - TypeScript type definitions

**Infrastructure**:
- `infra/` - Infrastructure configuration
- `scripts/` - Automation scripts
- `api-spec/` - OpenAPI specifications

**Documentation**:
- `docs/` - Complete documentation suite
- `docs/resolution-summaries/` - Previous issue resolutions

---

## 📚 Step 2: Review Previous Issue Resolutions

### 2.1 Read Resolution Summaries
- **Directory**: `docs/resolution-summaries/`
- **Action**: Read all resolution summary documents
- **Files to read**:
  - `agent-display-issue-resolution.md` - Agent endpoint fix (November 13, 2025)
  - `secrets-management-implementation-resolution.md` - Secrets management system implementation (November 16, 2025)

### 2.2 Review Troubleshooting Documentation
- **Directory**: `docs/troubleshooting/`
- **Action**: Review all troubleshooting guides
- **Focus on**:
  - Known issues and their solutions
  - Common problems and fixes
  - Error patterns and resolutions

### 2.3 Check CHANGELOG
- **File**: `CHANGELOG.md`
- **Action**: Review recent entries to understand:
  - Recent fixes and improvements
  - Known issues
  - Deployment history
  - Breaking changes

---

## 🔐 Step 3: Check Environment Configuration

### 3.0 Ensure Docker is Running
**⚠️ IMPORTANT**: Docker must be running for deployment and local development.

**Check Docker Status**:
```bash
docker ps
```

**If Docker is not running**:
- **macOS**: Run `open -a Docker` or `open -a "Docker Desktop"`
- **Linux**: Start Docker service: `sudo systemctl start docker`
- **Windows**: Open Docker Desktop application

**Wait for Docker to be ready**:
- Docker Desktop may take 10-30 seconds to fully start
- Verify with: `docker ps` (should return container list or empty list, not an error)
- Never proceed with deployment if Docker is not running

### 3.1 Locate Environment Files
Search for environment configuration files:
- `.env` - Local development environment
- `.env.local` - Local overrides
- `.env.production` - Production configuration
- `config/` - Configuration directory
- `backend/.env` - Backend-specific environment
- `frontend/next-app/.env*` - Frontend environment files

### 3.2 Check for API Keys and Secrets
**IMPORTANT**: When checking environment files, identify but **DO NOT DISPLAY** sensitive values:

1. **Check for presence** of these keys (but don't show values):
   - `SUPABASE_URL` and `SUPABASE_KEY`
   - `OPENAI_API_KEY`
   - `GITHUB_TOKEN`
   - `GOOGLE_CLOUD_PROJECT_ID`
   - Any other API keys or secrets

2. **Report status**:
   - Which keys are configured
   - Which keys are missing
   - Environment (development/production)
   - Configuration method (local encrypted storage, Cloud Secrets Manager, etc.)

3. **Security Note**: 
   - Never display actual API key values
   - Report only presence/absence and configuration status
   - Note if using secure configuration system

4. **Secrets Management Note**:
   - **Local Development**: Uses encrypted file storage (`config/api-secrets.enc`)
   - **Production**: Uses Google Cloud Secrets Manager
   - **Source of Truth**: Local encrypted storage is the source of truth
   - **Sync Status**: Check if local and cloud are in sync using `./scripts/verify-secrets-sync.sh`
   - **Update Order**: Always update local first, then sync to cloud
   - See `docs/security/SECRETS_QUICK_REFERENCE.md` for workflow details

5. **Production Configuration Note**:
   - In production, secrets are stored in Google Cloud Secrets Manager
   - The health check uses the `config` object to detect configuration, which handles all sources correctly
   - If health check shows "degraded" but API endpoints work, check sync status
   - See `docs/troubleshooting/health-check-environment-variables.md` for details

### 3.3 Review Configuration System
- **File**: `config/secure-api-manager.py` (if exists)
- **Action**: Understand how configuration is managed
- **Check**: Secure configuration system usage

---

## 🏥 Step 4: Run Health Checks

### 4.1 Backend Health Check
Test the production backend API:

**Endpoints to check**:
1. **Basic Health**: 
   - URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health`
   - Expected: `200 OK` with health status

2. **Detailed Health**:
   - URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health/detailed`
   - Expected: Detailed service status

3. **Configuration Status**:
   - URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/config`
   - Expected: Configuration validation status

**Report**:
- HTTP status codes
- Service status (healthy/degraded/unhealthy)
- Environment configuration status
- Service connectivity (Supabase, OpenAI, GitHub, Google Cloud)

**Important Notes**:
- Health checks use the `config` object to detect configuration, which correctly handles all sources (env vars, Cloud Run vars, secrets)
- If health check shows "degraded" but endpoints work, configuration is likely correct
- The health check was updated (Nov 16, 2025) to use config object instead of `os.getenv()` directly for accurate detection
- See `docs/troubleshooting/health-check-environment-variables.md` for details on health check behavior

### 4.2 Key API Endpoints
Test critical endpoints:

1. **Agents Endpoint**:
   - URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/agents`
   - Expected: `200 OK` with agents list (or empty array)

2. **PRDs Endpoint**:
   - URL: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds`
   - Expected: `200 OK` with PRDs list

3. **MCP Server Status**:
   - URL: `https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/health`
   - Expected: MCP server health status

### 4.3 Frontend Status
- **URL**: `https://ai-agent-factory-frontend-952475323593.us-central1.run.app`
- **Check**: Frontend accessibility and status
- **Note**: Known SSR issue (documented in README)

### 4.4 Deployed Agents
Check deployed agents:
- **Redis Caching Agent**: `https://redis-caching-agent-fdqqqinvyq-uc.a.run.app/health`
- **Status**: Verify agent is running and healthy

---

## 📊 Step 5: Generate Summary Report

After completing all steps, provide a comprehensive summary:

### 5.1 Application Overview
- **What it does**: Brief description of the AI Agent Factory
- **Purpose**: Main goal and use case
- **Architecture**: High-level architecture (backend, frontend, infrastructure)
- **Technology Stack**: Key technologies used

### 5.2 Current Status
- **Production URLs**: All live service URLs
- **Health Status**: Overall system health
- **Service Status**: Status of each service (backend, frontend, MCP, agents)
- **Known Issues**: Any documented issues or limitations

### 5.3 Configuration Status
- **Environment**: Development or production
- **API Keys**: Which keys are configured (without showing values)
- **Missing Keys**: Any missing required configuration
- **Configuration Method**: How configuration is managed
  - **Local**: Encrypted file storage (`config/api-secrets.enc`) - Source of truth
  - **Production**: Google Cloud Secrets Manager (recommended) or Environment Variables
- **Secrets Sync Status**: Check if local and cloud are in sync (use `./scripts/verify-secrets-sync.sh`)
- **Secrets Update Order**: Always update local first, then sync to cloud
- **Health Check Status**: Note if health check shows "degraded" but endpoints work (likely detection issue, now fixed)
- **Production Configuration**: Note that production uses Cloud Secrets Manager or Cloud Run environment variables

### 5.4 Recent Changes
- **Latest Fixes**: Recent bug fixes and improvements
- **Deployments**: Recent deployment history
- **Documented Issues**: Issues resolved in resolution summaries

### 5.5 Project Structure
- **Key Directories**: Important directories and their purposes
- **Key Files**: Critical files for understanding the codebase
- **Documentation**: Available documentation resources

---

## 🎯 Execution Instructions

1. **Start with README**: Always begin by reading `README.md`
2. **Systematic Approach**: Follow steps 1-4 in order
3. **Document Findings**: Take notes as you go
4. **Verify Health**: Always run health checks to confirm current state
5. **Security First**: Never display sensitive information
6. **Comprehensive Summary**: Provide detailed summary in Step 5

---

## 📝 CRITICAL: Resolution Summary Documentation Requirement

**⚠️ MANDATORY**: If you make any code changes during this session, you **MUST** create a resolution summary document once the fix is resolved.

### **When to Create a Resolution Summary**

Create a resolution summary document (`docs/resolution-summaries/{issue-name}-resolution-{date}.md`) when:
- ✅ You fix a bug or issue
- ✅ You implement a new feature or system
- ✅ You resolve a configuration problem
- ✅ You deploy changes to production
- ✅ You make any code changes that affect functionality

### **Resolution Summary Template**

Use this template structure (see existing resolution summaries for examples):

```markdown
# [Issue Name] Resolution Summary

**Date**: [Date]
**Issue**: [Brief description]
**Status**: ✅ **RESOLVED** - [Brief status]
**Resolution Time**: [Time taken]

---

## 📋 Executive Summary
[High-level overview of the issue and resolution]

## 🔍 Issue Discovery
[How the issue was discovered, symptoms, investigation steps]

## 🐛 Root Cause Analysis
[Detailed analysis of the root cause]

## ✅ Solution Implementation
[What was fixed, how it was fixed, why it works]

## 🧪 Testing
[How the fix was tested, test results]

## 🚀 Deployment
[Deployment process and verification]

## 📊 Impact Analysis
[Before/after comparison]

## 📚 Documentation
[Documentation created or updated]

## 📝 Lessons Learned
[Technical and process lessons]

## 🔗 Related Files
[List of files modified/created]

## ✅ Verification Checklist
[Checklist of verification steps]

## 🎯 Conclusion
[Final status and confirmation]
```

### **Resolution Summary Requirements**

1. **File Location**: `docs/resolution-summaries/{descriptive-name}-resolution-{YYYY-MM-DD}.md`
2. **Naming Convention**: Use descriptive names like:
   - `agents-endpoint-500-error-resolution-2025-11-16.md`
   - `secrets-management-implementation-resolution-2025-11-16.md`
   - `health-check-detection-fix-resolution-2025-11-16.md`

3. **Content Requirements**:
   - **Executive Summary**: High-level overview
   - **Root Cause**: Detailed analysis
   - **Solution**: What was changed and why
   - **Testing**: How it was verified
   - **Deployment**: Production deployment details
   - **Impact**: Before/after comparison
   - **Lessons Learned**: Key takeaways

4. **Update Related Files**:
   - Update `CHANGELOG.md` with the fix
   - Update relevant documentation if needed
   - Update this startup prompt if workflow changes

### **Why This Matters**

- **Knowledge Preservation**: Future sessions can learn from past fixes
- **Pattern Recognition**: Helps identify recurring issues
- **Onboarding**: New developers can understand system history
- **Debugging**: Provides context for similar issues
- **Process Improvement**: Documents what works and what doesn't

### **Examples of Good Resolution Summaries**

- `docs/resolution-summaries/agent-display-issue-resolution.md`
- `docs/resolution-summaries/secrets-management-implementation-resolution.md`
- `docs/resolution-summaries/agents-endpoint-500-error-resolution-nov-16-2025.md`

**Remember**: If you change code, document it. This is not optional - it's essential for maintaining project knowledge and preventing regression.

---

## 📝 Expected Output Format

After completing all steps, provide your findings in this format:

```markdown
# AI Agent Factory - Session Startup Report

## Application Overview
[Brief description of what the application does]

## Current Status
- Backend: [Status]
- Frontend: [Status]
- MCP Server: [Status]
- Deployed Agents: [List and status]

## Health Check Results
- Backend Health: [Status]
- API Endpoints: [Status]
- Services: [Status of each service]

## Configuration Status
- Environment: [dev/prod]
- API Keys Configured: [List without values]
- Missing Keys: [List if any]

## Recent Issues & Resolutions
[Summary of documented issues and fixes]

## Project Structure
[Key directories and files]

## Ready for Development
[Confirmation that you understand the codebase and are ready to work]
```

---

## ⚠️ Important Notes

1. **Security**: Never display API keys, tokens, or secrets
2. **Production**: This is a live production application - be careful with changes
3. **Documentation**: Always check documentation before making assumptions
4. **Health Checks**: Always verify current state before making changes
5. **Resolution History**: Review previous fixes to avoid repeating mistakes
6. **Resolution Summaries**: **MANDATORY** - Create a resolution summary document for any code changes (see "Resolution Summary Documentation Requirement" section above)

---

**Start Now**: Begin with Step 1.1 - Read the README file.

