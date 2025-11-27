# Setup ChatGPT Actions - Quick Start Guide

## 🎯 What You're Setting Up

ChatGPT Actions will automatically detect PRDs in your voice conversations and submit them to the AI Agent Factory - no manual steps needed!

## ✅ Pre-Flight Check

### 1. Verify API Endpoint

The endpoint is ready at:
```
https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
```

### 2. Get the OpenAPI Schema

The schema file is ready at: `api-spec/chatgpt-action-openapi.json`

## 📋 Setup Steps (5 minutes)

### Step 1: Enable Actions in ChatGPT

1. Go to **chat.openai.com**
2. Click your **profile icon** (bottom left)
3. **Settings** → **Beta features**
4. Enable **"Actions"** ✅
5. Click **"Save"**

### Step 2: Create the Action

1. In ChatGPT settings, go to **"Actions"** tab
2. Click **"Create new action"**
3. **Name**: `AI Agent Factory PRD Submission`
4. **Description**: `Automatically submit PRDs to AI Agent Factory`

### Step 3: Add the Schema

1. Open: `api-spec/chatgpt-action-openapi.json`
2. **Copy the entire JSON** (all 78 lines)
3. In ChatGPT, paste into **"Schema"** field
4. Click **"Validate"** ✅

### Step 4: Add Instructions

Paste this into **"Instructions"** field:

```
When the user creates, describes, or asks you to create a Product Requirements Document (PRD), you should:

1. Format the PRD content as markdown following this structure:
   - Title
   - Description
   - Requirements (list)
   - Technical Requirements
   - Success Metrics
   - Timeline (if provided)

2. Automatically call the submitPRD action with the formatted PRD content

3. Confirm to the user that the PRD has been submitted and provide the PRD ID

4. If the user is just discussing ideas (not creating a PRD), do NOT call the action

The PRD should be complete and well-structured before submission.
```

### Step 5: Save and Test

1. Click **"Save"**
2. **Test**: Say to ChatGPT (voice or text):
   ```
   Create a PRD for a user authentication system
   ```
3. ChatGPT should automatically submit it! ✅

## 🎤 How It Works

**You (voice)**: "Create a PRD for a caching system"

**ChatGPT**:
1. Creates PRD
2. Formats as markdown
3. **Calls submitPRD action automatically**
4. Confirms: "✅ PRD submitted! ID: abc123..."

## 📁 Files You Need

- **Schema**: `api-spec/chatgpt-action-openapi.json` (copy this)
- **Instructions**: See Step 4 above (copy this)

## ✅ Verification

After setup, test with:
- **Voice**: "Create a PRD for [any feature]"
- **Expected**: ChatGPT automatically submits it
- **Check**: PRD appears in your dashboard

---

**Ready?** Follow the 5 steps above and you're done! 🚀



