#!/bin/bash

echo "🚀 Setting up Cursor Agent Integration for AI Agent Factory"
echo "=========================================================="

# Get the current directory
CURRENT_DIR=$(pwd)
MCP_SERVER_PATH="$CURRENT_DIR/scripts/mcp/cursor-agent-mcp-server.py"
CONFIG_PATH="$CURRENT_DIR/config/cursor-agent-mcp-config.json"

echo "📁 Current directory: $CURRENT_DIR"
echo "📁 MCP Server path: $MCP_SERVER_PATH"
echo "📁 Config path: $CONFIG_PATH"

# Check if MCP server exists
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at: $MCP_SERVER_PATH"
    exit 1
fi

echo "✅ MCP server found"

# Make the script executable
chmod +x "$MCP_SERVER_PATH"
echo "✅ Made MCP server executable"

# Test the MCP server
echo "🧪 Testing MCP server..."
python3 "$MCP_SERVER_PATH" --test 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ MCP server test passed"
else
    echo "⚠️  MCP server test failed (this might be normal for stdio mode)"
fi

# Check environment configuration
echo "🔧 Checking environment configuration..."
if [ -f "config/env/.env.local" ]; then
    echo "✅ Environment configuration found"
    
    # Check if all required services are configured
    if grep -q "SUPABASE_URL=" config/env/.env.local && grep -q "GITHUB_TOKEN=" config/env/.env.local; then
        echo "✅ Core services configured (Supabase, GitHub)"
    else
        echo "⚠️  Some core services may not be configured"
    fi
    
    if grep -q "OPENAI_API_KEY=" config/env/.env.local; then
        echo "✅ OpenAI configured"
    else
        echo "⚠️  OpenAI not configured"
    fi
    
    if grep -q "GOOGLE_CLOUD_PROJECT_ID=" config/env/.env.local; then
        echo "✅ Google Cloud configured"
    else
        echo "⚠️  Google Cloud not configured"
    fi
else
    echo "❌ Environment configuration not found"
    echo "Please run: ./scripts/config/env-manager.sh init"
    exit 1
fi

# Test database connection
echo "🗄️  Testing database connection..."
python3 -c "
import sys
sys.path.insert(0, '.')
from backend.fastapi_app.config import Config
from scripts.mcp.simple_services import SimpleSupabaseService

config = Config()
if config.supabase_url and config.supabase_service_role_key:
    try:
        service = SimpleSupabaseService(config.supabase_url, config.supabase_service_role_key)
        print('✅ Database connection configured')
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
else:
    print('❌ Database not configured')
"

# Test GitHub connection
echo "🐙 Testing GitHub connection..."
python3 -c "
import sys
sys.path.insert(0, '.')
from backend.fastapi_app.config import Config
from scripts.mcp.simple_services import SimpleGitHubService

config = Config()
if config.github_token:
    try:
        service = SimpleGitHubService(config.github_token)
        print('✅ GitHub connection configured')
    except Exception as e:
        print(f'❌ GitHub connection failed: {e}')
else:
    print('❌ GitHub not configured')
"

echo ""
echo "📋 Cursor Agent Integration Setup Complete!"
echo "=========================================="
echo ""
echo "🔧 Next Steps:"
echo "1. Add the MCP server to Cursor Agent:"
echo "   - Open Cursor Agent settings"
echo "   - Go to MCP Servers"
echo "   - Add new server with the configuration from: $CONFIG_PATH"
echo ""
echo "2. Available Tools:"
echo "   - get_platform_status: Check system health"
echo "   - list_prds: View all PRDs"
echo "   - create_prd: Add new PRDs"
echo "   - deploy_agent: Deploy agents to Google Cloud Run"
echo "   - create_github_repo: Create repositories"
echo "   - start_backend_server: Run backend locally"
echo "   - start_frontend_server: Run frontend locally"
echo ""
echo "3. Test the integration:"
echo "   - Use 'get_platform_status' to verify all connections"
echo "   - Use 'validate_environment' to check configuration"
echo ""
echo "📄 Configuration file: $CONFIG_PATH"
echo "🤖 MCP Server: $MCP_SERVER_PATH"
echo ""
echo "🎉 You can now use Cursor Agent to manage your AI Agent Factory platform!"
