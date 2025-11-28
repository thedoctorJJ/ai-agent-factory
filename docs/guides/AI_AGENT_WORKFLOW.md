# AI Agent Development Workflow

**Purpose**: Standardized workflow for AI agent sessions to ensure quality, consistency, and documentation

**Last Updated**: November 27, 2025

---

## 🎯 Core Principles

1. **Start with Context**: Every session begins with understanding the system
2. **Lint Throughout**: Use linting tools continuously, not just at the end
3. **Document Everything**: Every fix gets a resolution summary
4. **Commit Properly**: Follow git best practices with meaningful commits
5. **Test Before Deploy**: Verify changes work before pushing

---

## 📋 Standard Session Workflow

### Phase 1: Session Startup (Always Run First)

**Purpose**: Get context, verify environment, understand linting

#### Step 1.1: Run Startup Prompt

```bash
# This is MANDATORY at the start of every session
# Located in: .cursor/startup-prompt.md
# AI Agent should execute all steps in order
```

**What this does**:

1. Reads README and key documentation
2. Reviews previous issue resolutions
3. Checks environment configuration
4. Verifies Docker is running
5. Tests Supabase connection and syncs PRDs
6. Runs health checks on all services
7. Generates comprehensive status report

**Output**: AI agent has full context and system status

#### Step 1.2: Understand Linting System

```bash
# Check what linting is available
cat .cursor/LINTING_SYSTEM.md

# Verify linting tools are installed
./scripts/dev/check-linting-tools.sh
```

**AI Agent must**:

- Know which linters are available for each file type
- Understand how to run linting
- Be aware of linting standards and rules
- Remember to lint throughout the session, not just at end

---

### Phase 2: Problem Solving (Main Work)

**Purpose**: Address the user's request with quality and testing

#### Step 2.1: Understand the Problem

- Read any referenced files or documentation
- Ask clarifying questions if needed
- Break down complex tasks into steps
- Create TODOs for multi-step tasks

#### Step 2.2: Implement Solution

- Write code following project conventions
- **Lint as you go** - don't wait until the end
- Test changes incrementally
- Handle edge cases and errors

#### Step 2.3: Lint During Development

```bash
# IMPORTANT: Lint DURING development, not after

# Python files
black <file>.py
flake8 <file>.py
mypy <file>.py

# TypeScript/JavaScript files  
npm run lint:fix <file>.ts

# Shell scripts
shellcheck <file>.sh

# Markdown files (built-in)
# Cursor's read_lints tool handles this automatically
```

**Why lint during development**:

- Catch issues immediately
- Don't accumulate linting debt
- Easier to fix in context
- Better code quality throughout

#### Step 2.4: Test Changes

- Run relevant tests
- Verify functionality manually
- Check integration points
- Test edge cases

---

### Phase 3: Quality Assurance (Before Commit)

**Purpose**: Ensure everything is production-ready and well-organized

#### Step 3.1: Check Repository Structure

**Keep the repository clean and organized**:

```bash
./scripts/dev/check-repo-structure.sh
```

**What this checks**:

- ✅ No loose files in root directory
- ✅ Python files in correct locations (backend/, scripts/, config/)
- ✅ JS/TS files in correct locations (frontend/)
- ✅ Shell scripts in scripts/ directory
- ✅ Documentation properly organized
- ✅ No temporary/test files (.tmp, .bak, ~, .swp)
- ✅ No large files (> 5MB) that shouldn't be tracked
- ✅ No empty directories
- ✅ Expected directory structure present
- ✅ No duplicate file names

**If issues found**: Fix them before proceeding!

**Why this matters**:

- Clean, organized repository is easier to navigate
- Prevents confusion about where files belong
- Maintains professional appearance
- Makes onboarding easier for new contributors

#### Step 3.2: Comprehensive Linting

```bash
# Run full linting suite
./scripts/dev/lint-all.sh

# Or lint specific areas:
./scripts/dev/lint-backend.sh
./scripts/dev/lint-frontend.sh
./scripts/dev/lint-scripts.sh
```

**AI Agent checklist**:

- [ ] All Python files pass black, flake8, mypy
- [ ] All TypeScript files pass ESLint
- [ ] All shell scripts pass shellcheck
- [ ] All markdown files have no linter errors
- [ ] No console.log or debug statements left in code
- [ ] No TODO comments without associated issues

#### Step 3.2: Run Tests

```bash
# Backend tests
cd backend && pytest

# Frontend tests (when available)
cd frontend/next-app && npm test

# Integration tests
./scripts/testing/run-integration-tests.sh
```

#### Step 3.3: Verify Health Checks

```bash
# Ensure system still works
./scripts/check-supabase-and-sync.sh

# Test critical endpoints
curl -k -s https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health | jq
```

---

### Phase 4: Documentation (Always Required)

**Purpose**: Preserve knowledge and context for future sessions

**⚠️ CRITICAL**: This phase is **MANDATORY** after solving any problem. Don't skip it!

---

### 🚀 **QUICK START: ONE COMMAND FOR EVERYTHING**

```bash
./scripts/dev/document-solution.sh
```

**This interactive script handles the entire documentation workflow**:

1. ✅ Creates resolution summary (Step 4.1)
2. ✅ Guides CHANGELOG update (Step 4.2)
3. ✅ Shows documentation checklist (Step 4.3)
4. ✅ Helps with git commit (Phase 5)

**Just run this command and follow the prompts!**

---

### 💬 **For AI Agents: Natural Language Commands**

When the user says any of these, run `./scripts/dev/document-solution.sh`:

- "invoke the lint, doc update, github sync command"
- "run the documentation workflow"
- "document this solution"
- "let's document this"
- "time to document"
- "document and commit"
- "sync everything"
- "wrap this up with docs"
- "I solved the problem, what's next?"
- "ready to commit"
- "let's finish this properly"

**Any phrase about documenting/committing/syncing = run this script!**

---

### Or Follow Manual Steps

#### Step 4.1: Create Resolution Summary (ALWAYS for problem-solving)

**When to create**:

- ✅ Fixed a bug
- ✅ Implemented a feature
- ✅ Enhanced existing functionality
- ✅ Resolved a configuration issue
- ✅ Deployed changes to production
- ✅ Made any code changes that solve a problem

**Use the helper script**:

```bash
./scripts/dev/create-resolution-summary.sh
```

**What this script does**:

1. Prompts for issue name (auto-generates filename)
2. Prompts for basic info (description, type, status, time)
3. Creates template with all required sections
4. Opens in editor for you to complete
5. Provides checklist of what to fill in

**Interactive prompts**:

```text
What issue did you solve? → agents-endpoint-500-error
Brief description: → Endpoint returning 500 error
Type: → bug
Status: → RESOLVED
Resolution time: → 2 hours
```

**Generated file**: `docs/resolution-summaries/agents-endpoint-500-error-resolution-2025-11-27.md`

**Required sections** (in template):

1. ✅ Executive Summary (2-3 paragraphs)
2. ✅ Issue Discovery (symptoms, investigation)
3. ✅ Root Cause Analysis (why it happened)
4. ✅ Solution Implementation (what you fixed)
5. ✅ Testing (how you verified)
6. ✅ Deployment (production deployment details, if applicable)
7. ✅ Impact Analysis (before/after comparison)
8. ✅ Lessons Learned (technical and process)
9. ✅ Related Files (all files modified/created)
10. ✅ Verification Checklist (check off all items)
11. ✅ Conclusion (final status)

**Complete ALL sections** before moving to next step.

**See examples**: `docs/resolution-summaries/` for reference

#### Step 4.2: Update CHANGELOG

```bash
# Add entry to CHANGELOG.md with:
# - Date
# - Feature/Fix description
# - Technical details
# - Files changed
```

**Format**:

```markdown
## [Unreleased] - YYYY-MM-DD

### 🔧 **[Feature Name] - [TYPE]**
- **✅ Feature**: [Brief description]
- **✅ Purpose**: [Why this was needed]
- **✅ Implementation**: [How it was done]
- **✅ Benefits**: [What this improves]
- **✅ Status**: [Current state]

### **Technical Details**
- **Files Created**: [List new files]
- **Files Modified**: [List changed files]
- **Testing**: [How it was tested]
```

**Important**: Add reference to resolution summary in CHANGELOG

#### Step 4.3: Update Relevant Documentation

**📋 Use the comprehensive checklist**: `docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md`

**This checklist covers 24 document categories**:

- Core docs (README, startup prompt, workflow)
- Security & configuration docs
- Architecture & technical guides
- PRD system docs
- Agent management docs
- Integration guides (MCP, Cursor, Devin)
- Database & infrastructure docs
- Troubleshooting guides
- Project status & planning

**Quick Decision Matrix** (in checklist):

- After fixing a bug → Update X, Y, Z docs
- After adding a feature → Update A, B, C docs
- After deployment → Update D, E, F docs
- etc.

**Don't guess - use the checklist!** It ensures nothing is forgotten.

---

### Phase 5: Git Commit (Structured Process)

**Purpose**: Clean, atomic commits with meaningful messages

#### Step 5.1: Review Changes

```bash
# See what changed
git status

# Review diffs
git diff

# Check for unintended changes
git diff --staged
```

#### Step 5.2: Stage Files Logically

```bash
# Stage related changes together
git add [files for specific feature/fix]

# Don't stage everything at once unless it's all related
# Avoid: git add .
```

#### Step 5.3: Write Meaningful Commit Message

```bash
git commit -m "type(scope): description

- Detailed explanation of what changed
- Why it was needed
- Any breaking changes or important notes

Related: #issue-number (if applicable)
Refs: docs/resolution-summaries/[filename].md
"
```

**Commit Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, linting
- `refactor`: Code restructuring
- `test`: Test additions/changes
- `chore`: Build, config, dependencies
- `perf`: Performance improvements

**Examples**:

```bash
# Good
git commit -m "feat(startup): add dynamic PRD count to Supabase sync

- Changed hardcoded '8 PRDs' to dynamic file counting
- Script now counts .md files in prds/queue/ automatically
- Updates all documentation to reflect dynamic behavior
- Future-proof for any number of PRDs

Refs: docs/resolution-summaries/2025-11-27-startup-prompt-prd-sync-enhancement.md
"

# Bad
git commit -m "fixed stuff"
git commit -m "updates"
```

#### Step 5.4: Sync Entire Repository with GitHub

**IMPORTANT**: Always sync the ENTIRE repository, not just current changes!

```bash
# Check for ANY uncommitted changes
git status --short

# If there are uncommitted changes, stage and commit ALL of them
git add -A
git commit -m "chore: sync all remaining changes"

# Push everything to GitHub
git push origin main

# Verify complete sync
git status  # Should show "nothing to commit, working tree clean"
```

**Why sync everything?**:

- ✅ Ensures no work is lost
- ✅ Keeps repository fully synced
- ✅ Prevents accumulation of uncommitted changes
- ✅ Makes collaboration easier
- ✅ Complete backup to GitHub
- ✅ No surprises for other developers or AI agents

**The `document-solution.sh` script handles this automatically in Step 6!**

---

### Phase 6: Session Closure (Clean Exit)

**Purpose**: Ensure nothing is left incomplete

#### Step 6.1: Final Verification

- [ ] All changes committed and pushed
- [ ] CHANGELOG updated
- [ ] Documentation updated
- [ ] **Resolution summary created** (MANDATORY for all problem-solving)
- [ ] Linting passed
- [ ] Tests passed
- [ ] Health checks passed

#### Step 6.2: Clean Up Temporary Files

```bash
# Remove any test files, debug scripts, etc.
rm -f /tmp/test-*.json
rm -f debug-*.log
```

#### Step 6.3: Session Summary

AI Agent provides:

- Summary of what was accomplished
- List of files changed
- Any follow-up items needed
- Verification that all steps completed

---

## 🚫 Anti-Patterns to Avoid

### Don't Do This

❌ **Skip startup prompt**

- Always run the full startup prompt
- Don't assume you know the current state

❌ **Lint only at the end**

- Lint throughout development
- Fix linting issues immediately

❌ **Commit without documentation**

- Every significant change needs documentation
- Update CHANGELOG for all user-facing changes

❌ **Push without testing**

- Always verify changes work
- Run health checks before pushing

❌ **Generic commit messages**

- "fixed bug" tells us nothing
- "updated files" is meaningless

❌ **Skip resolution summaries**

- **MANDATORY** for ALL problem-solving (not just bugs)
- Use `./scripts/dev/create-resolution-summary.sh` helper
- Complete ALL sections before committing
- Future you will thank present you

❌ **Accumulate changes**

- Commit logical units of work
- Don't wait until everything is done

❌ **Ignore linting errors**

- Fix linting issues immediately
- Don't disable linters to bypass errors

---

## 🎯 Quick Reference Checklist

### Every Session Start

- [ ] Run full startup prompt
- [ ] Read linting system documentation
- [ ] Verify linting tools are available
- [ ] Check recent changes (git log)

### During Development

- [ ] Lint files as you edit them
- [ ] Test changes incrementally
- [ ] Document complex decisions
- [ ] Handle errors gracefully

### Before Commit

- [ ] Run comprehensive linting
- [ ] Run all tests
- [ ] Verify health checks pass
- [ ] **Create resolution summary** (MANDATORY - use helper script)
- [ ] Update CHANGELOG (reference resolution summary)
- [ ] Update relevant documentation

### Git Commit

- [ ] Review all changes (git diff)
- [ ] Stage logically related files
- [ ] Write meaningful commit message
- [ ] Reference documentation
- [ ] Push to GitHub

### Session End

- [ ] All changes committed
- [ ] All documentation updated
- [ ] All temporary files cleaned up
- [ ] Provide session summary

---

## 📖 Complete Example: Fixing a Bug

### Scenario: "Website shows 0 PRDs after Supabase pause"

**Phase 1: Session Startup**

```bash
# 1. Run startup prompt (includes health checks, PRD sync)
# 2. Check linting: ./scripts/dev/check-linting-tools.sh
# 3. Discover: PRD count is 0, Supabase was paused
```

**Phase 2: Problem Solving**

```bash
# 1. Understand: Supabase pauses wipe data, happens frequently
# 2. Implement: Create smart detection script
# 3. Lint during: bash -n check-supabase-and-sync.sh
# 4. Test: Run script, verify it detects and syncs
```

**Phase 3: Quality Assurance**

```bash
# 1. Lint all modified files
bash -n scripts/check-supabase-and-sync.sh
read_lints([".cursor/startup-prompt.md"])

# 2. Test functionality
./scripts/check-supabase-and-sync.sh
# Result: ✅ All systems operational, 8 PRDs synced

# 3. Verify health
curl -k https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds
# Result: {"total": 8, ...}
```

**Phase 4: Documentation**

```bash
# 1. Create resolution summary (FIRST!)
./scripts/dev/create-resolution-summary.sh
# → Prompts for: issue name, description, type, status, time
# → Creates: docs/resolution-summaries/2025-11-27-startup-prompt-prd-sync-enhancement.md
# → Open and complete ALL sections

# 2. Update CHANGELOG
vim CHANGELOG.md
# → Add entry with reference to resolution summary

# 3. Update other docs
vim .cursor/startup-prompt.md  # Updated Step 4.0.1
vim docs/guides/SUPABASE_AUTO_UNPAUSE.md  # Created new guide
```

**Phase 5: Git Commit**

```bash
# 1. Review changes
git status
git diff

# 2. Stage related files
git add scripts/check-supabase-and-sync.sh
git add .cursor/startup-prompt.md
git add CHANGELOG.md
git add docs/resolution-summaries/2025-11-27-startup-prompt-prd-sync-enhancement.md
git add docs/guides/SUPABASE_AUTO_UNPAUSE.md

# 3. Commit with structured message
git commit -m "feat(startup): add smart Supabase pause detection and auto-sync

- Created scripts/check-supabase-and-sync.sh for intelligent pause detection
- Detects when Supabase is paused vs just empty
- Shows dashboard link with clear unpause instructions
- Auto-syncs PRDs once database is accessible
- Integrated into startup prompt Step 4.0.1
- Dynamic PRD count (not hardcoded)

Benefits:
- Handles frequent Supabase pauses gracefully
- Clear user guidance when manual action needed
- Automatic recovery after unpause
- Future-proof for any number of PRDs

Refs: docs/resolution-summaries/2025-11-27-startup-prompt-prd-sync-enhancement.md
"

# 4. Push
git push origin main
```

**Phase 6: Session Closure**

```bash
# 1. Final verification
git log -1  # Verify commit
curl -k https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds | jq .total
# Result: 8 PRDs ✅

# 2. Clean up
rm -f /tmp/*.json  # Remove temp files

# 3. Session summary
# "Implemented smart Supabase pause detection
#  - Created check script with auto-sync
#  - Updated startup prompt
#  - Documentation complete
#  - 8 PRDs restored and verified
#  All changes committed and pushed ✅"
```

---

## 📁 File Locations

**Startup Prompt**: `.cursor/startup-prompt.md`
**Linting System**: `.cursor/LINTING_SYSTEM.md`
**Workflow**: `docs/guides/AI_AGENT_WORKFLOW.md` (this file)
**Quick Reference**: `.cursor/QUICK_REFERENCE.md`
**Documentation Checklist**: `docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md` ⭐ NEW
**Resolution Summaries**: `docs/resolution-summaries/`
**Resolution Summary Creator**: `scripts/dev/create-resolution-summary.sh` (helper script)
**Linting Tools Checker**: `scripts/dev/check-linting-tools.sh`
**Linting Scripts**: `scripts/dev/lint-*.sh` (to be created)
**CHANGELOG**: `CHANGELOG.md`

---

## 🔄 Continuous Improvement

This workflow is **living documentation**. If you find:

- Steps that could be automated
- Process improvements
- Missing safeguards
- Better practices

→ Update this document and discuss with the team

---

## 💡 Philosophy

**Why this matters**:

1. **Consistency**: Every session follows the same high-quality process
2. **Knowledge Preservation**: Documentation ensures nothing is lost
3. **Quality**: Linting and testing catch issues early
4. **Collaboration**: Clear commit history helps everyone
5. **Speed**: Structured process is faster than ad-hoc

**The goal**: Make doing the right thing the easy thing

---

**Remember**: This workflow exists to **help**, not hinder. If something doesn't make sense, ask questions and improve the process.

---

**Last Updated**: November 27, 2025
**Status**: ✅ Active - Use for all AI agent sessions
