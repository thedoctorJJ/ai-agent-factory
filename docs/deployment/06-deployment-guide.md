# Deployment Guide

## 📋 **Document Summary**

This comprehensive deployment guide covers deploying the AI Agent Factory to production environments, including the deployment architecture with Google Cloud Run, Supabase, and MCP servers, detailed deployment procedures for backend, frontend, and MCP server components, database deployment with Supabase setup and migrations, security configuration including service accounts and secret management, monitoring and logging setup with Google Cloud monitoring, testing procedures for deployment validation, CI/CD pipeline configuration with GitHub Actions, deployment scripts and automation, production checklists, troubleshooting common issues, and maintenance procedures for keeping the system updated and secure.

---

## 🎯 **Deployment Overview**

This guide covers deploying the AI Agent Factory to production environments, including backend, frontend, and MCP server deployments.

## 🌐 **Current Live Deployment**

The AI Agent Factory is **currently deployed and running** in production on Google Cloud Run:

### **Live Production URLs**
- **Frontend Application**: https://ai-agent-factory-frontend-952475323593.us-central1.run.app
- **Backend API**: https://ai-agent-factory-backend-952475323593.us-central1.run.app
- **MCP Server**: https://ai-agent-factory-mcp-server-952475323593.us-central1.run.app
- **API Documentation**: https://ai-agent-factory-backend-952475323593.us-central1.run.app/docs

### **Deployment Status**
- ✅ **All services deployed** and responding
- ✅ **Auto-scaling enabled** (1-10 instances per service)
- ✅ **Health monitoring** active
- ✅ **Environment variables** configured
- ✅ **Database connections** established

## 🏗️ **Deployment Architecture**

### **Production Stack**
- **Backend**: Google Cloud Run (FastAPI)
- **Frontend**: Google Cloud Run (Next.js)
- **Database**: Supabase (PostgreSQL)
- **MCP Server**: Google Cloud Run (HTTP MCP Server)
- **Storage**: Google Cloud Storage
- **Secrets**: Google Secret Manager

### **Deployment Flow**
```
Development → Staging → Production
     ↓           ↓         ↓
Local Testing → Staging Tests → Production Deployment
```

## 🚀 **Backend Deployment**

### **Google Cloud Run Deployment**
```bash
# Deploy backend to Cloud Run
./scripts/setup-google-cloud-run.sh
```

### **Manual Deployment Steps**
1. **Build Docker Image**
   ```bash
   cd backend
   docker build -t ai-agent-factory-backend .
   ```

2. **Tag for Google Container Registry**
   ```bash
   docker tag ai-agent-factory-backend gcr.io/PROJECT_ID/ai-agent-factory-backend
   ```

3. **Push to Registry**
   ```bash
   docker push gcr.io/PROJECT_ID/ai-agent-factory-backend
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy ai-agent-factory-backend \
     --image gcr.io/PROJECT_ID/ai-agent-factory-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ENVIRONMENT=production
   ```

### **Environment Variables**
Set the following environment variables in Cloud Run:
```bash
ENVIRONMENT=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
GOOGLE_CLOUD_PROJECT_ID=your-project-id
```

## 🎨 **Frontend Deployment**

### **Google Cloud Run Deployment**
```bash
cd frontend/next-app
gcloud run deploy ai-agent-factory-frontend --source .
```

### **Manual Deployment Steps**
1. **Build Next.js Application**
   ```bash
   cd frontend/next-app
   npm run build
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY . .
   RUN npm run build
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

3. **Build and Deploy**
   ```bash
   docker build -t ai-agent-factory-frontend .
   docker tag ai-agent-factory-frontend gcr.io/PROJECT_ID/ai-agent-factory-frontend
   docker push gcr.io/PROJECT_ID/ai-agent-factory-frontend
   
   gcloud run deploy ai-agent-factory-frontend \
     --image gcr.io/PROJECT_ID/ai-agent-factory-frontend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### **Environment Variables**
Set the following environment variables:
```bash
NEXT_PUBLIC_API_URL=https://ai-agent-factory-backend-xxx-uc.a.run.app
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 🔧 **MCP Server Deployment**

### **HTTP MCP Server Deployment**
```bash
# Deploy HTTP MCP server
./scripts/deployment/deploy-mcp-server-http.sh
```

### **Manual Deployment Steps**
1. **Build MCP Server**
   ```bash
   cd scripts/mcp
   docker build -t ai-agent-factory-mcp-server .
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy ai-agent-factory-mcp-server-http \
     --image gcr.io/PROJECT_ID/ai-agent-factory-mcp-server \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000
   ```

### **MCP Server Configuration**
Set the following environment variables:
```bash
GITHUB_TOKEN=your-github-token
GOOGLE_CLOUD_PROJECT_ID=your-project-id
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 🗄️ **Database Deployment**

### **Supabase Setup**
1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note project URL and API keys

2. **Run Database Schema**
   ```bash
   # Apply schema to Supabase
   ./scripts/setup/apply-schema-to-supabase.sh
   ```

3. **Verify Database Setup**
   ```bash
   # Test database connection
   ./scripts/setup/test-supabase-connection.py
   ```

### **Database Migrations**
```bash
# Apply database migrations
./scripts/setup/apply-schema.py
```

## 🔒 **Security Configuration**

### **Google Cloud Security**
1. **Service Account Setup**
   ```bash
   # Create service account
   gcloud iam service-accounts create ai-agent-factory-service \
     --display-name="AI Agent Factory Service Account"
   
   # Grant necessary roles
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:ai-agent-factory-service@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   ```

2. **Secret Manager Setup**
   ```bash
   # Create secrets
   echo -n "your-secret-value" | gcloud secrets create SECRET_NAME --data-file=-
   
   # Grant access to service account
   gcloud secrets add-iam-policy-binding SECRET_NAME \
     --member="serviceAccount:ai-agent-factory-service@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

### **CORS Configuration**
Configure CORS for production:
```python
# In backend configuration
CORS_ORIGINS = [
    "https://ai-agent-factory-frontend-xxx-uc.a.run.app",
    "https://your-custom-domain.com"
]
```

## 📊 **Monitoring and Logging**

### **Google Cloud Monitoring**
1. **Enable Monitoring APIs**
   ```bash
   gcloud services enable monitoring.googleapis.com
   gcloud services enable logging.googleapis.com
   ```

2. **Set Up Alerts**
   - Create alerting policies in Google Cloud Console
   - Set up notifications for errors and performance issues
   - Configure Slack/email notifications

### **Application Logging**
```python
# Configure structured logging
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use structured logging for better monitoring
logger = logging.getLogger(__name__)
logger.info("Application started", extra={
    "service": "ai-agent-factory-backend",
    "version": "1.0.0"
})
```

## 🧪 **Testing Deployment**

### **Health Checks**
```bash
# Test backend health
curl https://ai-agent-factory-backend-xxx-uc.a.run.app/api/v1/health

# Test frontend
curl https://ai-agent-factory-frontend-xxx-uc.a.run.app

# Test MCP server
curl https://ai-agent-factory-mcp-server-http-xxx-uc.a.run.app/health
```

### **Integration Testing**
```bash
# Test complete workflow
./scripts/testing/test-devin-integration.py

# Test MCP server functionality
./scripts/testing/test-mcp-server.sh
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions Workflow**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Deploy Backend
        run: |
          cd backend
          gcloud run deploy ai-agent-factory-backend --source .
      
      - name: Deploy Frontend
        run: |
          cd frontend/next-app
          gcloud run deploy ai-agent-factory-frontend --source .
      
      - name: Deploy MCP Server
        run: |
          ./scripts/deployment/deploy-mcp-server-http.sh
```

### **Deployment Scripts**
```bash
# Full deployment script
#!/bin/bash
set -e

echo "🚀 Starting deployment to production..."

# Deploy backend
echo "📦 Deploying backend..."
./scripts/setup-google-cloud-run.sh

# Deploy frontend
echo "🎨 Deploying frontend..."
cd frontend/next-app
gcloud run deploy ai-agent-factory-frontend --source .

# Deploy MCP server
echo "🔧 Deploying MCP server..."
./scripts/deployment/deploy-mcp-server-http.sh

echo "✅ Deployment completed successfully!"
```

## 🎯 **Production Checklist**

### **Pre-deployment**
- [ ] All environment variables configured
- [ ] Database schema applied
- [ ] Secrets stored in Secret Manager
- [ ] CORS configured for production domains
- [ ] Monitoring and alerting set up

### **Post-deployment**
- [ ] Health checks passing
- [ ] All services accessible
- [ ] Database connections working
- [ ] MCP server responding
- [ ] Frontend loading correctly
- [ ] API endpoints functional

### **Monitoring**
- [ ] Application logs visible
- [ ] Error tracking configured
- [ ] Performance metrics available
- [ ] Alerting rules active
- [ ] Backup procedures tested

## 🚨 **Troubleshooting**

### **Common Issues**
1. **CORS Errors**
   - Check CORS configuration in backend
   - Verify frontend URL is in allowed origins

2. **Database Connection Issues**
   - Verify Supabase credentials
   - Check network connectivity
   - Verify database schema is applied

3. **MCP Server Issues**
   - Check GitHub token permissions
   - Verify Google Cloud credentials
   - Check MCP server logs

### **Debug Commands**
```bash
# Check Cloud Run logs
gcloud logs read --service=ai-agent-factory-backend --limit=50

# Check MCP server logs
gcloud logs read --service=ai-agent-factory-mcp-server-http --limit=50

# Test database connection
./scripts/setup/test-supabase-connection.py
```

## 📚 **Documentation**

### **Deployment Documentation**
- **Environment Setup** - Complete environment configuration guide
- **Service Configuration** - Individual service configuration
- **Monitoring Setup** - Monitoring and alerting configuration
- **Troubleshooting** - Common issues and solutions

### **Maintenance**
- **Regular Updates** - Keep dependencies updated
- **Security Patches** - Apply security patches promptly
- **Performance Monitoring** - Monitor performance metrics
- **Backup Procedures** - Regular backup and recovery testing

The deployment guide provides comprehensive instructions for deploying the AI Agent Factory to production with proper security, monitoring, and maintenance procedures.
