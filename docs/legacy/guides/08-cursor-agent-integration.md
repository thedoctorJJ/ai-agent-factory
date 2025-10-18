# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[02 - Devin AI Integration](../../02-devin-ai-integration.md)** — Current AI integration documentation
> 
> **This file is preserved for historical reference only.**

---

# Cursor Agent Integration Guide

## 🎯 **Overview**

This guide shows you how to connect Cursor Agent to your AI Agent Factory platform, giving you complete control over all platform components directly from Cursor.

## 🚀 **What You Can Do**

With Cursor Agent integration, you can:

- **Monitor Platform Health**: Check status of all services (Supabase, GitHub, Google Cloud, OpenAI)
- **Manage PRDs**: Create, view, update, and track PRD progress
- **Deploy Agents**: Deploy agents directly to Google Cloud Run
- **Manage Repositories**: Create and manage GitHub repositories
- **Database Operations**: Test connections and view schema
- **Start Services**: Launch backend and frontend servers locally
- **Environment Management**: Validate configuration and troubleshoot issues

## 🔧 **Setup Process**

### **Step 1: Run the Setup Script**

```bash
cd /Users/jason/Repositories/ai-agent-factory
./scripts/setup-cursor-agent-integration.sh
```

This script will:
- ✅ Verify the MCP server is properly configured
- ✅ Test all service connections
- ✅ Validate environment configuration
- ✅ Provide setup instructions

### **Step 2: Add MCP Server to Cursor Agent**

1. **Open Cursor Agent Settings**
2. **Navigate to MCP Servers**
3. **Add New Server** with this configuration:

```json
{
  "name": "AI Agent Factory - Cursor Integration",
  "command": "python3",
  "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"],
  "env": {
    "DATABASE_URL": "postgresql://postgres:postgres@db.your-project.supabase.co:5432/postgres",
    "SUPABASE_URL": "https://your-project.supabase.co",
    "SUPABASE_KEY": "your-supabase-key",
    "SUPABASE_SERVICE_ROLE_KEY": "your-supabase-key",
    "GOOGLE_CLOUD_PROJECT_ID": "your-project-id",
    "GITHUB_TOKEN": "your-github-token",
    "GITHUB_ORG_NAME": "thedoctorJJ",
    "OPENAI_API_KEY": "your-openai-api-key"
  }
}
```

### **Step 3: Test the Integration**

Use these commands in Cursor Agent to test:

```
get_platform_status
```

This should return the status of all connected services.

## 🛠️ **Available Tools**

### **Platform Management**
- `get_platform_status` - Get comprehensive status of all platform components
- `validate_environment` - Validate all environment configuration

### **PRD Management**
- `list_prds` - List all PRDs with optional status filtering
- `get_prd_details` - Get detailed information about a specific PRD
- `create_prd` - Create a new PRD in the system
- `update_prd_status` - Update PRD status (queue, in-progress, completed, failed)

### **Agent Management**
- `list_agents` - List all agents with optional status filtering
- `get_agent_details` - Get detailed information about a specific agent
- `deploy_agent` - Deploy an agent to Google Cloud Run

### **Repository Management**
- `create_github_repo` - Create a new GitHub repository
- `get_github_repo` - Get information about a GitHub repository

### **Database Operations**
- `test_database_connection` - Test the database connection
- `get_database_schema` - Get the current database schema

### **Development Tools**
- `start_backend_server` - Start the backend API server locally
- `start_frontend_server` - Start the frontend development server locally

## 📋 **Common Workflows**

### **1. Check Platform Health**
```
get_platform_status
validate_environment
```

### **2. Create and Process a PRD**
```
create_prd
list_prds
get_prd_details
update_prd_status
```

### **3. Deploy an Agent**
```
create_github_repo
deploy_agent
list_agents
```

### **4. Start Development Environment**
```
start_backend_server
start_frontend_server
```

## 🔍 **Troubleshooting**

### **Connection Issues**
If you get connection errors:

1. **Check Environment**: Use `validate_environment` to see what's configured
2. **Test Database**: Use `test_database_connection` to verify Supabase
3. **Check Services**: Use `get_platform_status` to see service health

### **Permission Issues**
If you get permission errors:

1. **GitHub**: Verify your GitHub token has the right permissions
2. **Google Cloud**: Check your service account key file exists
3. **Supabase**: Verify your service role key is correct

### **MCP Server Issues**
If the MCP server doesn't start:

1. **Check Path**: Ensure the path to the MCP server is correct
2. **Check Permissions**: Make sure the script is executable
3. **Check Dependencies**: Ensure all Python dependencies are installed

## 🎯 **Best Practices**

### **1. Start with Status Checks**
Always begin by checking platform status:
```
get_platform_status
```

### **2. Validate Before Operations**
Before making changes, validate your environment:
```
validate_environment
```

### **3. Use Specific Filters**
When listing items, use status filters to focus on relevant data:
```
list_prds status=queue
list_agents status=deployed
```

### **4. Monitor Deployments**
After deploying agents, check their status:
```
list_agents
get_agent_details
```

## 🔐 **Security Notes**

- All API keys and tokens are securely stored in environment variables
- The MCP server only exposes necessary functionality
- Database operations use service role keys with appropriate permissions
- GitHub operations are limited to your organization

## 📚 **Additional Resources**

- **MCP Configuration**: `config/cursor-agent-mcp-config.json`
- **Setup Script**: `scripts/setup-cursor-agent-integration.sh`
- **MCP Server**: `scripts/mcp/cursor-agent-mcp-server.py`
- **Environment Config**: `config/env/.env.local`

## 🎉 **You're Ready!**

With this integration, you now have complete control over your AI Agent Factory platform directly from Cursor Agent. You can manage PRDs, deploy agents, create repositories, and monitor the entire system without leaving your development environment.
