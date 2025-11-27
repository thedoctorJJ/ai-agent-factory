# Instructions for ChatGPT - Copy and Paste This

Copy the text below and paste it into ChatGPT:

---

## PRD Submission to AI Agent Factory

I have an AI Agent Factory platform that can automatically process Product Requirements Documents (PRDs). When I create or describe a PRD in our conversation, you should submit it to my platform using the following webhook endpoint.

### Webhook Endpoint
**URL**: `https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/api/v1/prds/incoming`
**Method**: POST
**Content-Type**: application/json

### Request Format
```json
{
  "content": "# PRD Title\n\n## Description\n[PRD content in markdown format]"
}
```

### When to Submit
Submit a PRD when:
- I explicitly ask you to create a PRD
- I describe a product or feature that should be documented as a PRD
- I say "submit this PRD" or similar

### PRD Format
Format the PRD content as markdown with these sections:
- Title (as H1)
- Description
- Requirements (as a list)
- Technical Requirements
- Success Metrics (if provided)
- Timeline (if provided)

### Example
If I say: "Create a PRD for a user authentication system with JWT tokens"

You should:
1. Format it as a proper PRD in markdown
2. Submit it to the webhook endpoint above
3. Confirm submission and provide the PRD ID if returned

### Important Notes
- Only submit complete, well-structured PRDs
- Don't submit if I'm just discussing ideas or asking questions
- Always confirm when you've submitted a PRD
- If the submission fails, let me know the error

---



