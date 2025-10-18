# Setup Documentation

This directory contains setup guides and checklists for the AI Agent Factory.

## 🚀 Quick Setup (Recommended)

**For new installations, use the secure configuration system:**

```bash
# One-command secure setup
./setup/setup-secure-config.sh
```

## Files

- `SETUP-CHECKLIST.md` - Complete setup checklist for new installations

## 🔐 Secure Configuration System

The AI Agent Factory now uses a **secure, encrypted configuration system** that:

- ✅ **Encrypts all API keys** using AES-256 encryption
- ✅ **Centralizes configuration** in one secure location
- ✅ **Prevents git exposure** of sensitive files
- ✅ **Provides easy management** with simple commands

## 📚 Documentation

- **Main README**: See project root `README.md` for complete setup instructions
- **Security Guide**: See `docs/SECURITY.md` for detailed security information
- **Configuration Guide**: See `config/README.md` for configuration details

## 🛡️ Security Best Practices

1. **Use secure setup**: Always use `./setup-secure-config.sh`
2. **Never commit sensitive files**: `.env`, `api-secrets.enc`, `.master-key`
3. **Use secure manager**: Use `config/secure-api-manager.py` for all operations
4. **Keep master key safe**: Losing it means losing access to encrypted keys
