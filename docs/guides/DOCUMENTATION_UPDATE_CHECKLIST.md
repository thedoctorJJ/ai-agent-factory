# Documentation Update Checklist

**Purpose**: Comprehensive checklist of all key documents that should be reviewed and potentially updated after solving any problem or implementing any feature.

**When to use**: After completing Phase 4 (Documentation) in the AI Agent Workflow - specifically after creating your resolution summary.

---

## 📋 Core Documents (ALWAYS Review)

### 1. **CHANGELOG.md** ✅ MANDATORY
**Location**: `/CHANGELOG.md`

**Update when**:
- ANY code changes
- ANY bug fixes
- ANY new features
- ANY enhancements
- ANY configuration changes

**What to add**:
```markdown
## [Unreleased] - YYYY-MM-DD

### 🔧 **[Feature/Fix Name] - [TYPE]**
- **✅ Feature**: [Brief description]
- **✅ Purpose**: [Why this was needed]
- **✅ Implementation**: [How it was done]
- **✅ Benefits**: [What this improves]
- **✅ Status**: [Current state]

### **Technical Details**
- **Files Created**: [List]
- **Files Modified**: [List]
- **Testing**: [How verified]
```

**Always include**: Reference to resolution summary

---

### 2. **Resolution Summary** ✅ MANDATORY
**Location**: `/docs/resolution-summaries/`

**Create for**:
- ALL problem-solving (not just bugs)
- Features
- Enhancements
- Deployments
- Configuration fixes
- ANY code changes

**How to create**:
```bash
./scripts/dev/create-resolution-summary.sh
```

**Template includes**:
1. Executive Summary
2. Issue Discovery
3. Root Cause Analysis
4. Solution Implementation
5. Testing
6. Deployment (if applicable)
7. Impact Analysis
8. Lessons Learned
9. Related Files
10. Verification Checklist
11. Conclusion

---

### 3. **README.md** (Project Root)
**Location**: `/README.md`

**Update when**:
- New major features added
- Architecture changes
- New production URLs
- Project status changes
- New dependencies
- Setup instructions change
- New integrations
- Production deployment changes

**Key sections to review**:
- 🌐 Live Production Application (URLs, status)
- 🔧 Recent Updates & Fixes
- ✅ Project Status
- 🚀 Quick Start
- 📋 PRD System (if PRD-related)
- 🏗️ Architecture (if structure changes)

---

## 📚 Subsystem Documentation (Review When Relevant)

### 4. **Startup Prompt**
**Location**: `/.cursor/startup-prompt.md`

**Update when**:
- Workflow changes
- New health checks added
- Environment config changes
- New scripts in startup flow
- New critical files to check

**Remember**: This is Phase 1 of AI Agent Workflow - keep it current!

---

### 5. **AI Agent Workflow**
**Location**: `/docs/guides/AI_AGENT_WORKFLOW.md`

**Update when**:
- Development process changes
- New linting tools added
- New quality gates
- New documentation requirements
- Git commit standards change
- New helper scripts

---

### 6. **Quick Reference Card**
**Location**: `/.cursor/QUICK_REFERENCE.md`

**Update when**:
- New commands added
- New scripts created
- Workflow steps change
- Important file locations change

---

### 7. **Linting System Documentation**
**Location**: `/.cursor/LINTING_SYSTEM.md`

**Update when**:
- Linting tools installed/removed
- Linting scripts added
- Linting configuration changes
- Pre-commit hooks updated
- CI/CD linting changes

**Current status**: 🚧 Incomplete - update when linting system is implemented

---

## 🔒 Security & Configuration

### 8. **Secrets Management Docs**
**Locations**:
- `/docs/security/SECRETS_QUICK_REFERENCE.md`
- `/docs/security/SECRETS_SYNC_STRATEGY.md`
- `/docs/security/SECRETS_MANAGEMENT.md`

**Update when**:
- New secrets added
- Secrets workflow changes
- Cloud sync process changes
- Security practices updated

---

### 9. **Environment Configuration**
**Location**: `/config/README.md`

**Update when**:
- New environment variables required
- Configuration structure changes
- New config files added
- Setup process changes

---

## 🏗️ Architecture & Technical Guides

### 10. **Architecture Overview**
**Location**: `/docs/architecture/01-architecture-overview.md`

**Update when**:
- System architecture changes
- New services added
- Technology stack changes
- Integration points change

---

### 11. **Deployment Guide**
**Location**: `/docs/deployment/06-deployment-guide.md`

**Update when**:
- Deployment process changes
- New services deployed
- Cloud configuration changes
- CI/CD pipeline updates

---

### 12. **API Contract Documentation**
**Location**: `/docs/api/API_CONTRACT.md`

**Update when**:
- New API endpoints added
- Endpoints modified/removed
- Request/response schemas change
- API versioning changes

**Don't forget**:
```bash
# Regenerate OpenAPI spec
python3 scripts/api/generate-openapi-spec.py

# Regenerate TypeScript types
./scripts/api/generate-typescript-types.sh
```

---

## 📋 PRD System (If PRD-Related)

### 13. **PRD Guides**
**Locations**:
- `/docs/guides/04-prd-system.md` - Main PRD system guide
- `/docs/guides/PRD_SYNC_STRATEGY.md` - PRD sync documentation
- `/docs/guides/PRD_QUICK_REFERENCE.md` - Quick reference
- `/docs/guides/INCOMING_PRD_WORKFLOW.md` - Incoming PRD workflow

**Update when**:
- PRD processing changes
- New PRD types added
- Sync strategy changes
- PRD templates updated
- PRD status workflow changes

---

### 14. **PRD Templates**
**Location**: `/prds/templates/`

**Update when**:
- New template sections added
- Template structure changes
- Requirements change

---

## 🤖 Agent Management (If Agent-Related)

### 15. **Agent Management Guide**
**Location**: `/docs/guides/05-agent-management.md`

**Update when**:
- Agent lifecycle changes
- New agent features
- Deployment process changes
- Health check changes

---

### 16. **Agent Deployment Guides**
**Locations**:
- `/docs/guides/redis-agent-migration.md` (example)
- Any agent-specific guides

**Update when**:
- Deployment process changes
- Configuration requirements change
- Integration patterns change

---

## 🔌 Integration Guides (If Integration-Related)

### 17. **MCP Server Documentation**
**Locations**:
- `/docs/guides/MCP_SETUP_SIMPLIFIED.md`
- `/docs/guides/MCP_QUICK_START.md`
- `/docs/guides/CURSOR_MCP_SUPABASE_SETUP.md`

**Update when**:
- MCP server changes
- New tools added
- Setup process changes
- Connection configuration changes

---

### 18. **Cursor Agent Integration**
**Location**: `/docs/guides/08-cursor-agent-integration.md`

**Update when**:
- Integration process changes
- New features available
- Setup steps change

---

### 19. **Devin AI Integration**
**Location**: `/docs/guides/02-devin-ai-integration.md`

**Update when**:
- Devin workflow changes
- Integration points change
- Manual workflow updates

---

## 🗄️ Database & Infrastructure (If DB-Related)

### 20. **Supabase Guides**
**Locations**:
- `/docs/guides/SUPABASE_AUTO_UNPAUSE.md`
- `/docs/guides/FIX_FOREIGN_KEY_RLS_GUIDE.md`
- `/docs/guides/VERIFY_RLS_FIX.md`

**Update when**:
- Database schema changes
- RLS policies updated
- Supabase configuration changes
- Connection issues resolved

---

### 21. **Health Check Documentation**
**Location**: Embedded in README.md and various guides

**Update when**:
- Health check endpoints added/changed
- Status reporting changes
- Monitoring system updates

---

## 🚨 Troubleshooting (If Relevant)

### 22. **Troubleshooting Guides**
**Location**: `/docs/troubleshooting/`

**Create/Update when**:
- Common issues identified
- Resolution patterns emerge
- Error patterns documented

**Files to consider**:
- `README.md` - Troubleshooting index
- Individual issue guides (if recurring)

---

## 📊 Project Status & Planning

### 23. **Project Status**
**Location**: `/docs/getting-started/07-project-status.md`

**Update when**:
- Milestones completed
- Major features deployed
- Project phase changes
- Status updates needed

---

### 24. **Deployment Status**
**Location**: `/docs/deployment/DEPLOYMENT_STATUS.md`

**Update when**:
- Services deployed
- Deployment status changes
- Production URLs change
- Service configuration updates

---

## 🎯 Decision Matrix: What to Update When

### After Fixing a Bug
- ✅ **MANDATORY**: Resolution summary, CHANGELOG
- 🔍 **Review**: README (if user-facing), Troubleshooting guides
- 📝 **Consider**: Related subsystem guides

### After Adding a Feature
- ✅ **MANDATORY**: Resolution summary, CHANGELOG, README
- 🔍 **Review**: Quick Reference, Workflow (if process changes)
- 📝 **Consider**: API docs, Architecture docs, Guide docs

### After Changing Configuration
- ✅ **MANDATORY**: Resolution summary, CHANGELOG
- 🔍 **Review**: Startup prompt, Environment docs, Secrets docs
- 📝 **Consider**: README, Deployment guide

### After Deployment
- ✅ **MANDATORY**: Resolution summary, CHANGELOG, README (URLs), Deployment Status
- 🔍 **Review**: Architecture docs, Health check docs
- 📝 **Consider**: Deployment guide updates

### After Workflow Changes
- ✅ **MANDATORY**: Resolution summary, CHANGELOG, AI_AGENT_WORKFLOW
- 🔍 **Review**: Startup prompt, Quick Reference
- 📝 **Consider**: README (if affects setup)

### After Security Changes
- ✅ **MANDATORY**: Resolution summary, CHANGELOG, Security docs
- 🔍 **Review**: README, Secrets management docs
- 📝 **Consider**: Deployment guide, Environment docs

### After Database Changes
- ✅ **MANDATORY**: Resolution summary, CHANGELOG, Supabase guides
- 🔍 **Review**: Architecture docs, API docs (if schema affects API)
- 📝 **Consider**: Troubleshooting guides

---

## 🔄 Update Process Workflow

```
1. Solve Problem
   ↓
2. Check Repository Structure (Phase 3.1)
   ./scripts/dev/check-repo-structure.sh
   - Ensure clean, organized repo
   ↓
3. Create Resolution Summary (Phase 4.1)
   ./scripts/dev/create-resolution-summary.sh
   ↓
4. Update CHANGELOG (Phase 4.2)
   - Add entry with resolution summary reference
   ↓
5. Review This Checklist (Phase 4.3)
   - Use Decision Matrix above
   - Check each relevant section
   ↓
6. Update Relevant Docs
   - Core docs (always)
   - Subsystem docs (if relevant)
   - Integration docs (if applicable)
   ↓
7. Git Commit (Phase 5)
   - Stage all updated docs together
   - Reference resolution summary in commit
   ↓
8. Verify
   - Check git status
   - Ensure all docs committed
   - Repository structure is clean
```

---

## 📁 Quick File Reference

**Always Update**:
- `/CHANGELOG.md`
- `/docs/resolution-summaries/[issue]-resolution-[date].md`

**Frequently Updated**:
- `/README.md`
- `/.cursor/startup-prompt.md`
- `/docs/guides/AI_AGENT_WORKFLOW.md`
- `/.cursor/QUICK_REFERENCE.md`

**Conditionally Updated** (see Decision Matrix):
- All guides in `/docs/guides/`
- Security docs in `/docs/security/`
- Architecture docs in `/docs/architecture/`
- Deployment docs in `/docs/deployment/`
- API docs in `/docs/api/`
- Troubleshooting in `/docs/troubleshooting/`

---

## ⚠️ Common Mistakes to Avoid

❌ **Don't skip CHANGELOG**
- EVERY code change needs CHANGELOG entry
- Reference resolution summary

❌ **Don't skip resolution summary**
- MANDATORY for ALL problem-solving
- Use helper script: `./scripts/dev/create-resolution-summary.sh`

❌ **Don't forget README.md**
- Update production URLs when they change
- Update status when major features deploy
- Keep "Recent Updates" section current

❌ **Don't forget Quick Reference**
- New scripts need to be added
- New commands should be documented

❌ **Don't update outdated guides**
- Check `/docs/legacy/` - these should NOT be updated
- Only update active guides

❌ **Don't forget API regeneration**
- If API changes, regenerate OpenAPI spec
- Regenerate TypeScript types

---

## ✅ Verification Checklist

Before committing:
- [ ] Resolution summary created and complete
- [ ] CHANGELOG updated with full details
- [ ] README reviewed and updated (if needed)
- [ ] Relevant subsystem guides updated
- [ ] Quick Reference updated (if new commands)
- [ ] Startup prompt updated (if workflow changes)
- [ ] All updated docs added to git
- [ ] Git commit message references resolution summary

---

**Last Updated**: November 27, 2025  
**Version**: 1.0  
**Status**: ✅ Active - Use after every problem solved

**Remember**: Good documentation is knowledge preservation. Future you (and future AI agents) will thank present you!

