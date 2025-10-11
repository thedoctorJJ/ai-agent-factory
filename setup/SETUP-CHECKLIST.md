# 🚀 Setup Checklist for AI Agent Factory Agent Factory

Use this checklist to ensure you have all accounts and APIs properly configured.

## 📋 Account Setup Checklist

### ✅ Core Services
- [ ] **Supabase Account**
  - [ ] Create project: `end-cap-agent-factory`
  - [ ] Get API keys (URL, anon key, service role key)
  - [ ] Set up database schema
  - [ ] Configure authentication
  - [ ] Create storage buckets

- [ ] **Google Cloud Platform**
  - [ ] Create project: `end-cap-agent-factory`
  - [ ] Enable required APIs (Cloud Run, Cloud Build, Secret Manager)
  - [ ] Create service account with proper permissions
  - [ ] Download service account JSON key
  - [ ] Set up Secret Manager with all secrets

- [ ] **GitHub**
  - [ ] Create GitHub App in your organization
  - [ ] Configure permissions (Contents, Metadata, Pull requests, Issues)
  - [ ] Set webhook URL and secret
  - [ ] Generate and download private key
  - [ ] Install app on organization
  - [ ] Note App ID

- [ ] **OpenAI**
  - [ ] Create account and add payment method
  - [ ] Generate API key
  - [ ] Set usage limits
  - [ ] Test API access

### ✅ Optional Services
- [ ] **Sentry** (for error monitoring)
- [ ] **Slack** (for notifications)
- [ ] **Vercel** (alternative frontend hosting)

## 🔧 Configuration Checklist

### ✅ Environment Variables
- [ ] Initialize environment: `./scripts/config/env-manager.sh init`
- [ ] Edit `config/env/.env.local` with your actual values
- [ ] Create backup: `./scripts/config/env-manager.sh backup`
- [ ] Fill in all required values:
  - [ ] `DATABASE_URL`
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_KEY`
  - [ ] `SUPABASE_SERVICE_ROLE_KEY`
  - [ ] `GOOGLE_CLOUD_PROJECT_ID`
  - [ ] `GITHUB_APP_ID`
  - [ ] `GITHUB_PRIVATE_KEY`
  - [ ] `OPENAI_API_KEY`

### ✅ File Permissions
- [ ] Service account JSON key file is readable
- [ ] GitHub private key file is readable
- [ ] All scripts are executable (`chmod +x scripts/*`)

## 🧪 Validation Checklist

### ✅ Test Connections
- [ ] Run configuration validation: `python scripts/validate-config.py`
- [ ] Test Supabase connection
- [ ] Test OpenAI API
- [ ] Test Google Cloud authentication
- [ ] Test GitHub App webhook

### ✅ Local Development
- [ ] Backend starts without errors: `uvicorn fastapi_app.main:app --reload`
- [ ] Frontend builds successfully: `npm run build`
- [ ] Database migrations run successfully
- [ ] All API endpoints respond correctly

## 🚀 Deployment Checklist

### ✅ Production Setup
- [ ] Google Cloud Run services configured
- [ ] Supabase production project created
- [ ] GitHub App installed on production org
- [ ] Domain and SSL certificates configured
- [ ] Monitoring and logging set up

### ✅ Security
- [ ] All secrets stored in Secret Manager
- [ ] No hardcoded credentials in code
- [ ] API keys have appropriate permissions
- [ ] Webhook signatures verified
- [ ] CORS properly configured

## 📚 Documentation

### ✅ Read Documentation
- [ ] [Accounts and APIs Setup Guide](./docs/09-accounts-and-apis-setup.md)
- [ ] [Infrastructure Blueprint](./docs/01-infrastructure-blueprint.md)
- [ ] [DevOps & Deployment Flow](./docs/02-devops-deployment-flow.md)
- [ ] [Platform Architecture Diagram](./docs/08-platform-architecture-diagram.md)

## 🆘 Troubleshooting

### Common Issues
- **Supabase connection fails**: Check URL and API keys
- **GitHub App not working**: Verify webhook URL and permissions
- **Google Cloud errors**: Ensure APIs are enabled and service account has permissions
- **OpenAI API errors**: Check API key and billing status

### Getting Help
- Check the detailed setup guide: `docs/09-accounts-and-apis-setup.md`
- Run validation script: `python scripts/validate-config.py`
- Review error logs in your services

---

## ✅ Ready to Go!

Once all items are checked, you can:

1. **Start development**: `./scripts/dev-setup.sh`
2. **Run validation**: `python scripts/validate-config.py`
3. **Start services**: Follow the Quick Start guide in README.md

Your Modular AI Agent Platform will be ready for development and deployment! 🎉
