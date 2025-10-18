# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[04-06 - System Guides](../../04-prd-system.md)** — Current implementation documentation
> 
> **This file is preserved for historical reference only.**

---

# DevOps & Deployment Flow

## Overview
This document describes the deployment pipeline and CI/CD workflow for the AI Agent Factory Agent Factory.

## Local Development

### Environment Setup
```bash
# Initialize environment configuration
./scripts/config/env-manager.sh init

# Start development environment
./scripts/setup/dev-setup.sh
```

### Backend Development
```bash
cd backend
source venv/bin/activate
python -m uvicorn fastapi_app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend/next-app
npm run dev
```

### Scripts Organization
- **Setup**: `./scripts/setup/` - Development environment setup
- **Configuration**: `./scripts/config/` - Environment and service configuration
- **Deployment**: `./scripts/deployment/` - Deployment automation
- **Testing**: `./scripts/testing/` - Test automation
- **MCP**: `./scripts/mcp/` - MCP server management

## CI/CD
- Use GitHub Actions to automate:
  - Running tests on backend and frontend
  - Linting and formatting
  - Deploying to Google Cloud Run for both backend and frontend
  - Supabase migrations
- Automatic rollback if deployment fails

## Monitoring & Logging
- Use Google Cloud Logging for backend + MCP service
- Supabase Edge Functions logs for PRD triggers
- Alerts via Slack/email
