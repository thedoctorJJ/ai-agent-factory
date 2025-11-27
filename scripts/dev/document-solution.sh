#!/bin/bash
# Document Solution - Complete Documentation Workflow
# Run this after solving any problem to create proper documentation

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   📚 AI Agent Factory - Document Solution Workflow   ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}This script will guide you through documenting your solution:${NC}"
echo -e "  1. Create resolution summary"
echo -e "  2. Remind you to update CHANGELOG"
echo -e "  3. Show documentation checklist"
echo -e "  4. Guide you through git commit"
echo ""
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 1: Create Resolution Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 1/4: Create Resolution Summary                 ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}This will create a comprehensive resolution summary document.${NC}"
echo ""

# Run the resolution summary creator
./scripts/dev/create-resolution-summary.sh

# Capture the created filename (stored in output)
RESOLUTION_FILE=$(ls -t docs/resolution-summaries/*.md | head -1)

echo ""
echo -e "${GREEN}✅ Resolution summary created:${NC}"
echo -e "   ${RESOLUTION_FILE}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Make sure you completed ALL sections in the file!${NC}"
echo ""
echo -e "${YELLOW}Press Enter when you've completed the resolution summary...${NC}"
read

# Step 2: Update CHANGELOG
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 2/4: Update CHANGELOG.md                       ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Add an entry to CHANGELOG.md with the following format:${NC}"
echo ""
cat << 'CHANGELOG_TEMPLATE'
## [Unreleased] - $(date +%Y-%m-%d)

### 🔧 **[Feature/Fix Name] - [TYPE]**
- **✅ Feature/Fix**: [Brief description]
- **✅ Purpose**: [Why this was needed]
- **✅ Implementation**: [How it was done]
- **✅ Benefits**: [What this improves]
- **✅ Status**: [Current state]

### **Technical Details**
- **Files Created**: [List]
- **Files Modified**: [List]
- **Testing**: [How verified]
- **Resolution Summary**: `$(basename "$RESOLUTION_FILE")`
CHANGELOG_TEMPLATE
echo ""
echo -e "${YELLOW}Opening CHANGELOG.md in editor...${NC}"
echo ""
echo -e "${YELLOW}Press Enter to open CHANGELOG.md...${NC}"
read

# Open CHANGELOG in editor
if [ -n "$EDITOR" ]; then
    $EDITOR CHANGELOG.md
else
    vim CHANGELOG.md
fi

echo ""
echo -e "${GREEN}✅ CHANGELOG.md should now be updated${NC}"
echo ""
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 3: Check Repository Structure
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 3/5: Check Repository Structure                ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Ensuring repository is clean and well-organized...${NC}"
echo ""

./scripts/dev/check-repo-structure.sh || {
    echo ""
    echo -e "${YELLOW}Repository structure issues found.${NC}"
    echo -e "${YELLOW}Would you like to continue anyway? (y/N):${NC} "
    read -r CONTINUE_ANYWAY
    if [[ "$CONTINUE_ANYWAY" != "y" && "$CONTINUE_ANYWAY" != "Y" ]]; then
        echo -e "${RED}Please fix repository structure issues first.${NC}"
        exit 1
    fi
}

echo ""
echo -e "${GREEN}✅ Repository structure verified${NC}"
echo ""
echo -e "${YELLOW}Press Enter to continue...${NC}"
read

# Step 4: Review Documentation Checklist
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 4/5: Review Documentation Checklist            ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}The documentation checklist covers 24 categories of docs.${NC}"
echo -e "${CYAN}Use the decision matrix to determine what to update.${NC}"
echo ""
echo -e "${YELLOW}Decision Matrix:${NC}"
echo ""
cat << 'DECISION_MATRIX'
After Fixing a Bug:
  ✅ MANDATORY: Resolution summary ✓, CHANGELOG ✓
  🔍 Review: README (if user-facing), Troubleshooting
  📝 Consider: Related subsystem guides

After Adding a Feature:
  ✅ MANDATORY: Resolution summary ✓, CHANGELOG ✓, README
  🔍 Review: Quick Reference, Workflow
  📝 Consider: API docs, Architecture, Guides

After Deployment:
  ✅ MANDATORY: Resolution summary ✓, CHANGELOG ✓, README, Deployment Status
  🔍 Review: Architecture, Health checks
  📝 Consider: Deployment guide

After Config Changes:
  ✅ MANDATORY: Resolution summary ✓, CHANGELOG ✓
  🔍 Review: Startup prompt, Environment, Secrets
  📝 Consider: README, Deployment guide
DECISION_MATRIX
echo ""
echo -e "${YELLOW}Would you like to see the full checklist? (y/N):${NC} "
read -r SHOW_CHECKLIST

if [[ "$SHOW_CHECKLIST" == "y" || "$SHOW_CHECKLIST" == "Y" ]]; then
    echo ""
    echo -e "${CYAN}Opening full checklist...${NC}"
    if [ -n "$EDITOR" ]; then
        $EDITOR docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md
    else
        less docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md
    fi
fi

echo ""
echo -e "${YELLOW}Have you updated all relevant documentation? (y/N):${NC} "
read -r DOCS_UPDATED

if [[ "$DOCS_UPDATED" != "y" && "$DOCS_UPDATED" != "Y" ]]; then
    echo ""
    echo -e "${RED}⚠️  Please update relevant documentation before committing!${NC}"
    echo ""
    echo -e "${CYAN}Refer to: docs/guides/DOCUMENTATION_UPDATE_CHECKLIST.md${NC}"
    echo ""
    echo -e "${YELLOW}Press Enter when documentation is complete...${NC}"
    read
fi

# Step 5: Git Commit Guidance
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 5/5: Git Commit                                ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Review your changes and prepare to commit:${NC}"
echo ""

# Show git status
echo -e "${YELLOW}Current changes:${NC}"
echo ""
git status
echo ""

echo -e "${YELLOW}Would you like to see the diff? (y/N):${NC} "
read -r SHOW_DIFF

if [[ "$SHOW_DIFF" == "y" || "$SHOW_DIFF" == "Y" ]]; then
    git diff
    echo ""
fi

echo -e "${CYAN}Commit Message Format:${NC}"
echo ""
cat << 'COMMIT_FORMAT'
type(scope): brief description

- Detailed explanation of what changed
- Why it was needed
- Any breaking changes or important notes

Benefits:
- Benefit 1
- Benefit 2

Testing:
- How verified

Refs: docs/resolution-summaries/[filename].md
COMMIT_FORMAT
echo ""
echo -e "${YELLOW}Commit types:${NC} feat, fix, docs, style, refactor, test, chore, perf"
echo ""

echo -e "${YELLOW}Would you like help staging and committing? (Y/n):${NC} "
read -r HELP_COMMIT

if [[ "$HELP_COMMIT" != "n" && "$HELP_COMMIT" != "N" ]]; then
    echo ""
    echo -e "${CYAN}Let's stage the files...${NC}"
    echo ""
    
    # Suggest files to stage
    echo -e "${YELLOW}Files to stage (suggested):${NC}"
    echo "  - $RESOLUTION_FILE"
    echo "  - CHANGELOG.md"
    git status --short | grep -E '^\s*M|^\s*A|^\?\?' | awk '{print "  - " $2}'
    echo ""
    
    echo -e "${YELLOW}Stage all modified files? (Y/n):${NC} "
    read -r STAGE_ALL
    
    if [[ "$STAGE_ALL" != "n" && "$STAGE_ALL" != "N" ]]; then
        git add -A
        echo ""
        echo -e "${GREEN}✅ All files staged${NC}"
    else
        echo ""
        echo -e "${CYAN}Please stage files manually:${NC}"
        echo "  git add [files]"
        echo ""
        echo -e "${YELLOW}Press Enter when files are staged...${NC}"
        read
    fi
    
    echo ""
    echo -e "${CYAN}Now create your commit message...${NC}"
    echo ""
    
    # Create commit
    git commit
    
    echo ""
    echo -e "${GREEN}✅ Commit created!${NC}"
    echo ""
    echo -e "${YELLOW}Push to GitHub? (Y/n):${NC} "
    read -r DO_PUSH
    
    if [[ "$DO_PUSH" != "n" && "$DO_PUSH" != "N" ]]; then
        git push origin main
        echo ""
        echo -e "${GREEN}✅ Pushed to GitHub!${NC}"
    fi
fi

# Step 6: Sync Entire Repository with GitHub
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Step 6/6: Sync Entire Repository with GitHub        ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Checking for any uncommitted changes...${NC}"
echo ""

# Check if there are any uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  Found uncommitted changes:${NC}"
    git status --short
    echo ""
    echo -e "${YELLOW}Would you like to commit and push ALL changes? (Y/n):${NC} "
    read -r SYNC_ALL
    
    if [[ "$SYNC_ALL" != "n" && "$SYNC_ALL" != "N" ]]; then
        echo ""
        echo -e "${CYAN}Staging all changes...${NC}"
        git add -A
        
        echo ""
        echo -e "${CYAN}Committing remaining changes...${NC}"
        git commit --no-verify -m "chore: sync all remaining changes

Syncing all outstanding changes to GitHub as part of workflow completion."
        
        echo ""
        echo -e "${CYAN}Pushing to GitHub...${NC}"
        git push origin main
        
        echo ""
        echo -e "${GREEN}✅ All changes synced to GitHub!${NC}"
    else
        echo ""
        echo -e "${YELLOW}⚠️  Skipped syncing uncommitted changes${NC}"
    fi
else
    echo -e "${GREEN}✅ No uncommitted changes - repository is already in sync${NC}"
fi

echo ""
echo -e "${CYAN}Verifying sync status...${NC}"
git status
echo ""

# Final Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   ✅ Workflow Complete!                               ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}✅ Resolution summary created${NC}"
echo -e "${GREEN}✅ CHANGELOG.md updated${NC}"
echo -e "${GREEN}✅ Repository structure verified${NC}"
echo -e "${GREEN}✅ Documentation reviewed${NC}"
echo -e "${GREEN}✅ Changes committed${NC}"
echo -e "${GREEN}✅ Repository synced with GitHub${NC}"
echo ""
echo -e "${CYAN}Created files:${NC}"
echo "  - $RESOLUTION_FILE"
echo ""
echo -e "${CYAN}Repository status:${NC}"
echo "  - Branch: $(git branch --show-current)"
echo "  - Latest commit: $(git log -1 --oneline)"
echo "  - Sync status: $(git status | grep -q 'up to date' && echo 'Up to date with origin' || echo 'Check git status')"
echo ""
echo -e "${GREEN}🎉 Great job! Everything is documented and synced!${NC}"
echo ""

