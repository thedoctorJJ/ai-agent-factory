# ChatGPT PRD Delivery via MCP Server

## ✅ What's Already Set Up

The MCP HTTP server has a webhook endpoint that receives PRDs from ChatGPT and delivers them to the agent factory:

**Endpoint**: `POST /api/v1/prds/incoming`

## 🌐 Production URL

Once deployed, ChatGPT can call:
```
https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/api/v1/prds/incoming
```

## 📋 How It Works

1. **ChatGPT** → Sends PRD to MCP server endpoint
2. **MCP Server** → Receives PRD and processes it
3. **MCP Server** → Forwards to agent factory backend
4. **Agent Factory** → Stores PRD in database

## 🔧 Request Format

```json
POST /api/v1/prds/incoming
Content-Type: application/json

{
  "content": "# PRD Title\n\n## Description\n..."
}
```

## 🚀 Next Steps

1. **Deploy the MCP server** to Google Cloud Run (if not already deployed)
2. **Get the public HTTPS URL** of the deployed MCP server
3. **Configure ChatGPT** to use this URL (via webhook, custom integration, or manual copy-paste)

## 💡 Alternative: Use MCP Tools in Cursor

If you can't configure ChatGPT to call the endpoint directly, you can:

1. Copy PRD content from ChatGPT
2. Use Cursor's MCP tools: `submit_prd_from_conversation`
3. The MCP server will deliver it to the agent factory

## 🧪 Test the Endpoint

```bash
curl -X POST https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/json" \
  -d '{"content": "# Test PRD\n\n## Description\nTest PRD from ChatGPT"}'
```



