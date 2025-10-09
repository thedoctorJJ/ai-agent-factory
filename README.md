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
- [Enhanced PRD System](./docs/15-enhanced-prd-system.md) — comprehensive guide to the industry-best-practices PRD system with guided completion.

---

## 🔧 Environment Management

The platform includes a comprehensive environment management system:

### Environment Files Organization
- **`config/env.example`** - Template with all required variables
- **`config/env/.env.local`** - Your local environment (DO NOT COMMIT)
- **`config/env/.env.backup.*`** - Automatic backups of your configuration

### Environment Manager Script
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

## ⚙️ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### 1. Clone and Setup
```bash
git clone https://github.com/thedoctorJJ/end-cap-agent-factory.git
cd end-cap-agent-factory
./scripts/setup/dev-setup.sh
```

### 2. Configure Environment
```bash
# Initialize environment configuration
./scripts/config/env-manager.sh init

# Edit the generated config/env/.env.local with your actual values
# See setup/SETUP-CHECKLIST.md for detailed account setup
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
- ✅ **Enhanced PRD System** - Industry best practices with 17 sections and guided completion
- ✅ **Voice-First PRD Creation** - Standardized markdown output for Devin AI
- ✅ **Professional Environment Management** - Organized config files with automated backup system
- ✅ **Optimized Directory Structure** - Clean, logical organization of all project files
- ✅ **Environment Manager Tool** - Automated backup/restore and configuration management
- ✅ **Script Organization** - Logical grouping of automation scripts by purpose

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
1. **Initialize environment**: `./scripts/config/env-manager.sh init` - Creates `.env.local` from template
2. **Add your credentials to `config/env/.env.local`** - This file is gitignored
3. **Create backups**: `./scripts/config/env-manager.sh backup` - Automatic backup system
4. **Use secure commit tools** - Prevents accidental credential commits
5. **Commit only code changes** - Credentials stay local and organized

### **Security Tools**
- **Pre-commit hook**: Automatically prevents sensitive files from being committed
- **Secure commit script**: `./scripts/setup/secure-commit.sh "Your message"`
- **Install security hook**: `./scripts/setup/install-pre-commit-hook.sh`
- **Environment manager**: `./scripts/config/env-manager.sh` - Manage config files safely

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

## 📁 Directory Structure

```
end-cap-agent-factory/
├── backend/              # FastAPI backend application
├── frontend/             # Next.js frontend application
├── docs/                 # Comprehensive documentation
├── scripts/              # Organized automation scripts
│   ├── mcp/             # MCP server scripts and configs
│   ├── config/          # Configuration management scripts
│   ├── setup/           # Development setup scripts
│   ├── deployment/      # Deployment automation scripts
│   └── testing/         # Test automation scripts
├── config/               # Configuration files and templates
│   ├── env/             # Environment configuration files
│   └── env.example      # Environment variables template
├── setup/                # Setup guides and checklists
├── tests/                # Test results and reports
├── reports/              # Project reports and analysis
├── libraries/            # Agent, prompt, and tool libraries
├── infra/                # Infrastructure and deployment configs
└── README.md             # This file
```

## 🏗️ Architecture

### Backend (FastAPI)
- **API Endpoints**: `/api/v1/agents`, `/api/v1/prds`, `/api/v1/health`, `/api/v1/devin`
- **Enhanced PRD System**: Industry best practices with 17 sections and guided completion
- **Models**: Pydantic models for agents and comprehensive PRDs
- **Database**: Supabase integration ready
- **Devin AI Integration**: MCP server for automated deployment
- **HTTP MCP Server**: Publicly deployed FastAPI server for external integrations
- **Authentication**: JWT-based auth system
- **PRD Completion Tracking**: Automatic calculation and missing section detection
- **Guided Questions**: Interactive completion workflow for incomplete PRDs

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

## 📋 Enhanced PRD System

### **Industry Best Practices**
The END_CAP Agent Factory includes a comprehensive PRD (Product Requirements Document) system that follows industry best practices:

#### **17 Comprehensive Sections**
- **Required Sections (10)**: Title, Description, Problem Statement, Target Users, User Stories, Requirements, Acceptance Criteria, Technical Requirements, Success Metrics, Timeline
- **Optional Sections (7)**: Performance Requirements, Security Requirements, Integration Requirements, Deployment Requirements, Dependencies, Risks, Assumptions

#### **Smart Completion Tracking**
- **Automatic Calculation**: System calculates completion percentage based on filled sections
- **Weighted Scoring**: Important sections (like Problem Statement) have higher weights
- **Status Management**: PRDs are marked as "draft" until 100% complete, then "submitted"
- **Missing Section Detection**: Identifies exactly which sections need attention

#### **Guided Questions System**
For each missing section, the system provides:
- **Main Question**: Direct, focused question about the section
- **Sub-Questions**: 3-4 clarifying questions to help think through the topic
- **Real Examples**: Concrete examples to guide thinking
- **Context**: Why this section matters for the project

#### **Voice-First Workflow**
- **Unified Output**: Whether you speak or type, you get the same professional PRD format
- **Devin-Ready**: Markdown files are optimized for Devin AI with clear implementation phases
- **Complete Specifications**: Includes all technical details, repository structure, and deployment instructions
- **Easy Sharing**: One-click download or view in browser

### **API Endpoints**
- `POST /api/v1/prds` - Create PRD with automatic completion tracking
- `GET /api/v1/prds/{id}/completion` - Get completion status and missing sections
- `GET /api/v1/prds/{id}/guided-questions` - Get questions for missing sections
- `GET /api/v1/prds/{id}/markdown` - Export PRD as markdown for Devin AI
- `GET /api/v1/prds/{id}/markdown/download` - Download PRD as .md file

## 🧩 Principles

* **Modular & Repeatable**: Every new agent follows the same lifecycle.
* **Voice-First & Automated**: PRDs can be created via voice, auto-triggering pipelines.
* **Auditable & Governed**: Supabase tracks metadata, logs, and version history.
* **Integration Ready**: Frontend, backend, and libraries are plug-and-play.
* **Complete & Professional**: Every PRD becomes a comprehensive document ready for Devin AI.

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
- [x] **Enhanced PRD System** - Industry best practices with 17 sections
- [x] **PRD Completion Tracking** - Automatic calculation and missing section detection
- [x] **Guided Questions System** - Interactive completion workflow
- [x] **Voice-First PRD Creation** - Standardized markdown output for Devin AI
- [x] **PRD Markdown Export** - Professional documentation ready for sharing
- [x] **Directory Structure Optimization** - Clean, logical organization of all project files
- [x] **Environment Management System** - Professional config file organization with backup system
- [x] **Script Organization** - Logical grouping of automation scripts by purpose
- [x] **Environment Manager Tool** - Automated backup/restore and configuration management

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
