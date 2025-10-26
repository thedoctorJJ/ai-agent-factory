#!/bin/bash

# Setup Enhanced Cursor Agent MCP Integration with Supabase Management
# This script helps you integrate Supabase database management with Cursor Agent

set -e

echo "🚀 Setting up Enhanced Cursor Agent MCP Integration"
echo "=================================================="

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Script directory: $SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/README.md" ]; then
    echo "❌ Error: Not in the AI Agent Factory project root"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "✅ Project structure verified"

# Create the enhanced MCP server
echo "📝 Creating enhanced MCP server..."
if [ -f "$PROJECT_ROOT/scripts/mcp/enhanced-cursor-agent-mcp-server.py" ]; then
    echo "✅ Enhanced MCP server already exists"
else
    echo "❌ Enhanced MCP server not found"
    exit 1
fi

# Create the Supabase manager
echo "📝 Creating Supabase manager..."
if [ -f "$PROJECT_ROOT/scripts/mcp/supabase-manager.py" ]; then
    echo "✅ Supabase manager already exists"
else
    echo "❌ Supabase manager not found"
    exit 1
fi

# Create the enhanced configuration
echo "📝 Creating enhanced MCP configuration..."
if [ -f "$PROJECT_ROOT/config/enhanced-cursor-agent-mcp-config.json" ]; then
    echo "✅ Enhanced MCP configuration already exists"
else
    echo "❌ Enhanced MCP configuration not found"
    exit 1
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$PROJECT_ROOT/scripts/mcp/enhanced-cursor-agent-mcp-server.py"
chmod +x "$PROJECT_ROOT/scripts/mcp/supabase-manager.py"

echo "✅ Scripts made executable"

# Check for required environment variables
echo "🔍 Checking environment configuration..."

ENV_FILE="$PROJECT_ROOT/config/env/.env.local"
if [ -f "$ENV_FILE" ]; then
    echo "✅ Environment file found: $ENV_FILE"
    source "$ENV_FILE"
    
    # Check for required variables
    if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_SERVICE_ROLE_KEY" ]; then
        echo "✅ Supabase credentials found"
    else
        echo "⚠️  Supabase credentials not found in environment"
        echo "Please add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to $ENV_FILE"
    fi
else
    echo "⚠️  Environment file not found: $ENV_FILE"
    echo "Please create the environment file with your Supabase credentials"
fi

# Create a Cursor Agent MCP configuration file
echo "📝 Creating Cursor Agent MCP configuration..."

CURSOR_MCP_CONFIG="$PROJECT_ROOT/cursor-agent-mcp-config.json"
cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "name": "AI Agent Factory - Enhanced Cursor Agent Integration",
  "description": "Enhanced MCP server with Supabase database management and security tools",
  "icon": "🤖",
  "transport": "stdio",
  "command": "python3",
  "args": ["$PROJECT_ROOT/scripts/mcp/enhanced-cursor-agent-mcp-server.py"],
  "env": {
    "SUPABASE_URL": "${SUPABASE_URL:-https://ssdcbhxctakgysnayzeq.supabase.co}",
    "SUPABASE_SERVICE_ROLE_KEY": "${SUPABASE_SERVICE_ROLE_KEY:-your-service-role-key-here}",
    "GITHUB_TOKEN": "${GITHUB_TOKEN:-your-github-token-here}",
    "OPENAI_API_KEY": "${OPENAI_API_KEY:-your-openai-api-key-here}",
    "GOOGLE_CLOUD_PROJECT_ID": "agent-factory-474201",
    "ENVIRONMENT": "production",
    "DEBUG": "true"
  }
}
EOF

echo "✅ Cursor Agent MCP configuration created: $CURSOR_MCP_CONFIG"

# Test the enhanced MCP server
echo "🧪 Testing enhanced MCP server..."
cd "$PROJECT_ROOT"
python3 scripts/mcp/enhanced-cursor-agent-mcp-server.py

if [ $? -eq 0 ]; then
    echo "✅ Enhanced MCP server test passed"
else
    echo "❌ Enhanced MCP server test failed"
    exit 1
fi

echo ""
echo "🎉 Enhanced Cursor Agent MCP Integration Setup Complete!"
echo "========================================================"
echo ""
echo "📋 Next Steps:"
echo "1. Copy the MCP configuration to your Cursor Agent setup:"
echo "   cp $CURSOR_MCP_CONFIG ~/.cursor/mcp-config.json"
echo ""
echo "2. Update the environment variables in the config with your actual credentials"
echo ""
echo "3. Restart Cursor Agent to load the new MCP server"
echo ""
echo "4. Use these tools in Cursor Agent:"
echo "   - check_database_security: Check security status of all tables"
echo "   - fix_agents_table_security: Fix agents table security issues"
echo "   - check_agents_endpoint: Test if agents endpoint is working"
echo "   - register_redis_agent: Register the Redis agent"
echo ""
echo "🔧 Available Tools:"
echo "   - Database Management: get_database_schema, test_database_connection"
echo "   - Security Analysis: check_database_security, get_security_recommendations"
echo "   - Agent Management: register_redis_agent, check_agents_endpoint"
echo "   - PRD Management: list_prds"
echo ""
echo "🚀 Ready to fix your Supabase security issues from Cursor Agent!"
