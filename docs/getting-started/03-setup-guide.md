# AI Agent Factory - Setup Guide

## 📋 **Document Summary**

This comprehensive setup guide walks through installing and configuring the AI Agent Factory platform, covering prerequisites (Python 3.11+, Node.js 18+, Docker), quick start instructions, required accounts and services (Supabase, Google Cloud, GitHub, OpenAI, Devin AI), detailed setup procedures for each service including API key configuration and database setup, environment configuration with the environment manager script, testing procedures to validate the setup, production deployment steps, security best practices for credential management, and a production checklist to ensure everything is working correctly.

---

## 🎯 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Supabase account
- OpenAI API key
- GitHub account with Personal Access Tokens

### **1. Clone and Setup**
```bash
git clone https://github.com/thedoctorJJ/ai-agent-factory.git
cd ai-agent-factory
./scripts/setup/dev-setup.sh
```

### **2. Configure Environment**
```bash
# Initialize environment configuration
./scripts/config/env-manager.sh init

# Edit the generated config/env/.env.local with your actual values
```

### **3. Start Development**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn fastapi_app.main:app --reload

# Terminal 2: Frontend  
cd frontend/next-app
npm run dev
```

### **4. Access the Platform**
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 **Required Accounts & Services**

### **Core Platform Services**
- [ ] **Supabase** - Database, Auth, Storage, Edge Functions
- [ ] **Google Cloud Platform** - Hosting, Storage, Secret Manager
- [ ] **GitHub** - Repository management, GitHub App
- [ ] **OpenAI** - GPT-5, Whisper for voice processing
- [ ] **Devin AI** - Autonomous agent orchestration and code generation

### **Optional/Advanced Services**
- [ ] **Sentry** - Error monitoring and logging
- [ ] **Slack** - Notifications and alerts
- [ ] **Vercel** - Alternative frontend hosting
- [ ] **Railway** - Alternative backend hosting

## 🗄️ **Supabase Setup**

### **Create Supabase Project**
1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Choose organization and enter:
   - **Name**: `ai-agent-factory`
   - **Database Password**: Generate strong password (save it!)
   - **Region**: Choose closest to your users
5. Wait for project creation (2-3 minutes)

### **Get API Keys**
1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon Key**: `your-supabase-key`
   - **Service Role Key**: `your-supabase-key`

### **Database Setup**
1. Go to **SQL Editor**
2. Run the schema from `infra/database/schema.sql`
3. Verify tables are created successfully

## ☁️ **Google Cloud Setup**

### **Create Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable required APIs:
   - Cloud Run API
   - Cloud Build API
   - Secret Manager API
   - Cloud Storage API

### **Service Account Setup**
1. Go to **IAM & Admin** → **Service Accounts**
2. Create new service account:
   - **Name**: `ai-agent-factory-service`
   - **Description**: Service account for AI Agent Factory
3. Grant roles:
   - Cloud Run Admin
   - Cloud Build Editor
   - Secret Manager Admin
   - Storage Admin
4. Create and download JSON key file
5. Save as `config/google-cloud-service-account.json`

### **Deploy MCP Server**
```bash
# Deploy HTTP MCP server to Cloud Run
./scripts/deployment/deploy-mcp-server-http.sh
```

## 🐙 **GitHub Setup**

### **Personal Access Token**
1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens**
2. Generate new token with scopes:
   - `repo` - Full control of repositories
   - `admin:org` - Full control of organizations
   - `workflow` - Update GitHub Action workflows
3. Save token securely

### **Multi-Token Configuration**
For multiple organizations, configure tokens in `scripts/mcp/.env`:
```bash
# GitHub Multi-Token Configuration
GITHUB_TOKEN_TELLENAI=your-github-token
GITHUB_TOKEN_THEDOCTORJJ=your-github-token
DEFAULT_GITHUB_ORG=thedoctorJJ
```

## 🤖 **OpenAI Setup**

### **API Key**
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Navigate to **API Keys**
3. Create new secret key
4. Save key securely

### **Usage Limits**
- Set appropriate usage limits
- Monitor usage in OpenAI dashboard
- Configure billing alerts

## 🔧 **Environment Configuration**

### **Environment Files**
- **`config/env.example`** - Template with all required variables
- **`config/env/.env.local`** - Your local environment (DO NOT COMMIT)
- **`config/env/.env.backup.*`** - Automatic backups of your configuration

### **Environment Manager Script**
```bash
# Initialize new environment
./scripts/config/env-manager.sh init

# Create backup
./scripts/config/env-manager.sh backup

# Restore from backup
./scripts/config/env-manager.sh restore

# List all environment files
./scripts/config/env-manager.sh list

# Clean old backups
./scripts/config/env-manager.sh clean
```

### **Required Environment Variables**
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/end_cap_agent_factory
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY=path/to/service-account-key.json

# GitHub Configuration
GITHUB_TOKEN=your-github-token

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Application Configuration
ENVIRONMENT=development
DEBUG=true
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 **Testing the Setup**

### **Configuration Validation**
```bash
# Validate all configuration
./scripts/config/validate-config.py
```

### **Test Supabase Connection**
```bash
# Test database connection
./scripts/setup/test-supabase-connection.py
```

### **Test MCP Server**
```bash
# Test MCP server functionality
./scripts/testing/test-mcp-server.sh
```

### **Create Sample PRDs**
```bash
# Populate system with test PRDs
python scripts/create-sample-prds.py
```

## 🚀 **Production Deployment**

### **Google Cloud Run Deployment**
```bash
# Deploy backend to Cloud Run
./scripts/setup-google-cloud-run.sh

# Deploy frontend to Cloud Run
cd frontend/next-app
gcloud run deploy ai-agent-factory-frontend --source .
```

### **Environment Variables for Production**
- Set all environment variables in Cloud Run
- Use Secret Manager for sensitive data
- Configure proper CORS origins
- Set up monitoring and alerting

## 🔒 **Security Best Practices**

### **Credential Management**
- Never commit sensitive files to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use least-privilege access principles

### **Protected File Patterns**
The following file patterns are automatically excluded from git:
- `.env*` - All environment files
- `*.pem` - Private key files
- `*-key.json` - Service account keys
- `*service-account*.json` - Google Cloud credentials
- `.env.backup*` - Backup files with sensitive data

### **Security Tools**
- **Pre-commit hook**: Prevents sensitive files from being committed
- **Secure commit script**: `./scripts/setup/secure-commit.sh "Your message"`
- **Environment manager**: Safe configuration management
- **Configuration validation**: Real-time config validation

## 🎉 **Ready to Go!**

Your AI Agent Factory is **fully configured** and ready for development:
- ✅ **All APIs configured** (Supabase, OpenAI, Google Cloud, GitHub)
- ✅ **Devin AI integration** with MCP server setup
- ✅ **GitHub token validated** and working correctly
- ✅ **MCP server functional** - Creates repositories automatically
- ✅ **Configuration validated** (8/8 checks passing)
- ✅ **Development environment ready**

**Start creating agents** - no additional setup required!
