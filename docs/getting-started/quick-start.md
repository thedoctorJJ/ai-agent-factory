# Quick Start Guide

Get the AI Agent Factory up and running in minutes with this quick start guide.

## 🎯 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

## ⚡ 5-Minute Setup

### 1. Clone the Repository
```bash
git clone https://github.com/thedoctorJJ/ai-agent-factory.git
cd ai-agent-factory
```

### 2. Run Setup Script
```bash
./scripts/setup/dev-setup.sh
```

### 3. Configure Environment
```bash
# Initialize environment configuration
./scripts/config/env-manager.sh init

# Edit the generated config/env/.env.local with your values
# See setup-guide.md for detailed configuration
```

### 4. Start the Platform
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn fastapi_app.main:app --reload

# Terminal 2: Frontend
cd frontend/next-app
npm run dev
```

### 5. Access the Platform
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Test the Workflow

### 1. Submit a PRD
- Go to http://localhost:3000
- Click "Submit PRD" tab
- Upload or paste a PRD

### 2. View PRDs
- Check the "PRD Repository" tab
- See your PRD in the queue

### 3. Create an Agent
- Go to "Create Agent" tab
- Select your PRD
- Watch the automated process

## 🎉 You're Ready!

The AI Agent Factory is now running locally. Check out the [Setup Guide](./setup-guide.md) for detailed configuration or the [Architecture Overview](../architecture/architecture-overview.md) to understand how it works.

## 🆘 Need Help?

- **Detailed Setup**: [Setup Guide](./setup-guide.md)
- **Architecture**: [Architecture Overview](../architecture/architecture-overview.md)
- **Issues**: [GitHub Issues](https://github.com/thedoctorJJ/ai-agent-factory/issues)

## 🚀 Next Steps

1. **Configure Services**: Set up Supabase, OpenAI, Google Cloud
2. **Test Integration**: Try the complete PRD-to-Agent workflow
3. **Deploy**: Follow the [Deployment Guide](../deployment/deployment-guide.md)
4. **Contribute**: See [Contributing Guide](../contributing/)
