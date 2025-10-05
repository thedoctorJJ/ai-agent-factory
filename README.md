# END_CAP Agent Factory

Welcome to the **END_CAP Agent Factory** — a repeatable, voice-first, AI-driven platform for creating modular agents with fully automated orchestration and deployment.

This repository contains all core infrastructure, libraries, and documentation to build, orchestrate, and deploy AI agents efficiently.

---

## 📚 Documentation

### 1. Core Platform
- [Infrastructure Blueprint](./docs/01-infrastructure-blueprint.md) — folder structure, frontend/backend setup, hosting, AI core, and key principles.
- [DevOps & Deployment Flow](./docs/02-devops-deployment-flow.md) — local dev, CI/CD, monitoring, and rollback.
- [Agent Lifecycle Framework](./docs/03-agent-lifecycle-framework.md) — lifecycle stages, metadata, versioning, and governance.

### 2. Specialized Integration
- [Devin AI Integration Framework](./docs/04-devin-ai-integration.md) — autonomous agent orchestration and execution.
- [Voice-Driven Workflow Design](./docs/05-voice-driven-workflow.md) — end-to-end PRD creation via voice or text.
- [UI Integration & Transition Layer](./docs/06-ui-integration.md) — Next.js + shadcn dashboard for monitoring and execution.
- [GitHub MCP Service](./docs/07-github-mcp-service.md) — automated repository creation for each new PRD.
- [OpenAI Voice Workflow](./docs/11-openai-voice-workflow.md) — complete voice-to-agent workflow via ChatGPT/OpenAI.

### 3. Supporting / Visualization
- [Platform Architecture Diagram](./docs/08-platform-architecture-diagram.md) — full architecture overview, data flow, and component interaction.
- [Accounts and APIs Setup Guide](./docs/09-accounts-and-apis-setup.md) — complete guide for setting up all required accounts and APIs.
- [MCP Server Setup Guide](./docs/13-mcp-server-setup-guide.md) — step-by-step guide for configuring the OpenAI MCP server in Devin AI.
- [Unified MCP Setup Guide](./docs/14-unified-mcp-setup.md) — complete guide for the unified MCP server configuration.

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### 1. Clone and Setup
```bash
git clone https://github.com/thedoctorJJ/end-cap-agent-factory.git
cd end-cap-agent-factory
./scripts/dev-setup.sh
```

### 2. Configure Environment
```bash
cp env.example .env
# Edit .env with your actual configuration values
# See SETUP-CHECKLIST.md for detailed account setup
```

### 3. Start Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn fastapi_app.main:app --reload

# Terminal 2: Frontend  
cd frontend/next-app
npm run dev
```

### 4. Access the Platform
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **HTTP MCP Server**: https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app
  - **Health Check**: `/health`
  - **Tools List**: `/tools`
  - **MCP Protocol**: `/mcp` (JSON-RPC 2.0)

## 🎉 **Ready to Go!**

Your END_CAP Agent Factory is **fully configured** and ready for development:
- ✅ **All APIs configured** (Supabase, OpenAI, Google Cloud, GitHub)
- ✅ **Devin AI integration** with MCP server setup
- ✅ **OpenAI voice workflow** - Create agents through ChatGPT conversations
- ✅ **GitHub token validated** and working correctly
- ✅ **MCP server functional** - Creates repositories automatically
- ✅ **HTTP MCP Server deployed** - Publicly accessible at `https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app`
- ✅ **Configuration validated** (15/15 checks passing)
- ✅ **Development environment ready**

**Start creating agents through voice conversations** - no additional setup required!

## 🔒 Security & Credentials Management

### **Important Security Notes**
- **Never commit sensitive files** to version control
- **All credential files are automatically ignored** by git
- **Use environment variables** for all sensitive data
- **Backup files with credentials are excluded** from commits

### **Protected File Patterns**
The following file patterns are automatically excluded from git:
- `.env*` - All environment files
- `*.pem` - Private key files
- `*-key.json` - Service account keys
- `*service-account*.json` - Google Cloud credentials
- `.env.backup*` - Backup files with sensitive data
- `*api-key*`, `*secret*`, `*token*` - Any files with sensitive names

### **Safe Development Workflow**
1. **Copy `env.example` to `.env`** - This is safe to do
2. **Add your credentials to `.env`** - This file is gitignored
3. **Run configuration scripts** - They create backups automatically
4. **Use secure commit tools** - Prevents accidental credential commits
5. **Commit only code changes** - Credentials stay local

### **Security Tools**
- **Pre-commit hook**: Automatically prevents sensitive files from being committed
- **Secure commit script**: `./scripts/secure-commit.sh "Your message"`
- **Install security hook**: `./scripts/install-pre-commit-hook.sh`

### **If You Accidentally Commit Sensitive Files**
```bash
# Remove from git history (if caught early)
git reset --soft HEAD~1
git reset HEAD <sensitive-file>
git commit -m "Your commit message"

# Or use git filter-branch for deeper cleanup
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch <sensitive-file>' \
  --prune-empty --tag-name-filter cat -- --all
```

## 🏗️ Architecture

### Backend (FastAPI)
- **API Endpoints**: `/api/v1/agents`, `/api/v1/prds`, `/api/v1/health`, `/api/v1/devin`
- **Models**: Pydantic models for agents and PRDs
- **Database**: Supabase integration ready
- **Devin AI Integration**: MCP server for automated deployment
- **HTTP MCP Server**: Publicly deployed FastAPI server for external integrations
- **Authentication**: JWT-based auth system

### Frontend (Next.js 14)
- **Dashboard**: Agent and PRD management interface
- **Devin AI Tab**: Copy-paste workflow for agent creation
- **Components**: shadcn/ui component library
- **Styling**: Tailwind CSS with dark mode support
- **State Management**: React hooks and context

### Infrastructure
- **Local Development**: Docker Compose with PostgreSQL & Redis
- **Production**: Google Cloud Run deployment
- **Database**: Supabase for production, PostgreSQL for local
- **MCP Server**: HTTP-based server deployed to Google Cloud Run
- **Monitoring**: Integrated logging and health checks

---

## 🧩 Principles

* **Modular & Repeatable**: Every new agent follows the same lifecycle.
* **Voice-First & Automated**: PRDs can be created via voice, auto-triggering pipelines.
* **Auditable & Governed**: Supabase tracks metadata, logs, and version history.
* **Integration Ready**: Frontend, backend, and libraries are plug-and-play.

---

## 📊 Project Status

### ✅ Completed
- [x] Complete project scaffolding
- [x] FastAPI backend with agents & PRDs API
- [x] Next.js frontend with dashboard
- [x] Docker development environment
- [x] Infrastructure configuration
- [x] Documentation suite
- [x] Development setup automation
- [x] **Supabase integration** - Database, auth, and storage configured
- [x] **OpenAI integration** - API key validated and working
- [x] **Google Cloud setup** - Project, APIs, and service account ready
- [x] **GitHub App configuration** - Repository management ready
- [x] **Devin AI integration** - MCP server for automated deployment
- [x] **GitHub token validation** - Personal access token working correctly
- [x] **MCP server testing** - Repository creation and deployment simulation working
- [x] **HTTP MCP Server deployment** - Publicly accessible server on Google Cloud Run

### 🚧 In Progress
- [ ] Voice input processing implementation
- [ ] Advanced agent orchestration features
- [ ] Production deployment to Google Cloud Run

### 📋 Next Steps
1. ✅ **Set up accounts and APIs** - Complete! All services configured
2. ✅ **Validate configuration** - All validations passing
3. **Start development** - Platform is ready to run
4. Implement voice-to-PRD conversion
5. Build GitHub MCP service for repo creation
6. Integrate Devin AI for agent orchestration
7. Deploy to Google Cloud Run

## 🔗 Contacts / Contributors

* **Lead Architect**: JJ
* **Platform AI**: Devin AI
* **Repository**: [thedoctorJJ/end-cap-agent-factory](https://github.com/thedoctorJJ/end-cap-agent-factory)
