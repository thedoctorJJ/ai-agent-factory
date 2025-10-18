#!/bin/bash

# AI Agent Factory - Secure Configuration Setup
# This script sets up secure API key management and creates a working configuration

set -e

echo "🔐 AI Agent Factory - Secure Configuration Setup"
echo "================================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "config/secure-api-manager.py" ]; then
    echo "❌ Error: Cannot find config/secure-api-manager.py"
    echo "   Current directory: $(pwd)"
    echo "   Expected: AI Agent Factory root directory"
    exit 1
fi

# Check if cryptography is installed
echo "📋 Checking dependencies..."
if ! python3 -c "import cryptography" 2>/dev/null; then
    echo "📦 Installing cryptography package..."
    pip3 install cryptography
fi

# Check if existing configuration exists
if [ -f "config/env/.env.local" ]; then
    echo "📥 Found existing configuration. Importing API keys securely..."
    python3 config/secure-api-manager.py import config/env/.env.local
else
    echo "⚠️  No existing configuration found at config/env/.env.local"
    echo "   Please create this file with your API keys first, then run this script again."
    echo ""
    echo "   Example config/env/.env.local content:"
    echo "   SUPABASE_URL=https://your-project.supabase.co"
    echo "   SUPABASE_KEY=your-anon-key"
    echo "   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key"
    echo "   OPENAI_API_KEY=your-openai-key"
    echo "   GITHUB_TOKEN=your-github-token"
    echo "   GITHUB_ORG_NAME=your-org-name"
    exit 1
fi

echo ""
echo "📝 Creating working .env file..."
python3 config/secure-api-manager.py create

echo ""
echo "🔍 Validating configuration..."
python3 config/secure-api-manager.py validate

echo ""
echo "📋 Listing stored API keys..."
python3 config/secure-api-manager.py list

echo ""
echo "✅ Secure configuration setup complete!"
echo ""
echo "🔐 Security Features:"
echo "  - All API keys are encrypted and stored securely"
echo "  - Master key file has restrictive permissions (600)"
echo "  - Encrypted secrets file has restrictive permissions (600)"
echo "  - Working .env file is auto-generated (not stored in git)"
echo ""
echo "📁 Files created:"
echo "  - config/api-secrets.enc (encrypted API keys)"
echo "  - config/.master-key (encryption key)"
echo "  - .env (working configuration - DO NOT COMMIT)"
echo ""
echo "🚀 You can now run the AI Agent Factory!"
echo ""
echo "💡 To update configuration later:"
echo "  1. Edit config/env/.env.local with new API keys"
echo "  2. Run: python3 config/secure-api-manager.py import config/env/.env.local"
echo "  3. Run: python3 config/secure-api-manager.py create"
echo "  4. Run: python3 config/secure-api-manager.py validate"
