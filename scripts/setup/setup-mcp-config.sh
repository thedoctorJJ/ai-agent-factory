#!/bin/bash

echo "🔧 Setting up MCP Server Configuration for AI Agent Factory"
echo "=========================================================="

# Get the current directory
CURRENT_DIR=$(pwd)
MCP_SERVER_PATH="$CURRENT_DIR/scripts/mcp/mcp-server.py"

echo "📁 Current directory: $CURRENT_DIR"
echo "📁 MCP Server path: $MCP_SERVER_PATH"

# Check if MCP server exists
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at: $MCP_SERVER_PATH"
    exit 1
fi

echo "✅ MCP server found"

# Create MCP configuration for local use
cat > mcp-config-local.json << EOF
{
  "mcpServers": {
    "ai-agent-factory": {
      "command": "python3",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "GITHUB_TOKEN": "your-github-token",
        "SUPABASE_SERVICE_ROLE_KEY": "your-supabase-service-role-key", 
        "GCP_SERVICE_ACCOUNT_KEY": "your-gcp-service-account-key",
        "GITHUB_ORG_NAME": "thedoctorJJ",
        "OPENAI_API_KEY": "your-openai-api-key",
        "ENDCAP_API_URL": "http://localhost:8000"
      }
    }
  }
}
EOF

echo "✅ Created mcp-config-local.json"

# Test the MCP server
echo "🧪 Testing MCP server..."
python3 "$MCP_SERVER_PATH" --test 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ MCP server test passed"
else
    echo "⚠️  MCP server test failed (this might be normal for stdio mode)"
fi

echo ""
echo "📋 Next steps:"
echo "1. Copy the configuration from mcp-config-local.json"
echo "2. Add it to your MCP CLI configuration"
echo "3. Replace the placeholder values with your actual API keys"
echo ""
echo "🔗 MCP CLI Configuration Location:"
echo "   - macOS: ~/.config/mcp/config.json"
echo "   - Linux: ~/.config/mcp/config.json"
echo "   - Windows: %APPDATA%/mcp/config.json"
echo ""
echo "📄 Configuration file created: mcp-config-local.json"
