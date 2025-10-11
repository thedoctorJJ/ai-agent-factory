# Infrastructure Configuration

This directory contains all infrastructure configuration files for the AI Agent Factory Agent Factory.

## Files

- `docker-compose.yml` - Local development environment with PostgreSQL and Redis
- `supabase-config.json` - Supabase project configuration
- `google-cloud.yaml` - Google Cloud Run deployment configuration

## Local Development

1. **Start the development environment:**
   ```bash
   cd infra
   docker-compose up -d
   ```

2. **Access services:**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

3. **Stop the environment:**
   ```bash
   docker-compose down
   ```

## Production Deployment

### Google Cloud Run

1. **Build and push images:**
   ```bash
   # Backend
   docker build -t gcr.io/PROJECT_ID/modular-ai-backend:latest ../backend
   docker push gcr.io/PROJECT_ID/modular-ai-backend:latest

   # Frontend
   docker build -t gcr.io/PROJECT_ID/modular-ai-frontend:latest ../frontend/next-app
   docker push gcr.io/PROJECT_ID/modular-ai-frontend:latest
   ```

2. **Deploy services:**
   ```bash
   kubectl apply -f google-cloud.yaml
   ```

### Supabase Setup

1. Create a new Supabase project
2. Update `supabase-config.json` with your project details
3. Set up the database schema
4. Configure authentication providers
5. Deploy edge functions

## Environment Variables

Create a `.env` file in the project root with:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/modular_ai_platform

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_REGION=us-central1

# GitHub
GITHUB_APP_ID=your-github-app-id
GITHUB_PRIVATE_KEY=your-github-private-key
GITHUB_WEBHOOK_SECRET=your-webhook-secret
```
