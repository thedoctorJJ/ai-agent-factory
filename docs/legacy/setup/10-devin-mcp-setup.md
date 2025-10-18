# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[03 - Setup Guide](../../03-setup-guide.md)** — Current setup documentation
> 
> **This file is preserved for historical reference only.**

---

# Devin AI MCP Server Setup Guide

## Overview
This guide helps you configure MCP (Model Context Protocol) servers in Devin AI to enable automatic deployment and integration with the AI Agent Factory Agent Factory.

## 🎯 Streamlined Workflow
With MCP servers configured, the workflow becomes:
```
[PRD Created] → [Copy to Devin AI] → [Devin AI + MCP Servers] → [Auto-Deploy to Platform]
```

## 🔧 Required MCP Servers

### 1. GitHub MCP Server
**Purpose**: Automatically create repositories and commit agent code

**Configuration in Devin AI**:
1. Go to **Settings** → **Integrations** → **MCP Servers**
2. Add GitHub MCP Server
3. Configure with:
   - **Organization**: `thedoctorJJ` (or your GitHub org)
   - **Repository Prefix**: `ai-agents-`
   - **Permissions**: Full repository access
   - **Branch Protection**: Enable for main branch

**Capabilities**:
- ✅ Create new repositories automatically
- ✅ Commit agent code with proper structure
- ✅ Set up GitHub Actions workflows
- ✅ Configure branch protection rules
- ✅ Create pull requests for reviews

### 2. Supabase MCP Server
**Purpose**: Automatically set up database tables and metadata

**Configuration in Devin AI**:
1. Add Supabase MCP Server
2. Configure with:
   - **Project URL**: `https://your-project.supabase.co`
   - **Service Role Key**: Your Supabase service role key
   - **Database**: `postgres`

**Capabilities**:
- ✅ Create agent metadata tables
- ✅ Set up execution logs tables
- ✅ Configure metrics and monitoring tables
- ✅ Set up authentication and permissions
- ✅ Create database triggers and functions

### 3. Google Cloud MCP Server
**Purpose**: Automatically deploy agents to Cloud Run

**Configuration in Devin AI**:
1. Add Google Cloud MCP Server
2. Configure with:
   - **Project ID**: `ai-agent-factory`
   - **Service Account**: Your GCP service account key
   - **Region**: `us-central1`

**Capabilities**:
- ✅ Deploy agents to Cloud Run
- ✅ Configure environment variables
- ✅ Set up monitoring and logging
- ✅ Configure auto-scaling
- ✅ Set up custom domains

## 🚀 Setup Instructions

### Step 1: Configure GitHub MCP Server
```bash
# In Devin AI, add MCP server with these settings:
{
  "name": "github",
  "type": "github",
  "config": {
    "organization": "thedoctorJJ",
    "repository_prefix": "ai-agents-",
    "permissions": ["repo", "workflow", "admin:org"]
  }
}
```

### Step 2: Configure Supabase MCP Server
```bash
# In Devin AI, add MCP server with these settings:
{
  "name": "supabase",
  "type": "supabase",
  "config": {
    "url": "https://your-project.supabase.co",
    "service_role_key": "your-service-role-key",
    "database": "postgres"
  }
}
```

### Step 3: Configure Google Cloud MCP Server
```bash
# In Devin AI, add MCP server with these settings:
{
  "name": "google-cloud",
  "type": "google-cloud",
  "config": {
    "project_id": "ai-agent-factory",
    "service_account_key": "your-service-account-key",
    "region": "us-central1"
  }
}
```

## 📋 MCP Server Capabilities

### GitHub MCP Server
- **Repository Creation**: Automatically creates `ai-agents-{name}` repositories
- **Code Structure**: Sets up proper folder structure with agent code
- **CI/CD**: Configures GitHub Actions for testing and deployment
- **Documentation**: Generates README files with usage instructions

### Supabase MCP Server
- **Database Schema**: Creates required tables for agent metadata
- **Authentication**: Sets up proper user permissions and roles
- **Monitoring**: Configures logging and metrics collection
- **API Integration**: Sets up database triggers for real-time updates

### Google Cloud MCP Server
- **Cloud Run Deployment**: Automatically deploys agents as microservices
- **Environment Variables**: Configures all necessary environment variables
- **Monitoring**: Sets up Cloud Monitoring and Logging
- **Scaling**: Configures auto-scaling based on demand

## 🔄 Automated Workflow

### What Happens Automatically:
1. **Repository Creation**: GitHub MCP creates new repo with proper structure
2. **Code Generation**: Devin AI generates complete agent implementation
3. **Database Setup**: Supabase MCP creates all necessary tables and relationships
4. **Deployment**: Google Cloud MCP deploys agent to Cloud Run
5. **Integration**: Agent is automatically integrated with the platform
6. **Monitoring**: All monitoring and logging is configured automatically

### What You Need to Do:
1. **Upload completed PRD** to the platform
2. **Copy prompt** to Devin AI
3. **Wait for completion** (usually 5-15 minutes)
4. **Verify deployment** in the platform dashboard

## 🎉 Benefits

### Before (Manual Workflow):
- ❌ Copy code from Devin AI
- ❌ Create repository manually
- ❌ Set up database tables manually
- ❌ Deploy to Cloud Run manually
- ❌ Configure monitoring manually
- ❌ Integrate with platform manually

### After (MCP Automated Workflow):
- ✅ **One-click deployment** via MCP servers
- ✅ **Automatic repository creation** with proper structure
- ✅ **Automatic database setup** with all required tables
- ✅ **Automatic Cloud Run deployment** with monitoring
- ✅ **Automatic platform integration** and testing
- ✅ **Complete end-to-end automation**

## 🔧 Troubleshooting

### Common Issues:
1. **MCP Server Connection Failed**: Check API keys and permissions
2. **Repository Creation Failed**: Verify GitHub organization access
3. **Database Setup Failed**: Check Supabase service role permissions
4. **Deployment Failed**: Verify Google Cloud service account permissions

### Debug Steps:
1. Check MCP server logs in Devin AI
2. Verify API keys and permissions
3. Test individual MCP server connections
4. Check platform logs for integration issues

## 📚 Next Steps

1. **Configure MCP Servers** in Devin AI using this guide
2. **Test the workflow** with a simple agent
3. **Verify automatic deployment** works correctly
4. **Scale up** to more complex agents

With MCP servers configured, you'll have a truly automated agent creation and deployment pipeline! 🚀
