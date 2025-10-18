# AI Agent Factory - Security Documentation

## 🔐 Security Overview

The AI Agent Factory implements a comprehensive security system to protect API keys, credentials, and sensitive configuration data. All sensitive information is encrypted and stored securely.

## 🛡️ Security Features

### **Encrypted API Key Storage**
- **AES Encryption**: All API keys are encrypted using AES-256 encryption
- **Secure Key Derivation**: Uses PBKDF2 with 100,000 iterations
- **Restrictive Permissions**: All sensitive files have 600 permissions (owner read/write only)

### **Centralized Management**
- **Single Source of Truth**: All API keys stored in one encrypted location
- **Automated Generation**: Working configuration files are auto-generated
- **No Git Exposure**: Sensitive files are never committed to version control

### **Access Control**
- **Master Key Protection**: Encryption key is protected with restrictive permissions
- **Masked Display**: API keys are masked when displayed (shows only first/last 8 characters)
- **Secure Validation**: API keys are validated without exposing full values

## 📁 Secure File Structure

```
config/
├── api-secrets.enc          # 🔐 Encrypted API keys (DO NOT EDIT)
├── .master-key              # 🔑 Encryption key (DO NOT EDIT)
├── secure-api-manager.py    # 🛠️ Secure management tool
├── google-cloud-service-account.json  # 🔐 Google Cloud credentials
└── env/
    ├── .env.local           # 📝 Source API keys (your input)
    ├── .env.backup          # 📋 Backup configuration
    └── env.example          # 📄 Template configuration
```

## 🔧 Security Commands

### **Setup Commands**
```bash
# Complete secure setup
./setup-secure-config.sh

# Manual secure setup
python3 config/secure-api-manager.py setup
```

### **Management Commands**
```bash
# Import API keys from file
python3 config/secure-api-manager.py import config/env/.env.local

# Create working .env file
python3 config/secure-api-manager.py create

# List stored keys (masked)
python3 config/secure-api-manager.py list

# Validate all services
python3 config/secure-api-manager.py validate
```

## 🔒 Stored API Keys

The system securely stores the following API keys and credentials:

### **Database & Storage**
- `DATABASE_URL` - PostgreSQL connection string
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY` - Supabase service role key

### **Cloud Services**
- `GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY` - Google Cloud service account
- `OPENAI_API_KEY` - OpenAI API key
- `GITHUB_TOKEN` - GitHub personal access token
- `GITHUB_PRIVATE_KEY` - GitHub app private key

### **Application Security**
- `JWT_SECRET_KEY` - JWT signing key
- `ENCRYPTION_KEY` - Application encryption key
- `GITHUB_WEBHOOK_SECRET` - GitHub webhook secret

### **Monitoring & Notifications**
- `SENTRY_DSN` - Sentry error tracking
- `SLACK_WEBHOOK_URL` - Slack notifications

## 🚨 Security Best Practices

### **DO:**
- ✅ Use `./setup-secure-config.sh` for initial setup
- ✅ Keep `config/.master-key` safe and backed up
- ✅ Use the secure manager for all API key operations
- ✅ Regularly validate your configuration
- ✅ Update API keys through the secure system

### **DON'T:**
- ❌ Never commit `api-secrets.enc` to git
- ❌ Never commit `.master-key` to git
- ❌ Never commit `.env` files to git
- ❌ Never edit encrypted files directly
- ❌ Never share your master key

## 🔄 Recovery Procedures

### **Lost Master Key**
If you lose your master key, you'll need to re-encrypt all API keys:

```bash
# 1. Delete encrypted files
rm config/api-secrets.enc config/.master-key

# 2. Re-run secure setup
./setup-secure-config.sh

# 3. Re-enter your API keys in config/env/.env.local
```

### **Corrupted Configuration**
If your configuration becomes corrupted:

```bash
# 1. Validate current state
python3 config/secure-api-manager.py validate

# 2. Recreate working .env
python3 config/secure-api-manager.py create

# 3. If still broken, re-import from source
python3 config/secure-api-manager.py import config/env/.env.local
```

## 🔍 Security Validation

### **File Permissions Check**
```bash
# Check that sensitive files have correct permissions
ls -la config/api-secrets.enc config/.master-key
# Should show: -rw------- (600 permissions)
```

### **Git Status Check**
```bash
# Ensure sensitive files are not tracked by git
git status
# Should NOT show: api-secrets.enc, .master-key, .env
```

### **Encryption Verification**
```bash
# Verify encryption is working
python3 config/secure-api-manager.py list
# Should show masked API keys, not plain text
```

## 🛠️ Development Security

### **Local Development**
- Use the secure configuration system for all development
- Never hardcode API keys in source code
- Always use environment variables for sensitive data

### **Production Deployment**
- Use secure environment variable injection
- Never store API keys in container images
- Use cloud provider secret management services

## 📞 Security Support

If you encounter security issues:

1. **Check file permissions**: Ensure sensitive files have 600 permissions
2. **Verify git status**: Ensure no sensitive files are tracked
3. **Run validation**: Use the secure manager validation
4. **Recreate if needed**: Use the recovery procedures above

## 🔐 Security Compliance

This security system provides:
- **Data Encryption**: All sensitive data is encrypted at rest
- **Access Control**: Restrictive file permissions
- **Audit Trail**: Clear logging of configuration operations
- **Recovery Procedures**: Documented recovery processes
- **Best Practices**: Comprehensive security guidelines

The AI Agent Factory security system ensures that your API keys and sensitive configuration data are protected according to industry best practices.
