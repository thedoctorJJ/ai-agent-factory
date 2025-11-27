# ChatGPT Custom Instructions for AI Agent Factory

If you don't want to create a custom GPT, you can add these instructions to your ChatGPT profile's "Custom Instructions" section.

## 📋 How to Add Custom Instructions

1. Click your profile icon in ChatGPT
2. Go to "Settings" → "Personalization" → "Custom Instructions"
3. Paste the instructions below into the "How would you like ChatGPT to respond?" section

## 📝 Custom Instructions

```
When creating Product Requirements Documents (PRDs), always submit them directly to the AI Agent Factory cloud API using this endpoint:

POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

Request format:
{
  "content": "[PRD markdown content]"
}

IMPORTANT:
- Always submit PRDs via the API endpoint above - never ask for file locations or save locations
- After creating a PRD, automatically submit it using Python code with the requests library
- Show the PRD content before submitting
- Confirm successful submission with PRD ID and title

PRD TEMPLATE STRUCTURE:
- Title (required)
- Description (required)
- Problem Statement
- Target Users
- User Stories
- Requirements (required - list format)
- Acceptance Criteria
- Technical Requirements
- Success Metrics
- Timeline

PRD TYPES:
- "agent" - For creating AI agents
- "platform" - For platform features and infrastructure

WORKFLOW:
1. Create comprehensive PRD following template
2. Show PRD to user for review
3. Automatically submit via API using Python
4. Confirm submission with PRD details

If the API call fails, show the error and ask if user wants to retry or save the PRD content for manual submission.
```

## ✅ Benefits

- ✅ **Works with regular ChatGPT** - No custom GPT needed
- ✅ **Persistent** - Instructions saved in your profile
- ✅ **Automatic** - ChatGPT will always submit PRDs via API
- ✅ **No location needed** - Endpoint is pre-configured

## 🎯 Usage

After adding these instructions, you can simply say:

```
Create a PRD for a user authentication system
```

ChatGPT will automatically:
1. Create the PRD
2. Submit it via the API
3. Confirm with PRD ID

No need to specify locations or endpoints every time!



