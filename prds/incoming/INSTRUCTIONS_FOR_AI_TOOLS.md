# Instructions for AI Tools (ChatGPT, Gemini, Claude, etc.)

## 🌐 Cloud-Based PRD Submission

**Use the API endpoint to submit PRDs directly to the cloud** - no local file access needed!

## 📋 How to Submit PRDs

### For ChatGPT (with API Access)

When creating a PRD, submit it directly via API:

**API Endpoint**: 
```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
```

**Request Format**:
```json
{
  "content": "# PRD Title\n\n## Description\nYour PRD content here..."
}
```

**Example ChatGPT Prompt**:
```
Create a PRD for a user authentication system and submit it to the AI Agent Factory API:

POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

{
  "content": "[Your PRD markdown content here]"
}
```

### For ChatGPT (Code Interpreter / File Creation)

If you need to create a file first, you can use Python to submit via API:

```python
import requests

prd_content = """# User Authentication System

## Description
A comprehensive authentication system with JWT tokens...

## Requirements
- User registration
- Login/logout
- Password reset
"""

response = requests.post(
    "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming",
    json={"content": prd_content}
)

if response.status_code in [200, 201]:
    prd = response.json()
    print(f"✅ PRD submitted successfully!")
    print(f"   ID: {prd['id']}")
    print(f"   Title: {prd['title']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

## 📝 PRD Format

Your PRD should follow the standard PRD template format. Include at minimum:

- **Title** - PRD title
- **Description** - High-level overview  
- **Requirements** - List of requirements

See `prds/templates/` for complete template examples.

## ✅ What Happens After Submission

1. PRD is parsed and structured
2. Saved to the cloud database
3. Status set to `uploaded`
4. Appears in the dashboard immediately
5. Ready for processing

## 🔗 Complete Documentation

See `docs/guides/INCOMING_PRD_WORKFLOW.md` for complete API documentation and examples.

