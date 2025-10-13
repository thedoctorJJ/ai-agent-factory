# Real Devin AI Integration with MCP

## Overview
This guide shows you how to set up **real integration** with Devin AI using MCP (Model Context Protocol) instead of the mock implementation. This works with Devin AI's Core plan (no API access required).

## 🎯 **New Architecture: Application → MCP Server → Devin AI**

Instead of Devin AI needing API access to our platform, we now:
1. **Load PRD data into the MCP server cache** from our application
2. **Devin AI accesses the MCP server** to get the cached data
3. **No API access required** - everything works through MCP protocol

## 🎯 How It Works

### Current Mock vs Real Integration:

**❌ Mock Implementation (Current):**
- Creates fake "4/4 steps completed" 
- Generates mock agents with fake URLs
- No actual Devin AI interaction

**✅ Real MCP Integration (New):**
- Devin AI accesses PRDs through MCP tools
- Creates real agents in the platform
- Updates status when implementation is complete
- Works with Devin AI Core plan (free)

## 🔧 Setup Instructions

### Step 1: Configure Multi-Token GitHub Access

The MCP server supports secure multi-token GitHub integration for different organizations:

**Create Environment File** (`scripts/mcp/.env`):
```bash
# GitHub Multi-Token Configuration
GITHUB_TOKEN_TELLENAI=ghp_xxxxx_for_tellenai_org
GITHUB_TOKEN_THEDOCTORJJ=ghp_xxxxx_for_thedoctorjj_account
DEFAULT_GITHUB_ORG=thedoctorJJ
```

**Token Requirements:**
- **`repo`** scope: Full control of repositories
- **`admin:org`** scope: Full control of organizations (for org repos)
- **Organization Access**: Ensure tokens have access to target organizations

**Supported Targets:**
- ✅ **Organizations**: `tellenai`, `tellen-academy`
- ✅ **Personal Accounts**: `thedoctorJJ`
- ✅ **Automatic Detection**: MCP server automatically selects correct token and API endpoint

### Step 2: Start the MCP Integration

Use the provided startup script to run all services:

```bash
cd /Users/jason/Repositories/end-cap-agent-factory
./scripts/start-mcp-integration.sh
```

This will start:
- **MCP HTTP Server** on port 8001
- **Backend API** on port 8000  
- **Frontend** on port 3000

### Step 2: Configure MCP Server in Devin AI

1. **Open Devin AI** in your browser
2. **Go to Settings** → **Integrations** → **MCP Servers**
3. **Click "Add MCP Server"**

### Step 3: MCP Server Configuration

Fill out the configuration form:

```
Server Name: AI Agent Factory - Devin Integration
Transport Type: STDIO
Icon: 🤖
Description: Access cached PRDs and create agents in AI Agent Factory platform
Enabled: ✅ (toggle ON)
```

### Step 4: STDIO Configuration

```
Command: python3
Arguments: /Users/jason/Repositories/end-cap-agent-factory/scripts/mcp/devin-mcp-server.py
```

**Note**: Update the path to match your system.

### Step 5: Environment Variables

Add these environment variables to your system or `.env` file:

```bash
# Required
ENDCAP_API_URL=http://localhost:8000
GITHUB_TOKEN=your-github-token
GITHUB_ORG_NAME=thedoctorJJ

# Optional (for advanced features)
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_ROLE_KEY=your-supabase-key
```

### Step 6: Test the Integration

1. **Save the MCP server configuration**
2. **Click "Test listing tools"**
3. **You should see these tools**:
   - `get_prd_details`
   - `list_available_prds`
   - `create_agent_from_prd`
   - `get_agent_library_info`
   - `update_agent_status`
   - `load_prd_data`

## 🚀 How to Use

### 1. Upload a PRD
- Go to your AI Agent Factory platform
- Upload a completed PRD
- The PRD will appear in the queue

### 2. Trigger Devin AI
- Go to the "Devin" tab in your platform
- Select the PRD you want to process
- Click "Generate Devin MCP Prompt"
- **PRD data is automatically loaded** into the MCP server cache
- **Copy the generated prompt** (it now includes MCP instructions)

### 3. Use with Devin AI
- **Paste the prompt** into Devin AI
- **Devin will automatically use the MCP tools** to:
  - Get the cached PRD details (no API calls needed!)
  - Access agent libraries
  - Create the agent record
  - Implement the agent code
  - Update the status when complete

### 4. Real Workflow Example

When you paste the prompt into Devin AI, it will:

1. **Call `get_prd_details`** to get the cached PRD data (instant access!)
2. **Call `get_agent_library_info`** to understand available tools
3. **Call `create_agent_from_prd`** to create the agent record
4. **Implement the agent** based on the PRD requirements
5. **Call `update_agent_status`** when deployment is complete

## 🎯 **Key Benefits of New Architecture:**

### Before (API-dependent):
- ❌ Required Devin AI Team plan ($500/month)
- ❌ Needed API access to our platform
- ❌ Network calls for every PRD access
- ❌ Potential rate limiting issues

### After (MCP Cache-based):
- ✅ **Works with Devin AI Core plan** (free!)
- ✅ **No API access required** to our platform
- ✅ **Instant PRD access** from cache
- ✅ **No rate limiting** concerns
- ✅ **Offline-capable** once data is cached

## 🎉 Benefits

### Before (Mock):
- ❌ Fake progress indicators
- ❌ Mock agents with fake URLs
- ❌ No real Devin AI interaction
- ❌ Manual copy-paste workflow

### After (Real MCP):
- ✅ **Real PRD access** through MCP tools
- ✅ **Actual agent creation** in the platform
- ✅ **Real status updates** when complete
- ✅ **Seamless integration** with Devin AI
- ✅ **Works with Core plan** (no API access needed)

## 🔍 Available MCP Tools

### `get_prd_details`
- **Purpose**: Get complete PRD information
- **Usage**: When Devin needs to understand requirements
- **Parameters**: `{"prd_id": "your-prd-id"}`

### `list_available_prds`
- **Purpose**: See all PRDs ready for processing
- **Usage**: When Devin wants to see available work
- **Parameters**: `{"status": "ready_for_devin"}` (optional)

### `create_agent_from_prd`
- **Purpose**: Create agent record in the platform
- **Usage**: When Devin is ready to start implementation
- **Parameters**: `{"prd_id": "...", "agent_name": "...", "agent_description": "..."}`

### `get_agent_library_info`
- **Purpose**: Access available templates and tools
- **Usage**: When Devin needs to understand the tech stack
- **Parameters**: `{}`

### `update_agent_status`
- **Purpose**: Update agent status when complete
- **Usage**: When Devin finishes implementation and deployment
- **Parameters**: `{"agent_id": "...", "status": "active", "repository_url": "...", "deployment_url": "..."}`

## 🛠️ Troubleshooting

### MCP Server Not Working
1. **Check the path** to `devin-mcp-server.py`
2. **Verify Python 3** is available
3. **Check environment variables** are set
4. **Test the server manually**:
   ```bash
   cd /Users/jason/Repositories/end-cap-agent-factory/scripts/mcp
   python3 devin-mcp-server.py
   ```

### Devin AI Can't Access Tools
1. **Restart Devin AI** after adding the MCP server
2. **Check the MCP server logs** in Devin AI
3. **Verify the API URL** is accessible from Devin AI
4. **Test the API** manually:
   ```bash
   curl http://localhost:8000/api/v1/prds
   ```

### Agent Creation Fails
1. **Check the backend logs** for errors
2. **Verify the PRD exists** and is accessible
3. **Check database connectivity**
4. **Verify GitHub token** has proper permissions

## 📋 Next Steps

1. **Configure the MCP server** in Devin AI
2. **Test with a simple PRD** first
3. **Verify the complete workflow** works
4. **Scale up** to more complex agents

## 🎯 Success Criteria

You'll know it's working when:
- ✅ Devin AI can access PRD details through MCP
- ✅ Agent records are created in your platform
- ✅ Devin AI updates agent status when complete
- ✅ Real agents appear in your dashboard
- ✅ No more mock "4/4 steps completed" messages

This is a **real integration** that works with Devin AI's free Core plan!
