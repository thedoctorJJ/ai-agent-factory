# Devin AI Integration Framework

## Overview
Devin AI acts as the autonomous engineering layer, connecting PRDs, agent libraries, and orchestration workflows to automatically create, update, and execute agents. Since Devin AI's API is not yet publicly available, we use a copy-paste workflow for integration.

## Core Responsibilities
1. **Agent Review**: Scans Agent Library and Tool Library.
2. **Orchestration Plan Generation**: Reads PRD JSON or GitHub repo and generates `manifest.json`.
3. **Agent Creation**: Builds agent files, adds prompts, tools, and metadata.
4. **Execution**: Deploys agents through FastAPI endpoints and connects to Supabase vector DB.
5. **Versioning & Governance**: Maintains agent versions and audit logs.

## Copy-Paste Workflow (Current Implementation)

Since Devin AI's API is not yet publicly available, we use a manual copy-paste workflow:

### 1. PRD to Devin AI
```
[PRD Created] --> [Generate Devin Prompt] --> [Copy to Devin AI] --> [Devin Generates Code]
```

### 2. Code Back to Platform
```
[Devin AI Output] --> [Copy Code] --> [Paste to Platform] --> [Deploy Agent]
```

### 3. Streamlined Workflow Steps
1. **Upload completed PRD** to the platform
2. **Generate optimized prompt** for Devin AI with MCP instructions
3. **Copy prompt** to Devin AI web interface
4. **Devin AI + MCP Servers** automatically:
   - Generate agent code
   - Create GitHub repository
   - Set up Supabase database
   - Deploy to Google Cloud Run
   - Integrate with platform
5. **Verify deployment** in platform dashboard

### 4. MCP Server Integration
- **GitHub MCP**: Automatic repository creation and code commits
- **Supabase MCP**: Automatic database setup and metadata creation
- **Google Cloud MCP**: Automatic Cloud Run deployment and monitoring
- **Platform Integration**: Automatic API endpoint creation and testing

## Future API Integration Flow
```
[PRD / GitHub Repo] --> Devin AI API
↓
[Agent Library + Tool Library] --> Analysis
↓
[Orchestration Plan Generated]
↓
[New Agent Scaffolds + Metadata Updated in Supabase]
↓
[Execution via FastAPI / Cloud Run]
```

## Key Principles
- Fully autonomous but auditable
- Reusable components
- Modular orchestration
- Integration-ready with voice, GitHub MCP, and frontend dashboard
