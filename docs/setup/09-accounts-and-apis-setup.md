# Accounts and APIs Setup Guide

This guide walks you through setting up all the necessary accounts, APIs, and MCP servers for the AI Agent Factory Agent Factory.

## 📋 Required Accounts & Services

### ✅ Core Platform Services
- [ ] **Supabase** - Database, Auth, Storage, Edge Functions
- [ ] **Google Cloud Platform** - Hosting, Storage, Secret Manager
- [ ] **GitHub** - Repository management, GitHub App
- [ ] **OpenAI** - GPT-5, Whisper for voice processing
- [ ] **Devin AI** - Autonomous agent orchestration and code generation

### ✅ Optional/Advanced Services
- [ ] **Sentry** - Error monitoring and logging
- [ ] **Slack** - Notifications and alerts
- [ ] **Vercel** - Alternative frontend hosting
- [ ] **Railway** - Alternative backend hosting

---

## 🗄️ 1. Supabase Setup

### Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Choose organization and enter:
   - **Name**: `end-cap-agent-factory`
   - **Database Password**: Generate strong password (save it!)
   - **Region**: Choose closest to your users
5. Wait for project creation (2-3 minutes)

### Get API Keys
1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Database Setup
1. Go to **SQL Editor**
2. Run the following schema:

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Agents table
CREATE TABLE agents (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    purpose TEXT NOT NULL,
    tools JSONB DEFAULT '[]',
    prompts JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'created',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- PRDs table
CREATE TABLE prds (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    requirements JSONB DEFAULT '[]',
    voice_input TEXT,
    text_input TEXT,
    status VARCHAR(50) DEFAULT 'submitted',
    github_repo_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent executions table
CREATE TABLE agent_executions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    agent_id UUID REFERENCES agents(id),
    prd_id UUID REFERENCES prds(id),
    status VARCHAR(50) DEFAULT 'pending',
    logs JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_prds_status ON prds(status);
CREATE INDEX idx_agent_executions_agent_id ON agent_executions(agent_id);
```

### Authentication Setup
1. Go to **Authentication** → **Settings**
2. Configure **Site URL**: `http://localhost:3000` (for development)
3. Add **Redirect URLs**:
   - `http://localhost:3000/auth/callback`
   - `https://your-domain.com/auth/callback`

### Storage Setup
1. Go to **Storage**
2. Create buckets:
   - **prd-documents** (private)
   - **agent-assets** (public)

---

## ☁️ 2. Google Cloud Platform Setup

### Create GCP Project
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Enter:
   - **Project name**: `end-cap-agent-factory`
   - **Organization**: Select your org (if applicable)
4. Click "Create"

### Enable Required APIs
1. Go to **APIs & Services** → **Library**
2. Enable these APIs:
   - **Cloud Run API**
   - **Cloud Build API**
   - **Container Registry API**
   - **Secret Manager API**
   - **Cloud Logging API**
   - **Cloud Monitoring API**

### Create Service Account
1. Go to **IAM & Admin** → **Service Accounts**
2. Click "Create Service Account"
3. Enter:
   - **Name**: `modular-ai-platform-sa`
   - **Description**: `Service account for Modular AI Agent Platform`
4. Grant roles:
   - **Cloud Run Admin**
   - **Cloud Build Editor**
   - **Storage Admin**
   - **Secret Manager Admin**
5. Create and download JSON key file

### Set up Secret Manager
1. Go to **Security** → **Secret Manager**
2. Create secrets:
   - **database-url**: Your Supabase database URL
   - **supabase-service-role-key**: Your Supabase service role key
   - **github-app-private-key**: GitHub App private key
   - **openai-api-key**: Your OpenAI API key

### Configure Cloud Run
1. Go to **Cloud Run**
2. Note the default region (usually `us-central1`)
3. This will be used in your deployment configuration

---

## 🐙 3. GitHub Setup

### Create GitHub App
1. Go to your GitHub organization settings
2. Click **Developer settings** → **GitHub Apps**
3. Click **New GitHub App**
4. Fill in:
   - **GitHub App name**: `Modular AI Agent Platform`
   - **Homepage URL**: `https://your-domain.com`
   - **Webhook URL**: `https://your-mcp-service.com/webhook`
   - **Webhook secret**: Generate and save securely

### App Permissions
Set these permissions:
- **Repository permissions**:
  - Contents: Read & Write
  - Metadata: Read
  - Pull requests: Read & Write
  - Issues: Read & Write
- **Organization permissions**:
  - Members: Read
- **Subscribe to events**:
  - Repository
  - Pull request
  - Issues

### Generate Private Key
1. Scroll to **Private keys**
2. Click **Generate a private key**
3. Download the `.pem` file
4. Save securely (you'll need this for MCP service)

### Install App
1. Go to **Install App**
2. Install on your organization
3. Note the **App ID** (you'll need this)

---

## 🤖 4. OpenAI Setup

### Create OpenAI Account
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up/Login
3. Add payment method (required for API access)

### Get API Key
1. Go to **API Keys**
2. Click **Create new secret key**
3. Name it: `modular-ai-platform`
4. Copy and save securely

### Set Usage Limits
1. Go to **Usage limits**
2. Set appropriate limits for your usage
3. Monitor usage in **Usage** tab

---

## 🤖 5. Devin AI Setup

### Create Devin AI Account
1. **Visit**: [devin.ai](https://devin.ai) or [cognition.ai](https://cognition.ai)
2. **Request Access**: Sign up for the waitlist or request early access
3. **Wait for Approval**: Devin AI is currently in private beta

### Get API Key (if available)
1. **Go to your Devin AI dashboard** (once you have access)
2. **Look for API settings** or **Developer section**
3. **Generate API key** (if available)

### Devin AI Configuration
```env
DEVIN_AI_API_KEY=your-devin-ai-api-key
DEVIN_AI_BASE_URL=https://api.devin.ai
DEVIN_AI_MODEL=devin-ai
DEVIN_AI_TIMEOUT=300
```

### Note on Devin AI Access
- **Currently in private beta** - limited access
- **API may not be publicly available yet**
- **Alternative**: Use other AI orchestration tools until Devin AI is available
- **Future integration**: Will be fully integrated once API is available

---

## 🔧 6. MCP Server Setup

### GitHub MCP Service
The MCP (Model Context Protocol) service will handle GitHub repository creation.

#### Create MCP Service Repository
1. Create new repository: `modular-ai-mcp-service`
2. Clone and set up basic FastAPI service
3. Deploy to Google Cloud Run or similar

#### MCP Service Configuration
```python
# mcp_service_config.py
GITHUB_APP_ID = "your-github-app-id"
GITHUB_PRIVATE_KEY_PATH = "path/to/private-key.pem"
GITHUB_WEBHOOK_SECRET = "your-webhook-secret"
SUPABASE_URL = "your-supabase-url"
SUPABASE_SERVICE_KEY = "your-supabase-service-key"
```

---

## 🔐 6. Environment Configuration

### Update .env File
Copy your `env.example` to `.env` and fill in:

```env
# Database
DATABASE_URL=postgresql://postgres:your-password@db.your-project.supabase.co:5432/postgres

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY=path/to/service-account-key.json

# GitHub
GITHUB_APP_ID=your-github-app-id
GITHUB_PRIVATE_KEY=your-github-private-key
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_ORG_NAME=your-org-name

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## ✅ 7. Verification Checklist

### Test Supabase Connection
```bash
# Test database connection
curl -H "apikey: YOUR_ANON_KEY" \
     -H "Authorization: Bearer YOUR_ANON_KEY" \
     "https://your-project.supabase.co/rest/v1/agents"
```

### Test Google Cloud
```bash
# Test authentication
gcloud auth application-default login
gcloud config set project your-project-id
```

### Test GitHub App
```bash
# Test webhook endpoint
curl -X POST https://your-mcp-service.com/webhook \
     -H "Content-Type: application/json" \
     -d '{"test": "webhook"}'
```

### Test OpenAI
```bash
# Test API key
curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🚨 Security Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Monitor usage** and set up alerts
5. **Use least privilege** for service accounts
6. **Enable audit logging** where available

---

## 📞 Support & Troubleshooting

### Common Issues
- **Supabase connection**: Check URL and API keys
- **GitHub App**: Verify webhook URL and permissions
- **Google Cloud**: Ensure APIs are enabled and service account has permissions
- **OpenAI**: Check API key and billing status

### Getting Help
- **Supabase**: [docs.supabase.com](https://docs.supabase.com)
- **Google Cloud**: [cloud.google.com/docs](https://cloud.google.com/docs)
- **GitHub Apps**: [docs.github.com/en/apps](https://docs.github.com/en/apps)
- **OpenAI**: [platform.openai.com/docs](https://platform.openai.com/docs)
