# ChatGPT Action Setup - Auto-Detect and Submit PRDs

This guide shows you how to set up ChatGPT Actions so ChatGPT automatically detects PRDs in your voice conversations and submits them to the AI Agent Factory.

## 🎯 What This Does

When you're talking to ChatGPT (via voice or text), if ChatGPT detects that you're creating a PRD, it will **automatically submit it** to the AI Agent Factory using the action endpoint. No need to specify locations or endpoints!

## 📋 Setup Steps

### Step 1: Create a ChatGPT Action

1. **Open ChatGPT** → Click your profile → **Settings** → **Beta features**
2. Enable **"Actions"** (if not already enabled)
3. Go to **"Actions"** in your ChatGPT settings
4. Click **"Create new action"**

### Step 2: Configure the Action

**Action Name**: `AI Agent Factory PRD Submission`

**Description**: 
```
Automatically submit Product Requirements Documents (PRDs) to the AI Agent Factory platform. When the user creates or describes a PRD in conversation, this action will automatically format and submit it.
```

**Authentication**: 
- **Type**: None (or API Key if you want to add authentication later)
- The endpoint is public and doesn't require authentication

**Schema**: 
- Use the OpenAPI schema from `api-spec/chatgpt-action-openapi.json`
- Or paste the schema directly (see below)

### Step 3: Add the OpenAPI Schema

Copy the contents of `api-spec/chatgpt-action-openapi.json` and paste it into the schema field, OR use this simplified version:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "AI Agent Factory PRD Submission",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    }
  ],
  "paths": {
    "/api/v1/prds/incoming": {
      "post": {
        "operationId": "submitPRD",
        "summary": "Submit a Product Requirements Document",
        "description": "Submit a PRD to the AI Agent Factory. Call this when the user creates or describes a PRD.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "content": {
                    "type": "string",
                    "description": "Complete PRD content in markdown format"
                  }
                },
                "required": ["content"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "PRD submitted successfully"
          }
        }
      }
    }
  }
}
```

### Step 4: Add Instructions

In the **Instructions** field, add:

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

1. **Save** the action
2. **Test it** by saying to ChatGPT: "Create a PRD for a user authentication system"
3. ChatGPT should automatically:
   - Create the PRD
   - Format it as markdown
   - Call the action to submit it
   - Confirm submission with PRD ID

## ✅ How It Works

### Automatic Detection

ChatGPT will automatically detect when you're creating a PRD based on:
- Keywords: "PRD", "product requirements", "requirements document"
- Context: Creating specifications, requirements, features
- Structure: Lists of requirements, technical specs, etc.

### Example Conversations

**You (voice)**: "I want to create a PRD for a user authentication system"

**ChatGPT**: 
- Creates the PRD
- Formats it
- **Automatically calls submitPRD action**
- Says: "✅ PRD submitted! ID: abc123..."

**You (voice)**: "What are the requirements for a caching system?"

**ChatGPT**: 
- Creates the PRD
- **Automatically submits it**
- Confirms submission

## 🎯 Benefits

- ✅ **Works with voice** - No typing needed
- ✅ **Automatic detection** - ChatGPT knows when to submit
- ✅ **No location needed** - Endpoint is pre-configured
- ✅ **Seamless** - Just talk, PRDs get submitted automatically

## 🔧 Troubleshooting

### Action Not Being Called

1. Check that Actions are enabled in ChatGPT settings
2. Verify the schema is correctly formatted
3. Make sure you're explicitly creating a PRD (not just discussing ideas)
4. Try saying: "Create a PRD for..." instead of just describing features

### PRD Not Submitting

1. Check the API endpoint is accessible
2. Verify the PRD content is properly formatted
3. Check ChatGPT's action logs for errors

## 📚 Related Files

- `api-spec/chatgpt-action-openapi.json` - Complete OpenAPI schema
- `docs/guides/INCOMING_PRD_WORKFLOW.md` - API documentation
- `.cursor/CHATGPT_CUSTOM_INSTRUCTIONS.md` - Alternative setup method

---

**Status**: ✅ Ready to configure in ChatGPT!



