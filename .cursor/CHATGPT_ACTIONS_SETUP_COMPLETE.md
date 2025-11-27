# ChatGPT Actions Setup - Complete Guide

## 🎯 Goal

Set up ChatGPT Actions so ChatGPT automatically detects and submits PRDs from voice conversations to the AI Agent Factory.

## ✅ Pre-Setup Checklist

### 1. Verify API Endpoint is Working

**Endpoint**: `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming`

**Test Command**:
```bash
curl -X POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/json" \
  -d '{"content": "# Test PRD\n\n## Description\nTest PRD"}'
```

**Expected Response**: `200 OK` with PRD data

### 2. Get OpenAPI Schema

The schema is located at: `api-spec/chatgpt-action-openapi.json`

**View it**:
```bash
cat api-spec/chatgpt-action-openapi.json
```

## 📋 Step-by-Step Setup in ChatGPT

### Step 1: Enable Actions

1. Open **ChatGPT** (chat.openai.com)
2. Click your **profile icon** (bottom left)
3. Go to **Settings** → **Beta features**
4. Enable **"Actions"** (toggle it on)
5. Click **"Save"**

### Step 2: Create New Action

1. In ChatGPT settings, go to **"Actions"** tab
2. Click **"Create new action"** button
3. Fill in:
   - **Name**: `AI Agent Factory PRD Submission`
   - **Description**: `Automatically submit Product Requirements Documents (PRDs) to the AI Agent Factory platform`

### Step 3: Add OpenAPI Schema

1. Open the file: `api-spec/chatgpt-action-openapi.json`
2. **Copy the entire JSON content**
3. In ChatGPT Actions, paste it into the **"Schema"** field
4. Click **"Validate"** to ensure it's correct

**Schema Location**: `api-spec/chatgpt-action-openapi.json`

### Step 4: Add Instructions

Paste this into the **"Instructions"** field in ChatGPT:

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

### Step 5: Configure Authentication (Optional)

- **Type**: None (the endpoint is public)
- Or add API key authentication if you want to secure it later

### Step 6: Save and Test

1. Click **"Save"** to save the action
2. **Test it** by saying to ChatGPT (voice or text):
   ```
   Create a PRD for a user authentication system
   ```
3. ChatGPT should:
   - Create the PRD
   - Format it as markdown
   - **Automatically call the submitPRD action**
   - Confirm: "✅ PRD submitted! ID: abc123..."

## 🎤 How It Works

### Voice Conversation Example

**You (voice)**: "I want to create a PRD for a caching system"

**ChatGPT**:
1. Creates the PRD
2. Formats it as markdown
3. **Automatically calls submitPRD action**
4. Says: "✅ PRD submitted! ID: abc123..."

**No manual steps needed!**

## 🔧 Troubleshooting

### Action Not Being Called

1. **Check Actions are enabled**: Settings → Beta features → Actions
2. **Verify schema is correct**: Use the schema from `api-spec/chatgpt-action-openapi.json`
3. **Check instructions**: Make sure instructions are clear about when to call the action
4. **Be explicit**: Say "Create a PRD for..." instead of just describing features

### API Errors

1. **Test endpoint manually**: Use the curl command above
2. **Check endpoint URL**: Should be `https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming`
3. **Verify PRD format**: Must be valid markdown

### PRD Not Submitting

1. Check ChatGPT's action logs (if available)
2. Verify the endpoint is accessible
3. Ensure PRD content is properly formatted

## 📚 Files Reference

- **OpenAPI Schema**: `api-spec/chatgpt-action-openapi.json`
- **Setup Guide**: `.cursor/CHATGPT_ACTION_SETUP.md`
- **MCP Tools Guide**: `.cursor/MCP_CHATGPT_ACTIONS.md`

## ✅ Verification

After setup, test with:

**Voice**: "Create a PRD for a user authentication system"

**Expected Result**:
- ChatGPT creates PRD
- Automatically submits via API
- Confirms with PRD ID
- PRD appears in your dashboard

---

**Status**: Ready to configure! Follow the steps above to set up ChatGPT Actions.



