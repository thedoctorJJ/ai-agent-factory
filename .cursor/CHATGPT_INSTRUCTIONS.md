# Instructions for ChatGPT - Cloud-Based PRD Submission

## 🌐 Submit PRDs Directly to Cloud

When creating PRDs, submit them directly to the AI Agent Factory cloud API - no local file access needed!

## 📋 API Endpoint

```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
```

## 🚀 How to Use

### Method 1: Direct API Call (If ChatGPT has API access)

**Request**:
```json
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

{
  "content": "# PRD Title\n\n## Description\nYour PRD markdown content here..."
}
```

### Method 2: Python Code (Using Code Interpreter)

If ChatGPT has access to Python, use this code:

```python
import requests

# Your PRD content
prd_content = """# User Authentication System

## Description
A comprehensive authentication system with JWT tokens, password reset, and multi-factor authentication.

## Requirements
- User registration with email verification
- Login/logout functionality
- Password reset via email
- JWT token-based authentication
- Session management
- Multi-factor authentication (optional)

## Technical Requirements
- FastAPI backend
- Supabase for user storage
- JWT tokens for authentication
- Email service for verification
"""

# Submit to AI Agent Factory
response = requests.post(
    "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming",
    json={"content": prd_content},
    timeout=30
)

if response.status_code in [200, 201]:
    prd = response.json()
    print(f"✅ PRD submitted successfully!")
    print(f"   ID: {prd['id']}")
    print(f"   Title: {prd['title']}")
    print(f"   Status: {prd['status']}")
else:
    print(f"❌ Error: HTTP {response.status_code}")
    print(response.text)
```

## 📝 Example ChatGPT Prompt

```
Create a PRD for a user authentication system and submit it to the AI Agent Factory using this API:

POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

{
  "content": "[Create the PRD markdown content here]"
}

The PRD should include:
- Title
- Description
- Requirements
- Technical Requirements
- Success Metrics
```

## ✅ What Happens

1. PRD is submitted to the cloud API
2. Automatically parsed and structured
3. Saved to the database
4. Appears in the dashboard immediately
5. Ready for agent creation

## 📚 PRD Format

Follow the standard PRD template format. Minimum required:
- **Title**
- **Description**
- **Requirements**

See `prds/templates/prd-template-agent.md` for complete template.

## 🔗 Complete Documentation

See `docs/guides/INCOMING_PRD_WORKFLOW.md` for complete API documentation.



