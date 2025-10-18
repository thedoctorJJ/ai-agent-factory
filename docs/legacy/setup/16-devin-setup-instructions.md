# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[03 - Setup Guide](../../03-setup-guide.md)** — Current setup documentation
> 
> **This file is preserved for historical reference only.**

---

# 🚀 Devin AI Setup Instructions - Environment Issues Fixed

## 📋 **Issues Identified & Solutions**

### 1. ✅ **MCP Server Path Issue - FIXED**
**Problem**: Hardcoded macOS path in MCP config
**Solution**: Created portable configuration with absolute path

### 2. 🔧 **GitHub Token Permissions Issue - NEEDS ACTION**
**Problem**: Token lacks `repo` and `admin:org` scopes
**Solution**: Update token permissions (see instructions below)

---

## 🛠️ **Immediate Actions Required**

### **Step 1: Update MCP Configuration in Devin**
Replace your current MCP server configuration with this:

```json
{
  "name": "AI Agent Factory - Devin Integration",
  "description": "MCP server for Devin AI to access PRDs and create agents in the AI Agent Factory platform",
  "icon": "🤖",
  "transport": "stdio",
  "command": "python3",
  "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/devin-mcp-server.py"],
  "secrets": {
    "ENDCAP_API_URL": "AI Agent Factory API URL (default: http://localhost:8000)",
    "GITHUB_TOKEN_TELLENAI": "GitHub personal access token for tellenai organization",
    "GITHUB_TOKEN_THEDOCTORJJ": "GitHub personal access token for thedoctorJJ organization", 
    "DEFAULT_GITHUB_ORG": "Default GitHub organization (tellenai or thedoctorJJ)",
    "SUPABASE_URL": "Supabase project URL",
    "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key"
  }
}
```

### **Step 2: Fix GitHub Token Permissions**

1. **Go to GitHub Token Settings**:
   - Visit: https://github.com/settings/tokens
   - Find your existing token or create a new one

2. **Update Token Scopes**:
   For **tellenai organization** access:
   - ✅ **`repo`** - Full control of private repositories
   - ✅ **`admin:org`** - Full control of orgs and teams
   - ✅ **`write:org`** - Write org and team membership

   For **thedoctorJJ personal account**:
   - ✅ **`repo`** - Full control of private repositories

3. **Update MCP Server Environment**:
   Create/update `scripts/mcp/.env` file:
   ```bash
   GITHUB_TOKEN_TELLENAI=your_updated_tellenai_token_here
   GITHUB_TOKEN_THEDOCTORJJ=your_updated_thedoctorjj_token_here
   DEFAULT_GITHUB_ORG=thedoctorJJ
   ENDCAP_API_URL=http://localhost:8000
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
   ```

### **Step 3: Test the Setup**
1. Restart Devin AI to pick up the new MCP configuration
2. Use the simple startup prompt:
   ```
   Use MCP tool: get_startup_guide
   ```
3. Then check for available PRDs:
   ```
   Use MCP tool: check_available_prds
   ```

---

## 🔍 **Alternative: HTTP MCP Server (If stdio fails)**

If you continue having issues with the stdio MCP server:

1. **Start HTTP MCP Server**:
   ```bash
   cd /Users/jason/Repositories/ai-agent-factory/scripts/mcp
   python3 mcp-http-server.py
   ```

2. **Update Devin Config** to use HTTP transport:
   ```json
   {
     "transport": "http",
     "url": "http://localhost:8001"
   }
   ```

---

## 📊 **Current System Status**

- ✅ **Backend**: Running and connected to Supabase
- ✅ **Data Persistence**: PRDs persist after restarts
- ✅ **MCP Loading**: Working perfectly
- ✅ **UI**: Loading states and error handling added
- 🔧 **GitHub Tokens**: Need permission updates
- 🔧 **MCP Config**: Need path update in Devin

---

## 🎯 **Expected Workflow After Fix**

1. **Devin starts** → calls `get_startup_guide`
2. **Gets mission** → calls `check_available_prds`
3. **Finds PRD** → calls `get_prd_details`
4. **Creates repo** → calls `create_github_repository` (with proper permissions)
5. **Implements agent** → writes code to the repository
6. **Deploys** → updates agent status

---

## 📞 **Need Help?**

- **Detailed Setup Guide**: `docs/setup/15-devin-mcp-real-integration.md`
- **GitHub Token Guide**: `scripts/mcp/GITHUB_TOKEN_SETUP.md`
- **Setup Script**: `scripts/mcp/setup-devin-mcp.sh`

The system is ready - just need the GitHub token permissions updated! 🚀
