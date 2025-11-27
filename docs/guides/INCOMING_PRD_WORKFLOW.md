# Incoming PRD Workflow Guide

This guide explains how to submit PRDs to the AI Agent Factory from external sources like ChatGPT, Gemini, Claude, or any other tool.

## 🎯 Overview

The AI Agent Factory supports cloud-based PRD submission via API endpoint. This is the recommended method for AI tools.

## 🌐 Option 1: Webhook API (Recommended - Cloud-Based)

### Endpoint

```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
```

This is a **cloud-based endpoint** - no local file access needed!

### Method 1: JSON Body (Recommended for AI Tools)

**Request:**
```bash
curl -X POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# PRD Title\n\n## Description\nYour PRD content here..."
  }'
```

**Python Example:**
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
    print(f"PRD created: {prd['id']}")
```

### Method 2: File Upload

**Request:**
```bash
curl -X POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -F "file=@my-prd.md"
```

**Python Example:**
```python
import requests

with open("my-prd.md", "rb") as f:
    response = requests.post(
        "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming",
        files={"file": ("my-prd.md", f, "text/markdown")}
    )

if response.status_code in [200, 201]:
    prd = response.json()
    print(f"PRD created: {prd['id']}")
```

### Method 3: Form Data

**Request:**
```bash
curl -X POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "content=# PRD Title%0A%0A## Description%0A..."
```

## 🤖 Instructions for AI Tools

### For ChatGPT

**System Prompt Addition:**
```
When creating a PRD, save it to this folder:
/Users/jason/Repositories/ai-agent-factory/prds/incoming/

File naming format: YYYY-MM-DD_prd-title.md

The PRD will be automatically processed and added to the AI Agent Factory system.
```

**Example ChatGPT Prompt:**
```
Create a PRD for a user authentication system and save it to:
/Users/jason/Repositories/ai-agent-factory/prds/incoming/2025-11-16_user-authentication-system.md
```

### For Gemini / Claude

Use the same folder path and file naming convention. The file watcher will automatically process any `.md` file added to the `prds/incoming/` folder.

### For Tools with API Access

If your AI tool supports API calls or webhooks, use the JSON API endpoint:

```
POST https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds/incoming
Content-Type: application/json

{
  "content": "# Your PRD markdown content here..."
}
```

## 📋 PRD Format Requirements

Your PRD should follow the standard PRD template format. See examples in:
- `prds/templates/prd-template-agent.md` - For AI agent PRDs
- `prds/templates/prd-template-platform.md` - For platform feature PRDs

### Minimum Required Sections

- **Title** - PRD title
- **Description** - High-level overview
- **Requirements** - List of requirements

### Recommended Sections

- Problem Statement
- Target Users
- User Stories
- Acceptance Criteria
- Technical Requirements
- Success Metrics
- Timeline

## ✅ What Happens After Submission

1. **Parsing**: PRD content is parsed and structured
2. **Database Upload**: PRD is saved to the database
3. **Status**: PRD status is set to `uploaded`
4. **File Organization**: File is moved to `prds/uploaded/` (if using file folder)
5. **Dashboard**: PRD appears in the dashboard under "PRD Repository"

## 🔍 Troubleshooting

### File Watcher Not Running

**Problem**: Files added to `prds/incoming/` aren't being processed.

**Solution**: 
1. Start the file watcher: `python3 scripts/prd-management/watch-incoming-prds.py`
2. Or process manually: `./scripts/prd-management/process-incoming-prds.sh`

### API Errors

**Problem**: API returns 400 or 500 errors.

**Solutions**:
- Check PRD format matches template
- Ensure content is valid markdown
- Verify backend URL is correct
- Check backend logs for detailed error messages

### Duplicate PRDs

**Problem**: PRD already exists in system.

**Solution**: The system detects duplicates by title. If you want to update an existing PRD, use the update endpoint or modify the file directly.

## 📚 Related Documentation

- [PRD System Guide](./04-prd-system.md) - Complete PRD system documentation
- [PRD Sync Strategy](./PRD_SYNC_STRATEGY.md) - File-based PRD sync workflow
- [API Reference](../api-reference/rest-api.md) - Complete API documentation

## 🎯 Quick Start

1. **Create PRD** using your preferred AI tool
2. **Save to folder**: `prds/incoming/YYYY-MM-DD_prd-title.md`
3. **Start watcher**: `python3 scripts/prd-management/watch-incoming-prds.py`
4. **Done!** PRD is automatically processed

Or use the API directly if your tool supports it!

