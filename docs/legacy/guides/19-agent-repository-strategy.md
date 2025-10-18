# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[04-06 - System Guides](../../04-prd-system.md)** — Current implementation documentation
> 
> **This file is preserved for historical reference only.**

---

# Agent Repository Strategy Implementation Guide

## Overview

This guide details the implementation of the separate repository strategy for AI agents created through the AI Agent Factory platform. Each agent gets its own dedicated GitHub repository while maintaining integration with the central platform.

## 🏗️ Repository Architecture

### **Central Platform Repository**
```
thedoctorJJ/ai-agent-factory/
├── backend/                    # Core platform backend
├── frontend/                   # Core platform frontend  
├── scripts/                    # Platform automation
├── libraries/                  # Shared components
├── docs/                       # Platform documentation
└── infra/                      # Infrastructure configs
```

### **Individual Agent Repositories**
```
thedoctorJJ/ai-agents-{name}/
├── agent/                      # Agent implementation
├── tests/                      # Agent-specific tests
├── docs/                       # Agent documentation
├── deployment/                 # Deployment configs
└── .github/                    # CI/CD workflows
```

## 🔄 Complete Workflow

### **Phase 1: PRD Creation & Upload**
1. **Voice/Text Conversation** in ChatGPT
2. **PRD Export** as structured markdown
3. **Upload to AI Agent Factory** platform
4. **Validation & Analysis** by platform

### **Phase 2: Agent Generation**
1. **Devin AI Processing** of PRD
2. **Repository Creation** via GitHub MCP server
3. **Code Generation** with platform templates
4. **Database Setup** via Supabase MCP server

### **Phase 3: Deployment & Integration**
1. **Cloud Run Deployment** via Google Cloud MCP server
2. **Platform Registration** in AI Agent Factory
3. **Health Monitoring** setup
4. **Documentation Generation**

## 🛠️ Implementation Details

### **1. Repository Creation Process**

#### **GitHub MCP Server Configuration**
```json
{
  "name": "AI Agent Factory - GitHub Integration",
  "capabilities": [
    "create_repository",
    "setup_branch_protection", 
    "configure_workflows",
    "manage_secrets"
  ],
  "repository_template": "thedoctorJJ/ai-agent-factory",
  "naming_convention": "ai-agents-{kebab-case-name}"
}
```

#### **Repository Structure Template**
```
ai-agents-{name}/
├── agent/
│   ├── main.py                 # Main agent logic
│   ├── requirements.txt        # Python dependencies
│   ├── config.py              # Configuration management
│   ├── utils.py               # Utility functions
│   └── handlers/              # Request handlers
│       ├── __init__.py
│       ├── api_handler.py
│       ├── data_handler.py
│       └── ai_handler.py
├── tests/
│   ├── __init__.py
│   ├── test_agent.py          # Unit tests
│   ├── test_integration.py    # Integration tests
│   └── test_handlers/         # Handler tests
├── docs/
│   ├── README.md              # Agent documentation
│   ├── API.md                 # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── EXAMPLES.md            # Usage examples
├── deployment/
│   ├── Dockerfile             # Container configuration
│   ├── cloud-run.yaml         # Google Cloud Run config
│   ├── .env.example           # Environment variables template
│   └── health-check.py        # Health check endpoint
├── .github/
│   └── workflows/
│       ├── ci.yml             # Continuous integration
│       ├── deploy.yml         # Deployment pipeline
│       └── security.yml       # Security scanning
├── .gitignore                 # Git ignore rules
├── pyproject.toml             # Python project config
└── LICENSE                    # License file
```

### **2. Agent Code Generation**

#### **Main Agent Template**
```python
# agent/main.py
from fastapi import FastAPI, HTTPException
from agent.config import AgentConfig
from agent.handlers import APIHandler, DataHandler, AIHandler
import logging

class AIAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.app = FastAPI(title=config.name, version=config.version)
        self.api_handler = APIHandler(config)
        self.data_handler = DataHandler(config)
        self.ai_handler = AIHandler(config)
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "agent": self.config.name}
        
        @self.app.post("/api/v1/process")
        async def process_request(request: dict):
            try:
                result = await self.ai_handler.process(request)
                return {"success": True, "result": result}
            except Exception as e:
                logging.error(f"Processing error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start(self):
        """Start the agent service"""
        logging.info(f"Starting {self.config.name} agent")
        # Implementation details
```

#### **Configuration Management**
```python
# agent/config.py
from pydantic import BaseSettings
from typing import List, Optional

class AgentConfig(BaseSettings):
    name: str
    version: str = "1.0.0"
    description: str
    requirements: List[str]
    target_users: List[str]
    success_metrics: List[str]
    
    # Platform integration
    platform_api_url: str = "https://ai-agent-factory.com/api/v1"
    agent_id: Optional[str] = None
    
    # External services
    openai_api_key: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
```

### **3. Database Integration**

#### **Supabase MCP Server Setup**
```json
{
  "name": "AI Agent Factory - Supabase Integration",
  "capabilities": [
    "create_tables",
    "setup_relationships",
    "configure_auth",
    "create_triggers"
  ],
  "database_schema": {
    "agents": {
      "id": "uuid PRIMARY KEY",
      "name": "text NOT NULL",
      "description": "text",
      "version": "text",
      "status": "text",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    },
    "agent_executions": {
      "id": "uuid PRIMARY KEY", 
      "agent_id": "uuid REFERENCES agents(id)",
      "request_data": "jsonb",
      "response_data": "jsonb",
      "execution_time": "float",
      "status": "text",
      "created_at": "timestamp"
    },
    "agent_metrics": {
      "id": "uuid PRIMARY KEY",
      "agent_id": "uuid REFERENCES agents(id)",
      "metric_name": "text",
      "metric_value": "float",
      "timestamp": "timestamp"
    }
  }
}
```

### **4. Deployment Configuration**

#### **Google Cloud Run Setup**
```yaml
# deployment/cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: ai-agents-{name}
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 100
      containers:
      - image: gcr.io/ai-agent-factory/ai-agents-{name}:latest
        ports:
        - containerPort: 8080
        env:
        - name: AGENT_NAME
          value: "{name}"
        - name: PLATFORM_API_URL
          value: "https://ai-agent-factory.com/api/v1"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
```

#### **Dockerfile Template**
```dockerfile
# deployment/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agent/ ./agent/
COPY deployment/health-check.py .

# Create non-root user
RUN useradd --create-home --shell /bin/bash agent
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python health-check.py

# Expose port
EXPOSE 8080

# Start the agent
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **5. CI/CD Pipeline**

#### **GitHub Actions Workflow**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r agent/requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=agent --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ai-agent-factory
    
    - name: Build and push image
      run: |
        docker build -t gcr.io/ai-agent-factory/ai-agents-${{ github.event.repository.name }}:${{ github.sha }} .
        docker push gcr.io/ai-agent-factory/ai-agents-${{ github.event.repository.name }}:${{ github.sha }}
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy ai-agents-${{ github.event.repository.name }} \
          --image gcr.io/ai-agent-factory/ai-agents-${{ github.event.repository.name }}:${{ github.sha }} \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
```

## 🔗 Platform Integration

### **Agent Registration Process**

#### **Platform API Integration**
```python
# agent/platform_integration.py
import httpx
from agent.config import AgentConfig

class PlatformIntegration:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.platform_url = config.platform_api_url
        self.agent_id = config.agent_id
    
    async def register_agent(self):
        """Register agent with AI Agent Factory platform"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.platform_url}/agents/register",
                json={
                    "name": self.config.name,
                    "description": self.config.description,
                    "version": self.config.version,
                    "deployment_url": self.get_deployment_url(),
                    "health_check_url": f"{self.get_deployment_url()}/health",
                    "capabilities": self.config.requirements
                }
            )
            if response.status_code == 201:
                agent_data = response.json()
                self.agent_id = agent_data["id"]
                return agent_data
            else:
                raise Exception(f"Registration failed: {response.text}")
    
    async def send_metrics(self, metrics: dict):
        """Send performance metrics to platform"""
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.platform_url}/agents/{self.agent_id}/metrics",
                json=metrics
            )
    
    def get_deployment_url(self) -> str:
        """Get the agent's deployment URL"""
        return f"https://ai-agents-{self.config.name.lower().replace(' ', '-')}-hash.run.app"
```

### **Health Monitoring**

#### **Health Check Implementation**
```python
# deployment/health-check.py
import requests
import sys
import os

def health_check():
    """Check if the agent is healthy"""
    try:
        # Get deployment URL from environment
        deployment_url = os.getenv("DEPLOYMENT_URL", "http://localhost:8080")
        
        # Check health endpoint
        response = requests.get(f"{deployment_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("Agent is healthy")
                return 0
            else:
                print(f"Agent unhealthy: {data}")
                return 1
        else:
            print(f"Health check failed: {response.status_code}")
            return 1
            
    except Exception as e:
        print(f"Health check error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(health_check())
```

## 📊 Monitoring & Analytics

### **Metrics Collection**

#### **Performance Metrics**
```python
# agent/metrics.py
import time
import asyncio
from typing import Dict, Any
from agent.platform_integration import PlatformIntegration

class MetricsCollector:
    def __init__(self, platform_integration: PlatformIntegration):
        self.platform = platform_integration
        self.metrics = {}
    
    async def record_execution(self, request_data: dict, response_data: dict, execution_time: float):
        """Record agent execution metrics"""
        metrics = {
            "execution_time": execution_time,
            "request_size": len(str(request_data)),
            "response_size": len(str(response_data)),
            "timestamp": time.time(),
            "status": "success" if response_data else "error"
        }
        
        # Send to platform
        await self.platform.send_metrics(metrics)
        
        # Store locally for batch processing
        self.metrics[time.time()] = metrics
    
    async def record_error(self, error: Exception, request_data: dict):
        """Record error metrics"""
        metrics = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "request_data": request_data,
            "timestamp": time.time(),
            "status": "error"
        }
        
        await self.platform.send_metrics(metrics)
```

## 🚀 Deployment Checklist

### **Pre-Deployment**
- [ ] Repository created with proper structure
- [ ] Agent code implemented and tested
- [ ] Database tables created in Supabase
- [ ] Environment variables configured
- [ ] CI/CD pipeline configured

### **Deployment**
- [ ] Docker image built and pushed
- [ ] Cloud Run service deployed
- [ ] Health check endpoint responding
- [ ] Agent registered with platform
- [ ] Monitoring configured

### **Post-Deployment**
- [ ] End-to-end testing completed
- [ ] Performance metrics baseline established
- [ ] Documentation updated
- [ ] Team access configured
- [ ] Backup procedures in place

## 🔧 Maintenance & Updates

### **Agent Updates**
1. **Code Changes** → Push to agent repository
2. **CI/CD Pipeline** → Automatic testing and deployment
3. **Platform Notification** → Update platform with new version
4. **Health Verification** → Confirm agent is functioning

### **Platform Updates**
1. **Template Updates** → Update agent template in main repository
2. **Library Updates** → Update shared libraries
3. **Agent Migration** → Migrate agents to new template (optional)
4. **Documentation** → Update agent documentation

## 📚 Best Practices

### **Repository Management**
- Use semantic versioning for agent releases
- Maintain comprehensive documentation
- Implement proper error handling and logging
- Follow security best practices
- Regular dependency updates

### **Platform Integration**
- Register agents immediately after deployment
- Send regular health checks to platform
- Implement proper metrics collection
- Handle platform API failures gracefully
- Maintain backward compatibility

### **Team Collaboration**
- Use feature branches for development
- Require code reviews for all changes
- Implement proper testing strategies
- Document all configuration changes
- Maintain clear ownership boundaries

## 🎯 Success Metrics

### **Technical Metrics**
- Agent deployment success rate: >95%
- Agent uptime: >99.5%
- Response time: <2 seconds
- Error rate: <1%

### **Operational Metrics**
- Time to deploy new agent: <30 minutes
- Time to fix critical issues: <1 hour
- Documentation completeness: 100%
- Test coverage: >80%

This implementation guide provides a comprehensive framework for managing individual agent repositories while maintaining tight integration with the AI Agent Factory platform.
