# Unified MCP Server Setup Guide

Your AI Agent Factory Agent Factory now has a **single unified MCP server** that handles the complete voice-to-agent workflow!

## 🎯 **What You Have Now**

### **Single MCP Server with 9 Tools:**

#### **OpenAI Integration Tools:**
- `create_prd_from_conversation` - Extract PRDs from ChatGPT conversations
- `deliver_prd_to_endcap` - Deliver PRDs to your platform
- `trigger_devin_workflow` - Generate Devin AI prompts
- `get_endcap_status` - Check platform health

#### **Deployment Tools:**
- `create_agent` - Create GitHub repositories
- `deploy_agent` - Deploy to Google Cloud Run
- `setup_database` - Set up Supabase tables
- `create_repository` - GitHub repo creation
- `get_repository_info` - Get repository details

## 🚀 **Configure in Devin AI**

### **Step 1: Update Your Existing MCP Server**

1. **Go to Devin AI** → MCP Marketplace
2. **Find your existing** "AI Agent Factory Agent Factory" MCP server
3. **Click "Edit"** to update it

### **Step 2: Add New Secrets**

Add these new secrets to your existing MCP server:

```
OPENAI_API_KEY: [Your OpenAI API Key]
ENDCAP_API_URL: http://localhost:8000
```

### **Step 3: Update Server Path**

Make sure your server path is:
```
Command: python3
Arguments: /Users/jason/Repositories/end-cap-agent-factory/scripts/mcp-server.py
```

### **Step 4: Test All Tools**

Click **"Test listing tools"** - you should now see **9 tools** instead of 4:
- create_agent
- deploy_agent
- setup_database
- create_repository
- get_repository_info
- create_prd_from_conversation
- deliver_prd_to_endcap
- trigger_devin_workflow
- get_endcap_status

## 🎉 **Complete Workflow**

### **Voice-to-Agent in 4 Steps:**

1. **Start conversation** in ChatGPT/OpenAI
2. **Use `create_prd_from_conversation`** to extract PRD
3. **Use `deliver_prd_to_endcap`** to create Devin AI task
4. **Use `trigger_devin_workflow`** to get deployment prompt
5. **Copy prompt to Devin AI** - it will use your deployment tools automatically

### **Example Usage:**

```
1. create_prd_from_conversation({
   "conversation": "I need an email marketing agent...",
   "agent_type": "email"
})

2. deliver_prd_to_endcap({
   "prd": [extracted PRD data]
})

3. trigger_devin_workflow({
   "task_id": [task ID from step 2]
})
```

## ✅ **Benefits of Unified Server**

- **Single configuration** to manage
- **Complete workflow** in one place
- **All tools available** to Devin AI
- **Easier maintenance** and updates
- **Seamless integration** between OpenAI and deployment

## 🎯 **Ready to Use**

Your unified MCP server is now ready! You can:

1. **Create agents through voice** conversations in ChatGPT
2. **Automatically deploy** them through Devin AI
3. **Monitor everything** in your AI Agent Factory dashboard

**The complete voice-to-agent workflow is now operational!** 🚀
