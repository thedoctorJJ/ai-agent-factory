# GitHub MCP Service

## Overview
Automates repository creation for each new PRD using GitHub App + MCP integration.  

## Workflow
1. PRD uploaded → stored in Supabase
2. Supabase trigger → MCP service webhook
3. MCP service → creates new repo from template
4. PRD.md and scaffolds added
5. Devin AI registered → builds agents

## GitHub App Setup
- Permissions: Repos read/write, Contents read/write
- Webhook URL: `https://<mcp-service-url>/webhook`
- Events: repository, repository_dispatch

## Security
- GitHub App tokens in Secret Manager
- Webhooks signed & verified
- Repo private, audit logs in Supabase

## Data Flow
```
[PRD Trigger] --> MCP Service --> GitHub Repo Created
↓
[Devin AI Orchestration]
```
