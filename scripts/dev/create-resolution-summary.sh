#!/bin/bash
# Create Resolution Summary Document
# Interactive script to help create properly formatted resolution summaries

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📝 Resolution Summary Creator${NC}"
echo "=================================="
echo ""

# Get current date
CURRENT_DATE=$(date +%Y-%m-%d)

# Prompt for issue name
echo -e "${YELLOW}What issue did you solve?${NC}"
echo -e "${BLUE}(Use kebab-case, e.g., 'agents-endpoint-500-error')${NC}"
read -p "Issue name: " ISSUE_NAME

if [ -z "$ISSUE_NAME" ]; then
    echo -e "${RED}❌ Issue name is required${NC}"
    exit 1
fi

# Generate filename
FILENAME="docs/resolution-summaries/${ISSUE_NAME}-resolution-${CURRENT_DATE}.md"

# Check if file already exists
if [ -f "$FILENAME" ]; then
    echo -e "${YELLOW}⚠️  File already exists: $FILENAME${NC}"
    read -p "Overwrite? (y/N): " OVERWRITE
    if [ "$OVERWRITE" != "y" ]; then
        echo -e "${RED}Cancelled${NC}"
        exit 1
    fi
fi

# Prompt for basic information
echo ""
echo -e "${YELLOW}Brief description of the issue:${NC}"
read -p "Issue: " ISSUE_DESC

echo ""
echo -e "${YELLOW}Was this a bug fix, feature, or enhancement?${NC}"
read -p "Type (bug/feature/enhancement): " ISSUE_TYPE

echo ""
echo -e "${YELLOW}Current status:${NC}"
read -p "Status (RESOLVED/IN_PROGRESS/DEPLOYED): " STATUS

echo ""
echo -e "${YELLOW}How long did it take to resolve?${NC}"
read -p "Resolution time (e.g., '2 hours', 'Same day'): " RESOLUTION_TIME

# Create the template
cat > "$FILENAME" << 'TEMPLATE_END'
# [ISSUE_NAME_TITLE] Resolution Summary

**Date**: [CURRENT_DATE]  
**Issue**: [ISSUE_DESC]  
**Status**: ✅ **[STATUS]** - [Brief status description]  
**Resolution Time**: [RESOLUTION_TIME]

---

## 📋 Executive Summary

[High-level overview of the issue and resolution - 2-3 paragraphs]

The issue was [describe problem]. Investigation revealed [root cause]. The solution implemented was [describe fix], which resulted in [outcome].

---

## 🔍 Issue Discovery

### Initial Symptoms

1. **How discovered**: [How the issue was first noticed]
2. **User impact**: [How it affected users/development]
3. **Error messages**: [Any error messages or symptoms]

### Investigation Steps

1. [Step 1 - what you checked]
2. [Step 2 - what you tested]
3. [Step 3 - what you discovered]

---

## 🐛 Root Cause Analysis

### Problem Identified

[Detailed explanation of the root cause]

**Primary Issues**:
1. **[Issue 1]**: [Description]
2. **[Issue 2]**: [Description]

### Code Location

**File**: `[file/path.py]`  
**Method/Function**: `[function_name]` (lines XX-YY)

**Why It Failed**:
- [Reason 1]
- [Reason 2]

---

## ✅ Solution Implementation

### Fix Applied

**Files Modified**: [List files changed]

#### 1. [Change 1 Title]

**What changed**:
```[language]
[Code snippet or description]
```

**Why this works**: [Explanation]

#### 2. [Change 2 Title]

**What changed**: [Description]

**Why this works**: [Explanation]

---

## 🧪 Testing

### Test Execution

**1. [Test 1 Name]**:
```bash
[Test command]
# Result: [Expected outcome]
```

**2. [Test 2 Name]**:
```bash
[Test command]
# Result: [Expected outcome]
```

### Test Results
- ✅ [Test 1] - PASSED
- ✅ [Test 2] - PASSED
- ✅ [Test 3] - PASSED

---

## 🚀 Deployment (if applicable)

### Deployment Process

1. **[Step 1]**: [What was deployed]
2. **[Step 2]**: [Verification performed]

### Deployment Details
- **Service**: [Service name]
- **Region**: [Deployment region]
- **Revision**: [Revision number/ID]
- **Status**: [Deployment status]

---

## 📊 Impact Analysis

### Before Fix
- ❌ [Problem 1]
- ❌ [Problem 2]
- ❌ [Problem 3]

### After Fix
- ✅ [Improvement 1]
- ✅ [Improvement 2]
- ✅ [Improvement 3]

---

## 📚 Documentation

### Files Created
- [List new documentation files]

### Files Modified
- [List updated files]

### Documentation Updated
- `CHANGELOG.md` - [What was added]
- [Other docs updated]

---

## 📝 Lessons Learned

### Technical Lessons

1. **[Lesson 1]**: [What you learned technically]
2. **[Lesson 2]**: [Technical insight]

### Process Lessons

1. **[Lesson 1]**: [Process improvement]
2. **[Lesson 2]**: [Workflow insight]

---

## 🔗 Related Files

### Modified Files
- [List with brief description of changes]

### Created Files
- [List with purpose]

### Related Documentation
- [Link to related docs]

---

## ✅ Verification Checklist

- [ ] Issue identified and root cause determined
- [ ] Fix implemented in code
- [ ] Testing completed and passed
- [ ] Fix deployed to production (if applicable)
- [ ] Production verified working (if applicable)
- [ ] Documentation created/updated
- [ ] CHANGELOG updated
- [ ] Code committed to repository
- [ ] Changes pushed to GitHub
- [ ] Resolution summary created (this document)

---

## 🎯 Conclusion

[2-3 sentences summarizing the resolution and final status]

✅ **Status**: [RESOLVED/DEPLOYED/VERIFIED]

---

**Resolved By**: AI Assistant  
**Reviewed By**: [Pending/Name]  
**Deployed**: [Date or N/A]  
**Verified**: [Date or N/A]
TEMPLATE_END

# Replace placeholders
sed -i '' "s/\[ISSUE_NAME_TITLE\]/${ISSUE_NAME^}/g" "$FILENAME"
sed -i '' "s/\[CURRENT_DATE\]/$CURRENT_DATE/g" "$FILENAME"
sed -i '' "s/\[ISSUE_DESC\]/$ISSUE_DESC/g" "$FILENAME"
sed -i '' "s/\[STATUS\]/$STATUS/g" "$FILENAME"
sed -i '' "s/\[RESOLUTION_TIME\]/$RESOLUTION_TIME/g" "$FILENAME"

echo ""
echo -e "${GREEN}✅ Resolution summary template created:${NC}"
echo "   $FILENAME"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "   1. Open the file and complete all sections"
echo "   2. Replace all [placeholders] with actual content"
echo "   3. Add code snippets, test results, and details"
echo "   4. Review and verify all sections are complete"
echo "   5. Add to git: git add $FILENAME"
echo ""
echo -e "${BLUE}💡 Template sections to complete:${NC}"
echo "   - Executive Summary (fill in 2-3 paragraphs)"
echo "   - Issue Discovery (how you found it)"
echo "   - Root Cause Analysis (why it happened)"
echo "   - Solution Implementation (what you fixed)"
echo "   - Testing (how you verified)"
echo "   - Deployment (if applicable)"
echo "   - Impact Analysis (before/after)"
echo "   - Lessons Learned (takeaways)"
echo "   - Related Files (list all changed files)"
echo "   - Verification Checklist (check off items)"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to:${NC}"
echo "   - Update CHANGELOG.md"
echo "   - Commit with meaningful message"
echo "   - Reference this file in commit message"
echo ""

# Open in editor if EDITOR is set
if [ -n "$EDITOR" ]; then
    echo -e "${BLUE}Opening in editor...${NC}"
    $EDITOR "$FILENAME"
fi

