# AI Agent Factory

Welcome to the **AI Agent Factory** — a repeatable, AI-driven platform that receives completed, formatted PRDs and automatically creates modular agents with fully automated orchestration and deployment.

This repository contains all core infrastructure, libraries, and documentation to build, orchestrate, and deploy AI agents efficiently from completed PRDs.

---

## 📚 Documentation

### 1. Core Platform
- [Infrastructure Blueprint](./docs/01-infrastructure-blueprint.md) — folder structure, frontend/backend setup, hosting, AI core, and key principles.
- [DevOps & Deployment Flow](./docs/02-devops-deployment-flow.md) — local dev, CI/CD, monitoring, and rollback.
- [Agent Lifecycle Framework](./docs/03-agent-lifecycle-framework.md) — lifecycle stages, metadata, versioning, and governance.

### 2. Specialized Integration
- [Devin AI Integration Framework](./docs/04-devin-ai-integration.md) — autonomous agent orchestration and execution.
- [UI Integration & Transition Layer](./docs/06-ui-integration.md) — Next.js + shadcn dashboard for monitoring and execution.
- [GitHub MCP Service](./docs/07-github-mcp-service.md) — automated repository creation for each new PRD.
  
#### Roadmap & PRD Management
- PRD Types — `platform` vs `agent` streams with filters and views
- Roadmap Dashboard — prioritization, kanban, analytics
- Architecture Agent — continuous architecture review; proposals flow Architecture Agent → Devin AI → Platform Owner

### 3. Supporting / Visualization
- [Platform Architecture Diagram](./docs/08-platform-architecture-diagram.md) — full architecture overview, data flow, and component interaction.
- [Accounts and APIs Setup Guide](./docs/09-accounts-and-apis-setup.md) — complete guide for setting up all required accounts and APIs.
- [MCP Server Setup Guide](./docs/13-mcp-server-setup-guide.md) — step-by-step guide for configuring the MCP server in Devin AI.
- [Unified MCP Setup Guide](./docs/14-unified-mcp-setup.md) — complete guide for the unified MCP server configuration.
- [Security Improvements](./docs/17-security-improvements.md) — security check fixes and GitHub sync improvements.
- [Agent Repository Strategy](./docs/19-agent-repository-strategy.md) — comprehensive guide for separate repository strategy implementation.

### 4. Project Management
- [Directory Reorganization](./DIRECTORY_REORGANIZATION.md) — summary of directory structure improvements and organization.
- [Environment Organization](./ENVIRONMENT_ORGANIZATION.md) — comprehensive environment management system documentation.
- [Architecture Review Summary](./ARCHITECTURE_REVIEW_SUMMARY.md) — detailed review of code and architecture improvements.

---


### PRD Types: Platform vs Agent
- `prd_type` field: `platform` (build the factory) or `agent` (use the factory)
- Frontend filters in PRDs and Roadmap tabs

---

## 🗺️ Product Roadmap Dashboard

Features:
- Filters: category, status, effort, prd_type; sorting by priority/date/title
- Views: Roadmap list, Prioritization Matrix, Kanban, Analytics

Endpoints:
- `GET /api/v1/prds/roadmap/overview`
- `GET /api/v1/prds/roadmap/prds?prd_type=platform|agent&...`
- `GET /api/v1/prds/roadmap/prioritization-matrix`

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

### 🔄 **Typical Workflow**

1. **Upload Completed PRD**: User uploads or pastes a completed, formatted PRD into the platform

2. **PRD Processing**: Platform processes and validates the completed PRD

3. **Agent Creation**: Our AI Factory automatically creates the AI agent based on the PRD specifications

4. **Repository Creation**: GitHub repository is automatically created for the new agent

5. **Deployment**: Agent is deployed and made available for use

The AI Agent Factory focuses on **agent creation from completed PRDs** - it receives finished PRDs and moves directly to agent generation.

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

## 🧪 **Testing the PRD Workflow**

### **How to Test PRD Submission:**
1. **Start the platform** (see Quick Start section below)
2. **Navigate to the dashboard** at http://localhost:3000
3. **Click "Create New" tab** to access PRD submission
4. **Submit a test PRD** using the form or upload functionality
5. **Verify PRD processing** in the PRDs tab
6. **Test markdown export** for Devin AI integration
7. **Review the roadmap** and prioritization features

### **Sample PRDs Available:**
- Run `python scripts/create-sample-prds.py` to populate the system with test PRDs
- Includes 9 comprehensive PRDs covering infrastructure, features, and platform improvements
- Perfect for testing the complete workflow from submission to processing

## 🎉 **Ready to Go!**

Your AI Agent Factory is **fully configured** and ready for development:
- ✅ **All APIs configured** (Supabase, OpenAI, Google Cloud, GitHub)
- ✅ **Devin AI integration** with MCP server setup
- ✅ **OpenAI voice workflow** - Create agents through ChatGPT conversations
- ✅ **GitHub token validated** and working correctly
- ✅ **MCP server functional** - Creates repositories automatically
- ✅ **HTTP MCP Server deployed** - Publicly accessible at `https://end-cap-mcp-server-http-fdqqqinvyq-uc.a.run.app`
- ✅ **Configuration validated** (15/15 checks passing)
- ✅ **Development environment ready**
- ✅ **PRD System** - Comprehensive PRD creation and management
- ✅ **PRD-First UI Design** - Home page prominently features PRD submission as primary entry point
- ✅ **Professional Environment Management** - Organized config files with automated backup system
- ✅ **Optimized Directory Structure** - Clean, logical organization of all project files
- ✅ **Environment Manager Tool** - Automated backup/restore and configuration management
- ✅ **Script Organization** - Logical grouping of automation scripts by purpose
- ✅ **Comprehensive Architecture Review** - Professional code quality and error handling
- ✅ **Centralized Configuration System** - Smart environment management with validation
- ✅ **Enhanced Health Monitoring** - Detailed system status and service health checks
- ✅ **Production-Ready Codebase** - All security vulnerabilities resolved, linting clean

**Start creating agents** - no additional setup required!

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
- **Pre-commit hook**: Automatically prevents sensitive files from being committed with improved pattern matching
- **Secure commit script**: `./scripts/setup/secure-commit.sh "Your message"` - Enhanced with better error handling
- **Install security hook**: `./scripts/setup/install-pre-commit-hook.sh`
- **Environment manager**: `./scripts/config/env-manager.sh` - Manage config files safely
- **Improved Security Check**: Fixed regex patterns and error handling for reliable GitHub sync

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
ai-agent-factory/
├── backend/              # FastAPI backend application
├── frontend/             # Next.js frontend application
├── docs/                 # Comprehensive documentation
│   ├── summaries/        # Project summaries and status reports
│   └── [18 guide files]  # Detailed documentation guides
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
│   └── samples/         # Test sample files
├── reports/              # Project reports and analysis
├── libraries/            # Agent, prompt, and tool libraries
│   ├── agent-library/   # Reusable agent templates
│   ├── prompt-library/  # Reusable prompts and templates
│   ├── tool-library/    # Reusable tools and utilities
│   └── mcp-service-template/ # MCP service templates
├── infra/                # Infrastructure and deployment configs
└── README.md             # This file
```

## 🏗️ Architecture

### Backend (FastAPI)
- **API Endpoints**: `/api/v1/agents`, `/api/v1/prds`, `/api/v1/health`, `/api/v1/devin`
- **PRD System**: Comprehensive PRD creation and management
- **Models**: Pydantic models for agents and PRDs
- **Database**: Supabase integration ready
- **Devin AI Integration**: MCP server for automated deployment
- **HTTP MCP Server**: Publicly deployed FastAPI server for external integrations
- **Authentication**: JWT-based auth system

### Frontend (Next.js 14)
- **Dashboard**: Agent and PRD management interface
- **Agent Creation Focus**: Home page prominently features PRD creation for agent generation
- **PRD Creation Interface**: Create comprehensive PRDs for agent creation
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

### Configuration & Monitoring
- **Centralized Configuration**: Smart environment management with validation
- **Health Monitoring**: Comprehensive system status and service health checks
- **Error Handling**: Robust error handling with graceful degradation
- **Configuration Validation**: Real-time config validation and status reporting

---

## 📋 PRD System

### **Completed PRD Processing**
The AI Agent Factory receives and processes completed, formatted PRDs:

#### **PRD Sections**
- **Core Sections**: Title, Description, Problem Statement, Target Users, User Stories, Requirements, Acceptance Criteria, Technical Requirements, Success Metrics, Timeline
- **Optional Sections**: Performance Requirements, Security Requirements, Integration Requirements, Deployment Requirements, Dependencies, Risks, Assumptions

#### **PRD-to-Agent Workflow**
- **PRD Upload**: Upload or paste completed, formatted PRDs into the platform
- **Devin-Ready**: Markdown files are optimized for Devin AI with clear implementation phases
- **Complete Specifications**: Includes all technical details, repository structure, and deployment instructions
- **Easy Sharing**: One-click download or view in browser

### **API Endpoints**
- `POST /api/v1/prds` - Submit completed PRD for agent creation
- `GET /api/v1/prds/{id}/markdown` - Export PRD as markdown for Devin AI
- `GET /api/v1/prds/{id}/markdown/download` - Download PRD as .md file

## 🧩 Principles

* **Modular & Repeatable**: Every new agent follows the same lifecycle.
* **Automated**: PRDs trigger automated agent creation and deployment pipelines.
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
- [x] **Conversational PRD Completion** - AI chatbot interface for natural PRD completion through dialogue
- [x] **Intelligent PRD Analysis** - Automatic analysis of PRD quality with specific improvement suggestions
- [x] **Markdown PRD Import** - Paste existing PRDs and get conversational completion for missing sections
- [x] **PRD-First UI Design** - Home page prominently features PRD submission as primary entry point
- [x] **Guided Questions System** - Interactive completion workflow
- [x] **Voice-First PRD Creation** - Standardized markdown output for Devin AI
- [x] **PRD Markdown Export** - Professional documentation ready for sharing
- [x] **Directory Structure Optimization** - Clean, logical organization of all project files
- [x] **Environment Management System** - Professional config file organization with backup system
- [x] **Script Organization** - Logical grouping of automation scripts by purpose
- [x] **Environment Manager Tool** - Automated backup/restore and configuration management
- [x] **Comprehensive Architecture Review** - Professional code quality and error handling
- [x] **Centralized Configuration System** - Smart environment management with validation
- [x] **Enhanced Health Monitoring** - Detailed system status and service health checks
- [x] **Production-Ready Codebase** - All security vulnerabilities resolved, linting clean

### 🚧 In Progress
- [ ] Advanced agent orchestration features
- [ ] Production deployment to Google Cloud Run
- [ ] Modular agent architecture implementation
- [ ] PRD workflow testing and validation

### 📋 Next Steps
1. ✅ **Set up accounts and APIs** - Complete! All services configured
2. ✅ **Validate configuration** - All validations passing
3. ✅ **Start development** - Platform is ready to run
4. **Test PRD submission workflow** - Submit test PRDs and validate the process
5. **UI/UX review and improvements** - Review and enhance the user interface
6. **Build GitHub MCP service** for automated repo creation
7. **Integrate Devin AI** for agent orchestration
8. **Deploy to Google Cloud Run** for production use

## 🔗 Contacts / Contributors

* **Lead Architect**: JJ
* **Platform AI**: Devin AI
* **Repository**: [thedoctorJJ/end-cap-agent-factory](https://github.com/thedoctorJJ/end-cap-agent-factory)
