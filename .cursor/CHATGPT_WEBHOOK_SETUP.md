# ChatGPT PRD Delivery via MCP Server - Webhook Setup

## 🎯 Overview

Since you're not using ChatGPT Actions, we'll set up a simple webhook endpoint that ChatGPT can call to deliver PRDs through the MCP server to the agent factory.

## 🔧 Setup Options

### Option 1: Direct HTTP Endpoint (Recommended)

The MCP HTTP server now has an endpoint at:
```
POST https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/api/v1/prds/incoming
```

**Request Format:**
```json
{
  "content": "# PRD Title\n\n## Description\n..."
}
```

### Option 2: Use MCP Server Tools via Cursor

You can use the MCP server tools in Cursor to submit PRDs from ChatGPT conversations:

1. Copy the PRD content from ChatGPT
2. Use Cursor's MCP tools: `submit_prd_from_conversation`
3. The MCP server will deliver it to the agent factory

## 📋 Next Steps

1. **Deploy the updated MCP server** with the ChatGPT endpoint
2. **Test the endpoint** to ensure it works
3. **Configure ChatGPT** to use the webhook URL (if using a custom integration)

## 🚀 Quick Test

Test the endpoint:
```bash
curl -X POST https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app/api/v1/prds/incoming \
  -H "Content-Type: application/json" \
  -d '{"content": "# Test PRD\n\n## Description\nTest PRD from ChatGPT"}'
```



