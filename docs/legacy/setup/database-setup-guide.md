# ⚠️ LEGACY DOCUMENT - DO NOT USE

> **WARNING**: This is a LEGACY document that is OUTDATED. Please use the new streamlined documentation:
> - **[03 - Setup Guide](../../03-setup-guide.md)** — Current setup documentation
> 
> **This file is preserved for historical reference only.**

---

# Database Setup Guide

This guide will help you set up the Supabase database integration for the AI Agent Factory.

## Prerequisites

1. A Supabase account and project
2. Your Supabase project URL and API keys

## Step 1: Create Environment File

Create a `.env.local` file in the `config/env/` directory with the following content:

```bash
# AI Agent Factory Environment Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Other required environment variables
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
GITHUB_ORG_NAME=thedoctorJJ
GOOGLE_CLOUD_PROJECT_ID=your-gcp-project-id

# Application Configuration
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Step 2: Set Up Supabase Database

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to the **SQL Editor**
4. Copy the contents of `infra/database/schema.sql`
5. Paste and run the SQL script

## Step 3: Test the Integration

Run the database setup script:

```bash
cd /Users/jason/Repositories/ai-agent-factory
source backend/venv/bin/activate
./scripts/setup/setup-database.sh
```

## Step 4: Start the Application

1. Start the backend server:
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn fastapi_app.main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend/next-app
   npm run dev
   ```

## Features Implemented

✅ **Database Schema**: Complete PostgreSQL schema with tables for PRDs, agents, and Devin tasks
✅ **Connection Pooling**: Automatic retry logic with exponential backoff
✅ **Audit Logging**: Automatic audit trails for all database operations
✅ **Fallback Support**: Graceful fallback to in-memory storage if database is unavailable
✅ **Data Persistence**: All data now persists across application restarts
✅ **Performance Optimization**: Indexed queries and efficient data access patterns

## Database Tables

- **prds**: Product Requirements Documents with full metadata
- **agents**: AI agents with configuration and health status
- **devin_tasks**: Devin AI task execution tracking
- **audit_logs**: Automatic audit trail for all operations
- **system_metrics**: Performance and usage metrics

## Troubleshooting

### Connection Issues
- Verify your Supabase URL and API keys are correct
- Check that your Supabase project is active
- Ensure the database schema has been created

### Performance Issues
- Monitor the audit logs for slow queries
- Check the system metrics for connection pool usage
- Verify indexes are being used effectively

### Data Issues
- Check the audit logs for failed operations
- Verify data integrity constraints
- Use the fallback in-memory storage for testing

## Next Steps

1. **Production Deployment**: Configure production Supabase instance
2. **Backup Strategy**: Set up automated database backups
3. **Monitoring**: Implement comprehensive monitoring and alerting
4. **Scaling**: Configure connection pooling for high-traffic scenarios
