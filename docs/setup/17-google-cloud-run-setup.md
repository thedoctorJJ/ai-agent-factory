# 🚀 Google Cloud Run Setup for AI Agent Factory

## ✅ **Solution: Google Cloud Run Instead of Fly.io**

You're absolutely right! Google Cloud Run is a much better choice than Fly.io for your AI Agent Factory. Here's why:

- ✅ **No credit card required** for basic usage
- ✅ **Better integration** with your existing Google Cloud setup
- ✅ **More control** over your deployments
- ✅ **Already configured** in your project

## 🔧 **What's Been Set Up**

I've configured your AI Agent Factory to use **Google Cloud Run** instead of Fly.io:

### 1. **Google Cloud Run Deployer**
- Created `scripts/mcp/google-cloud-run-deploy.py`
- Handles building and deploying agents to Google Cloud Run
- Uses your existing service account: `agent-factory-474201`

### 2. **Updated MCP Server**
- Added `deploy_to_google_cloud_run` tool to the MCP server
- Devin can now deploy agents directly to Google Cloud Run
- No more Fly.io dependency!

### 3. **Redis Setup**
- Created `scripts/mcp/google-cloud-redis-setup.py`
- Can create Redis instances on Google Cloud Memorystore
- Alternative to Fly.io Redis

## 🎯 **For Devin AI**

### **New MCP Tool Available:**
```
deploy_to_google_cloud_run
```

**Parameters:**
- `agent_name`: Name for the agent
- `agent_code`: Python FastAPI code
- `requirements`: Additional Python packages (optional)
- `environment_variables`: Environment variables (optional)

### **Example Usage:**
```json
{
  "name": "deploy_to_google_cloud_run",
  "arguments": {
    "agent_name": "redis-caching-layer",
    "agent_code": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef read_root():\n    return {'message': 'Hello from Google Cloud Run!'}",
    "requirements": ["redis==5.0.1"],
    "environment_variables": {
      "REDIS_URL": "redis://your-redis-host:6379"
    }
  }
}
```

## 🔐 **Credentials for Devin**

Share these with Devin AI:

```
GOOGLE_CLOUD_PROJECT_ID=agent-factory-474201
GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY=config/google-cloud-service-account.json
GOOGLE_CLOUD_REGION=us-central1
```

## 🚀 **Quick Setup**

Run this to test Google Cloud Run:

```bash
cd /Users/jason/Repositories/ai-agent-factory
./scripts/setup-google-cloud-run.sh
```

## 📋 **What Devin Should Do**

1. **Use the new MCP tool** `deploy_to_google_cloud_run` instead of Fly.io
2. **Deploy the Redis Caching Layer Agent** to Google Cloud Run
3. **Set up Redis** using Google Cloud Memorystore or Upstash
4. **Update the agent status** with the new deployment URL

## 🎉 **Benefits**

- ✅ **No credit card required**
- ✅ **Better performance** (Google Cloud infrastructure)
- ✅ **Easier management** (same project as your other services)
- ✅ **More reliable** (Google's global infrastructure)
- ✅ **Cost effective** (pay only for what you use)

## 🔄 **Migration from Fly.io**

The existing Redis Caching Layer Agent can be easily migrated:

1. **Get the current code** from the Fly.io deployment
2. **Use the new MCP tool** to deploy to Google Cloud Run
3. **Update the agent record** with the new URL
4. **Set up Redis** on Google Cloud or Upstash

## 📞 **Next Steps**

1. **Share the credentials** with Devin AI
2. **Let Devin know** to use `deploy_to_google_cloud_run` instead of Fly.io
3. **Devin will complete** the Redis Caching Layer Agent setup
4. **Enjoy** your fully functional AI Agent Factory! 🚀

---

**Ready to go!** Devin can now deploy agents to Google Cloud Run without any credit card requirements. 🎯
