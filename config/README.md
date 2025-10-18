# Configuration Files

This directory contains the **secure configuration system** for the AI Agent Factory.

## 🔐 Secure Configuration System

**⚠️ IMPORTANT**: The AI Agent Factory now uses a **secure, encrypted configuration system**. Do not manually edit configuration files.

## Files

- `secure-api-manager.py` - **Secure API key management tool**
- `api-secrets.enc` - **Encrypted API keys (DO NOT EDIT)**
- `.master-key` - **Encryption key (DO NOT EDIT)**
- `google-cloud-service-account.json` - Google Cloud service account credentials
- `env/` - Source configuration files

## 🚀 Quick Setup

```bash
# One-command secure setup
./setup/setup-secure-config.sh
```

## 🔧 Manual Setup

```bash
# 1. Import API keys securely
python3 config/secure-api-manager.py import config/env/.env.local

# 2. Create working .env file
python3 config/secure-api-manager.py create

# 3. Validate all services
python3 config/secure-api-manager.py validate
```

## 📁 File Structure

```
config/
├── api-secrets.enc          # 🔐 Encrypted API keys (DO NOT EDIT)
├── .master-key              # 🔑 Encryption key (DO NOT EDIT)
├── secure-api-manager.py    # 🛠️ Secure management tool
├── google-cloud-service-account.json  # 🔐 Google Cloud credentials
└── env/
    └── .env.local           # 📝 Your API keys (source file)
```

## 🛡️ Security

- **All API keys are encrypted** using AES-256 encryption
- **Files have restrictive permissions** (600 - owner only)
- **Never commit sensitive files** to version control
- **Use the secure manager** for all configuration operations

## 📚 Documentation

- **Main README**: See project root README.md for complete instructions
- **Security Guide**: See `docs/SECURITY.md` for detailed security information
