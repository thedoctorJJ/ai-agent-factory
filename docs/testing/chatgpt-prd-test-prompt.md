# ChatGPT PRD Test Prompt

## Prompt to Test End-to-End PRD Creation

Copy and paste this into ChatGPT:

---

**Please create a Product Requirements Document (PRD) for an "AI-Powered Code Review Assistant".**

This should be a comprehensive PRD that includes:

- **Title**: AI-Powered Code Review Assistant
- **Description**: An intelligent code review assistant that uses AI to analyze code changes, suggest improvements, and detect potential bugs before code is merged
- **Requirements**: 
  - Automated code analysis using AI models
  - Integration with GitHub pull requests
  - Real-time feedback on code quality
  - Security vulnerability detection
  - Performance optimization suggestions
  - Code style and best practices enforcement
- **Technical Requirements**: 
  - Integration with GitHub API
  - AI model for code analysis (OpenAI GPT-4 or similar)
  - Real-time webhook processing
  - Database for storing review history
  - Notification system for developers

Please submit this PRD to the AI Agent Factory using the available tools/actions.

---

## What Should Happen

1. ChatGPT will format the conversation as a PRD
2. ChatGPT will call the MCP server's `submit_prd_from_conversation` tool
3. MCP server will:
   - Check for duplicates in GitHub
   - Commit the PRD file to GitHub (prds/queue/)
   - Return success confirmation
4. GitHub Actions will automatically sync to database (within 30 seconds)
5. Website will show the new PRD

## Expected Response from ChatGPT

You should see something like:
```
✅ PRD submitted successfully!

Status: ok
File: prds/queue/2025-11-27_ai-powered-code-review-assistant.md
GitHub URL: https://github.com/thedoctorJJ/ai-agent-factory/blob/main/prds/queue/...
```

---

**Note**: If ChatGPT says it can't find the tool or action, make sure the MCP server is configured and the ChatGPT Actions are set up correctly.

