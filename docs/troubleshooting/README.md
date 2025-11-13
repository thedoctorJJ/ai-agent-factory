# Troubleshooting Guide

This directory contains documentation for bugs, issues, and their resolutions in the AI Agent Factory platform.

## 📋 Available Documentation

### Production Issues

- **[Agents Endpoint Internal Server Error](./agents-endpoint-internal-server-error.md)** (2025-11-13)
  - Fixed 500 error on `/api/v1/agents` endpoint
  - Root cause: Missing datetime conversion and enum validation

## 🔍 How to Use This Directory

1. **For Known Issues**: Check the list above to see if your issue has been documented
2. **For New Issues**: Create a new markdown file following the template below
3. **For Resolved Issues**: Update the status to "✅ Fixed" and add resolution details

## 📝 Issue Documentation Template

When documenting a new issue, use this structure:

```markdown
# [Issue Title] - [Status]

**Date**: [Date]  
**Status**: [Open/Fixed/In Progress]  
**Severity**: [Low/Medium/High/Critical]  
**Affected Service**: [Service Name]

## Summary
Brief description of the issue

## Problem Description
Detailed symptoms and root cause

## Solution
How the issue was resolved

## Testing
How to verify the fix

## Related Files
List of files modified

## Timeline
Key dates and milestones
```

## 🔗 Related Documentation

- **Deployment Issues**: See `docs/deployment/`
- **Setup Issues**: See `docs/getting-started/`
- **Architecture**: See `docs/architecture/`
- **Changelog**: See `CHANGELOG.md` in repository root

