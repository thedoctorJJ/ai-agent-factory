# Mobile ChatGPT - GitHub Direct File Creation Instructions

**Date**: November 28, 2025  
**Purpose**: Instructions for mobile ChatGPT to create PRD files directly in GitHub repository  
**Status**: ✅ **READY FOR TESTING**

---

## 🎯 Overview

Mobile ChatGPT can create PRD files directly in the GitHub repository. PRDs should be created in the `prds/queue/` directory, which is the cloud source of truth.

---

## 📍 GitHub Repository Location

**Repository**: `thedoctorJJ/ai-agent-factory`  
**Branch**: `main`  
**Directory**: `prds/queue/`  
**Full Path**: `https://github.com/thedoctorJJ/ai-agent-factory/tree/main/prds/queue`

---

## 📋 Instructions for Mobile ChatGPT

### **System Prompt / Custom Instructions**

```
You are an expert PRD (Product Requirements Document) creator for the AI Agent Factory platform.

When creating PRDs, you MUST create the PRD file directly in the GitHub repository at this location:

Repository: thedoctorJJ/ai-agent-factory
Branch: main
Directory: prds/queue/
Full Path: https://github.com/thedoctorJJ/ai-agent-factory/tree/main/prds/queue

FILE CREATION RULES:
1. Create PRD files directly in: prds/queue/
2. File naming format: YYYY-MM-DD_prd-title.md
   - Use today's date in YYYY-MM-DD format
   - Convert PRD title to lowercase with hyphens
   - Example: 2025-11-28_user-authentication-system.md
3. File must be in Markdown format (.md extension)
4. PRD content must follow the standard template (see below)

PRD TEMPLATE STRUCTURE (Minimum Required):
- Title (required)
- Description (required)
- Requirements (required - list format)

PRD TEMPLATE STRUCTURE (Recommended - Complete):
- Title
- Description
- Problem Statement
- Target Users
- User Stories
- Requirements
- Acceptance Criteria
- Technical Requirements
- Success Metrics
- Timeline
- Dependencies
- Risks
- Assumptions

PRD TYPES:
- "agent" - For creating AI agents (creates separate GitHub repository)
- "platform" - For platform features and infrastructure (added to main repo)

WORKFLOW:
1. User requests a PRD creation
2. Create comprehensive PRD following template
3. Show PRD content to user for review
4. Create file directly in GitHub at: prds/queue/YYYY-MM-DD_prd-title.md
5. Confirm file creation with GitHub URL

IMPORTANT:
- Always create files in prds/queue/ directory
- Use proper file naming: YYYY-MM-DD_prd-title.md
- Files created here are automatically synced to database via GitHub Actions
- GitHub is the cloud source of truth - files here persist forever
- Do NOT ask for file locations - always use prds/queue/

If you cannot create files directly in GitHub, provide the PRD content in markdown format and inform the user to save it manually.
```

---

## 🧪 Test Prompt for Mobile ChatGPT

Use this prompt to test mobile ChatGPT's GitHub file creation:

```
Create a PRD for a mobile app notification system and save it directly to the GitHub repository at:

Repository: thedoctorJJ/ai-agent-factory
Path: prds/queue/
File name: Use today's date and format as YYYY-MM-DD_mobile-app-notification-system.md

The PRD should include:
- Title: Mobile App Notification System
- Description: A comprehensive push notification system for mobile applications
- Requirements: List of functional requirements
- Technical Requirements: Backend, mobile SDK, notification service
- Success Metrics: Delivery rate, engagement metrics

Create the file directly in GitHub at prds/queue/ directory.
```

---

## ✅ Expected Behavior

When mobile ChatGPT successfully creates a PRD file:

1. **File Created**: PRD file appears in `prds/queue/` directory
2. **GitHub URL**: ChatGPT provides link to the created file
3. **Automatic Sync**: GitHub Actions automatically syncs to database (within 30 seconds)
4. **Website Update**: PRD appears on website immediately after sync

**Example Response**:
```
✅ PRD created successfully!

File: prds/queue/2025-11-28_mobile-app-notification-system.md
GitHub URL: https://github.com/thedoctorJJ/ai-agent-factory/blob/main/prds/queue/2025-11-28_mobile-app-notification-system.md

The PRD has been committed to GitHub and will be automatically synced to the database within 30 seconds.
```

---

## 🔍 Verification Steps

After mobile ChatGPT creates a PRD:

1. **Check GitHub**:
   - Visit: https://github.com/thedoctorJJ/ai-agent-factory/tree/main/prds/queue
   - Verify new PRD file appears

2. **Check Database** (after 30 seconds):
   ```bash
   curl -s https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds | jq '.total'
   ```

3. **Check Website**:
   - Visit: https://ai-agent-factory-frontend-952475323593.us-central1.run.app
   - PRD should appear in PRD Repository

---

## 📝 File Naming Examples

**Correct Format**:
- `2025-11-28_mobile-app-notification-system.md`
- `2025-11-28_user-authentication-system.md`
- `2025-11-28_api-rate-limiting.md`

**Incorrect Format** (avoid):
- `mobile-app-notification-system.md` (missing date)
- `2025-11-28 Mobile App Notification System.md` (spaces in filename)
- `mobile_app_notification_system.md` (underscores instead of hyphens)

---

## 🎯 Key Points for Mobile ChatGPT

1. **Always use**: `prds/queue/` directory
2. **File format**: `YYYY-MM-DD_prd-title.md`
3. **Date format**: Use today's date in YYYY-MM-DD format
4. **Title format**: Convert to lowercase with hyphens
5. **Content**: Must be valid Markdown following PRD template

---

## 🔗 Related Documentation

- **GitHub Repository**: https://github.com/thedoctorJJ/ai-agent-factory
- **PRD Queue Folder**: https://github.com/thedoctorJJ/ai-agent-factory/tree/main/prds/queue
- **PRD Templates**: `prds/templates/` directory
- **Workflow Guide**: `docs/guides/CHATGPT_PRD_WORKFLOW.md`

---

## 🚨 Troubleshooting

### **Problem: ChatGPT can't create files in GitHub**

**Solution**: Provide PRD content in markdown format and ask user to:
1. Go to GitHub repository
2. Navigate to `prds/queue/` directory
3. Click "Add file" → "Create new file"
4. Paste PRD content
5. Name file: `YYYY-MM-DD_prd-title.md`
6. Commit directly to main branch

### **Problem: File created in wrong location**

**Solution**: 
- Verify file is in `prds/queue/` directory
- If in wrong location, move file to `prds/queue/`
- Commit the move to GitHub

### **Problem: File not syncing to database**

**Solution**:
- Wait 30 seconds for GitHub Actions to trigger
- Check GitHub Actions: https://github.com/thedoctorJJ/ai-agent-factory/actions
- Manually trigger sync if needed

---

**Last Updated**: November 28, 2025  
**Status**: ✅ Ready for mobile ChatGPT testing

