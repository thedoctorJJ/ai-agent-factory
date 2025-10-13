# Devin AI Workflow Guide

## 🎯 Complete Workflow: AI Agent Factory + Devin AI

This guide explains how to use Devin AI with the AI Agent Factory system.

## 🚀 Step-by-Step Process

### 1. Load PRD to MCP Server
- Go to the AI Agent Factory platform
- Navigate to the "Devin" tab
- Select a PRD from the dropdown
- Click "📤 Load PRD to MCP Server"
- Copy the simple startup prompt that appears

### 2. Start Devin AI
- Open Devin AI in your browser
- Paste the simple startup prompt into Devin AI
- Devin will use the MCP tool to get the complete guide
- Devin will follow the guide and check for available PRDs

### 3. Devin AI Process
Devin AI will:
1. **Get startup guide**: Use `get_startup_guide` MCP tool
2. **Check for work**: Use `check_available_prds` MCP tool
3. **Get PRD details**: Use `get_prd_details` MCP tool
4. **Understand tools**: Use `get_agent_library_info` MCP tool
5. **Create agent record**: Use `create_agent_from_prd` MCP tool
6. **Implement agent**: Code, deploy, test
7. **Update status**: Use `update_agent_status` MCP tool

### 4. Monitor Progress
- Check the AI Agent Factory platform for status updates
- Agents will appear in the "Agents" tab as they're created
- Status will update from "draft" to "active" when complete

## 🔧 Technical Details

### MCP Server
- **Port**: 8001
- **Health Check**: http://localhost:8001/health
- **Tools**: http://localhost:8001/mcp/tools

### Available MCP Tools
- `get_startup_guide` - Get complete startup guide
- `check_available_prds` - See what PRDs are ready
- `get_prd_details` - Get full PRD information
- `list_available_prds` - List all PRDs in system
- `create_agent_from_prd` - Create agent record
- `get_agent_library_info` - Access agent libraries
- `update_agent_status` - Update agent status
- `load_prd_data` - Load PRD data into cache

### Technical Stack
- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Google Cloud Run
- **Repository**: GitHub (thedoctorJJ organization)
- **Monitoring**: Built-in health checks and logging

## 🎉 Benefits

- ✅ **Works with Devin AI Core plan** (free!)
- ✅ **No API access required** to our platform
- ✅ **Instant PRD access** from cache
- ✅ **No rate limiting** concerns
- ✅ **Offline-capable** once data is cached
- ✅ **Complete cold start guide** for Devin AI

## 🚀 Quick Start

1. **Start services**: `./scripts/start-mcp-integration.sh`
2. **Load PRD**: Use the AI Agent Factory platform
3. **Start Devin**: Copy simple prompt to Devin AI
4. **Monitor**: Check platform for updates

That's it! Devin AI will fetch the guide and handle the rest automatically.

## 🎯 Benefits of This Approach

- ✅ **Simple prompt** - Easy to copy and paste
- ✅ **Dynamic guide** - Always up-to-date from MCP server
- ✅ **Maintainable** - Update guide without changing frontend
- ✅ **Self-contained** - Guide includes everything needed
- ✅ **Version controlled** - Guide stored in GitHub repository
