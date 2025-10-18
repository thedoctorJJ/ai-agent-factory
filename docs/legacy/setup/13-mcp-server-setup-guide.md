# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[03 - Setup Guide](../../03-setup-guide.md)** — Current setup documentation
> 
> **This file is preserved for historical reference only.**

---

# MCP Server Setup Guide for Devin AI

This guide will walk you through setting up the OpenAI MCP Server in Devin AI to enable the complete voice-to-agent workflow.

## 🎯 **What This Enables**

With this MCP server configured, you can:
1. **Create agents through voice conversations** in ChatGPT/OpenAI
2. **Automatically deliver PRDs** to your AI Agent Factory Agent Factory
3. **Trigger Devin AI deployment** with optimized prompts
4. **Complete the full workflow** from conversation to deployed agent

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Access Devin AI MCP Marketplace**

1. **Log into Devin AI**
2. **Navigate to**: Organization Settings → MCP Marketplace
3. **Click**: "+ Configure MCP server" or "Add Custom Server"

### **Step 2: Basic Configuration**

Fill out the MCP server configuration form:

```
Server Name: AI Agent Factory Agent Factory - OpenAI Integration
Transport Type: STDIO
Icon: 🤖
Description: Automatically delivers PRDs from ChatGPT/OpenAI conversations to AI Agent Factory Agent Factory and triggers Devin AI deployment workflow.
Enabled: ✅ (toggle ON)
```

### **Step 3: Add Required Secrets**

Click **"+ Add a new secret"** for each of the following:

#### **Secret 1: OpenAI API Key**
```
Name: OPENAI_API_KEY
Value: [Your OpenAI API Key]
Description: OpenAI API key for ChatGPT integration
```

#### **Secret 2: AI Agent Factory API URL**
```
Name: ENDCAP_API_URL
Value: http://localhost:8000
Description: AI Agent Factory Agent Factory API URL
```

### **Step 4: STDIO Configuration**

Configure how Devin AI will execute your MCP server:

```
Command: python3
Arguments: /Users/jason/Repositories/ai-agent-factory/scripts/openai-mcp-server.py
```

**Note**: Ensure the path is correct for your system. If Devin AI runs in a container, you may need to adjust the path.

### **Step 5: Save and Test**

1. **Click "Save changes"**
2. **Click "Test listing tools"** to verify the server is working
3. **You should see these tools**:
   - `submit_prd_for_agent_creation`
   - `deliver_prd_to_endcap`
   - `trigger_devin_workflow`
   - `get_endcap_status`
4. **Click "▷ Use MCP"** to enable it

---

## 🧪 **Testing the Setup**

### **Test 1: Check AI Agent Factory Status**
```json
{
  "method": "get_endcap_status"
}
```

**Expected Response**:
```json
{
  "success": true,
  "status": "healthy",
  "endcap_version": "1.0.0",
  "environment": "development",
  "message": "AI Agent Factory Agent Factory is running and ready"
}
```

### **Test 2: Submit PRD for Agent Creation**
```json
{
  "method": "submit_prd_for_agent_creation",
  "params": {
    "conversation": "I need an email marketing agent that can send personalized campaigns and track open rates.",
    "agent_type": "email"
  }
}
```

### **Test 3: Complete Workflow**
```json
{
  "method": "deliver_prd_to_endcap",
  "params": {
    "prd": {
      "title": "Email Marketing Agent",
      "description": "AI agent for personalized email campaigns",
      "requirements": ["Send personalized emails", "Track open rates", "Segment customers"],
      "agent_type": "email"
    }
  }
}
```

---

## 🎉 **Using the Complete Workflow**

### **1. Start a Conversation in ChatGPT/OpenAI**
```
User: "I need a customer support agent that can answer common questions and escalate complex issues."

ChatGPT: "I'll help you create a customer support agent. Let me break this down into requirements..."
```

### **2. MCP Server Automatically**
- **Extracts the PRD** from your conversation
- **Delivers it to AI Agent Factory** via API
- **Creates a Devin AI task** with optimized prompts

### **3. Devin AI Deployment**
- **Copy the generated prompt** to Devin AI
- **Devin AI automatically**:
  - Creates GitHub repository
  - Sets up Supabase database
  - Deploys to Google Cloud Run
  - Integrates with your platform

### **4. Agent Ready**
- **Agent appears** in your AI Agent Factory dashboard
- **Monitor performance** and usage
- **Iterate and improve** as needed

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. "Connection refused" Error**
- **Check**: AI Agent Factory Agent Factory is running (`http://localhost:8000`)
- **Start**: `cd backend && PYTHONPATH=. python3 -m uvicorn fastapi_app.main:app --reload --port 8000`

#### **2. "Module not found" Error**
- **Check**: Python path is correct in STDIO configuration
- **Verify**: The MCP server script exists at the specified path

#### **3. "Invalid API key" Error**
- **Check**: OpenAI API key is correct and has sufficient credits
- **Verify**: Secret is properly configured in Devin AI

#### **4. "Tool not found" Error**
- **Check**: MCP server is enabled in Devin AI
- **Verify**: All tools are listed when testing

### **Debug Commands**

```bash
# Test MCP server locally
echo '{"method": "get_endcap_status"}' | python3 scripts/openai-mcp-server.py

# Check AI Agent Factory API
curl http://localhost:8000/api/v1/health

# Verify environment variables
grep -E "OPENAI_API_KEY|ENDCAP_API_URL" .env
```

---

## 🎯 **Next Steps**

Once your MCP server is configured:

1. **Test the complete workflow** with a simple agent idea
2. **Create your first agent** through voice conversation
3. **Monitor the deployment** in your AI Agent Factory dashboard
4. **Iterate and improve** your agent creation process

**Your voice-to-agent workflow is now ready!** 🚀

---

## 📚 **Additional Resources**

- [OpenAI Voice Workflow Documentation](./11-openai-voice-workflow.md)
- [Complete Workflow Diagram](./12-workflow-diagram.md)
- [AI Agent Factory Agent Factory README](../README.md)
- [Devin AI MCP Documentation](https://docs.devin.ai/mcp)
