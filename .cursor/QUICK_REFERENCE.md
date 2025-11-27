# Quick Reference - AI Agent Commands

**For AI Agents**: Use these commands throughout your session

---

## 🚀 Session Start (Every Time)

```bash
# 1. Run startup prompt (includes health checks, PRD sync)
# Follow: .cursor/startup-prompt.md

# 2. Check linting tools availability
./scripts/dev/check-linting-tools.sh

# 3. Read workflow
# Read: docs/guides/AI_AGENT_WORKFLOW.md
```

---

## 🛠️ Development (During Work)

### Linting (Throughout Development)

```bash
# Shell scripts (syntax check)
bash -n path/to/script.sh

# Python files (syntax check)
python3 -m py_compile path/to/file.py

# Markdown (use Cursor tool)
# read_lints(["path/to/file.md"])
```

---

## ✅ Before Commit (Quality Assurance)

### **🚀 ONE COMMAND TO DOCUMENT EVERYTHING:**

```bash
./scripts/dev/document-solution.sh
```

**This interactive script does EVERYTHING**:
1. ✅ Creates resolution summary (prompts you for details)
2. ✅ Reminds you to update CHANGELOG (shows template)
3. ✅ **Checks repository structure** (ensures clean, organized repo)
4. ✅ Shows documentation checklist (decision matrix)
5. ✅ Guides you through git commit (structured format)
6. ✅ **Syncs entire repository with GitHub** (commits and pushes ALL changes)

**Just run this ONE command after solving any problem!**

**The script now ensures the ENTIRE repository is synced, not just the current changes!**

---

### **Check Repository Structure** (NEW!)

```bash
./scripts/dev/check-repo-structure.sh
```

**Ensures**:
- No loose files in root
- Files in correct directories
- No temporary/test files
- No large files
- Clean, professional structure

**Run this regularly to keep the repository organized!**

---

**💬 For natural language**: Just say things like:
- "invoke the lint, doc update, github sync command"
- "document this solution"
- "let's document and commit"
- "run the documentation workflow"

AI agents will understand and run the script!

---

### Or Do It Manually (Step-by-Step):

#### 1. Create Resolution Summary (MANDATORY)

```bash
./scripts/dev/create-resolution-summary.sh
```

**What it does**:
- Prompts for issue name, description, type, status, time
- Creates template: `docs/resolution-summaries/[issue-name]-resolution-YYYY-MM-DD.md`
- Opens in editor
- **Complete ALL sections before continuing**

### 2. Lint All Modified Files

```bash
# Check all shell scripts
for f in $(git diff --name-only | grep '\.sh$'); do
    bash -n "$f"
done

# Check all Python files
for f in $(git diff --name-only | grep '\.py$'); do
    python3 -m py_compile "$f"
done
```

### 3. Run Tests (if applicable)

```bash
# Backend tests
cd backend && python -m pytest tests/

# Frontend tests (when available)
cd frontend/next-app && npm test
```

### 4. Verify Health Checks

```bash
# Check all systems
./scripts/health-check-mcp-database.py

# Verify PRD count
curl -k https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds | jq .total
```

---

## 📝 Documentation (MANDATORY)

### 1. Resolution Summary (Already done above)
**File**: `docs/resolution-summaries/[issue-name]-resolution-YYYY-MM-DD.md`

### 2. Update CHANGELOG

```bash
vim CHANGELOG.md
```

**Add**:
```markdown
## [Unreleased] - YYYY-MM-DD

### 🔧 **[Feature/Fix Name] - [TYPE]**
- **✅ Feature**: [Description]
- **✅ Purpose**: [Why]
- **✅ Implementation**: [How]
- **✅ Benefits**: [Impact]

### **Technical Details**
- **Files Created**: [List]
- **Files Modified**: [List]
```

### 3. Update Other Docs (Use Checklist!)

**📋 IMPORTANT**: Review `docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md`

This comprehensive checklist covers 24 document categories with a decision matrix:
- After fixing a bug → What to update
- After adding a feature → What to update  
- After deployment → What to update
- After config changes → What to update
- etc.

**Don't guess which docs to update - use the checklist!**

---

## 🎯 Git Commit (Structured)

### Review and Stage

```bash
# Review all changes
git status
git diff

# Stage related files together
git add [files-for-feature-1]
git commit -m "..." 
git add [files-for-feature-2]
git commit -m "..."
```

### Commit Message Format

```
type(scope): brief description

- Detailed explanation of what changed
- Why it was needed
- Any breaking changes or important notes

Related: #issue-number (if applicable)
Refs: docs/resolution-summaries/[filename].md
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

**Example**:
```
feat(startup): add smart Supabase pause detection and auto-sync

- Created scripts/check-supabase-and-sync.sh for intelligent pause detection
- Detects when Supabase is paused vs just empty
- Shows dashboard link with clear unpause instructions
- Auto-syncs PRDs once database is accessible

Benefits:
- Handles frequent Supabase pauses gracefully
- Clear user guidance when manual action needed
- Automatic recovery after unpause

Refs: docs/resolution-summaries/startup-prompt-prd-sync-enhancement-2025-11-27.md
```

### Push

```bash
git push origin main
```

---

## 🏁 Session End (Verification)

### Final Checklist

```bash
# 1. Verify commit
git log -1

# 2. Verify production
curl -k https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds

# 3. Clean up temp files
rm -f /tmp/*.json
rm -f /tmp/*.txt

# 4. Verify all files committed
git status
# Should show: "working tree clean"
```

---

## 📚 Important Files

**Read First**:
- `.cursor/startup-prompt.md` - Session startup procedure
- `docs/guides/AI_AGENT_WORKFLOW.md` - Complete workflow (6 phases)
- `.cursor/LINTING_SYSTEM.md` - Current linting status

**Use Often**:
- `scripts/dev/check-linting-tools.sh` - Check linting availability
- `scripts/dev/create-resolution-summary.sh` - Create resolution docs
- `CHANGELOG.md` - Project history

**Reference Examples**:
- `docs/resolution-summaries/` - Previous resolution summaries

---

## ⚠️ Critical Rules

1. **ALWAYS** run startup prompt at session start
2. **ALWAYS** check linting status before starting work
3. **ALWAYS** lint during development (not just at end)
4. **ALWAYS** create resolution summary (MANDATORY for all problem-solving)
5. **ALWAYS** update CHANGELOG
6. **ALWAYS** use structured commit messages
7. **NEVER** skip documentation
8. **NEVER** commit without linting
9. **NEVER** push without verification

---

## 🎯 Quick Workflow Summary

```
1. Session Start
   └─ Run startup prompt
   └─ Check linting tools
   └─ Read workflow

2. Problem Solving
   └─ Understand → Implement → Lint → Test

3. Quality Assurance
   └─ Comprehensive linting
   └─ Run tests
   └─ Verify health checks

4. Documentation (MANDATORY)
   └─ Create resolution summary (helper script)
   └─ Update CHANGELOG
   └─ Update other docs

5. Git Commit
   └─ Review changes
   └─ Stage logically
   └─ Structured commit message
   └─ Push to GitHub

6. Session Closure
   └─ Final verification
   └─ Clean up
   └─ Session summary
```

---

**Last Updated**: November 27, 2025  
**Version**: 1.0  
**Status**: ✅ Active - Use for all sessions

