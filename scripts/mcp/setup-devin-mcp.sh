#!/bin/bash

# Setup script for Devin AI MCP Integration
# This script helps configure the MCP server for Devin AI

set -e

echo "🚀 Setting up Devin AI MCP Integration..."

# Get the current directory (should be scripts/mcp)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 MCP directory: $SCRIPT_DIR"

# Create a portable MCP config
echo "📝 Creating portable MCP configuration..."

cat > "$SCRIPT_DIR/devin-mcp-config-portable.json" << EOF
{
  "name": "AI Agent Factory - Devin Integration",
  "description": "MCP server for Devin AI to access PRDs and create agents in the AI Agent Factory platform",
  "icon": "🤖",
  "transport": "stdio",
  "command": "python3",
  "args": ["$SCRIPT_DIR/devin-mcp-server.py"],
  "secrets": {
    "ENDCAP_API_URL": "AI Agent Factory API URL (default: http://localhost:8000)",
    "GITHUB_TOKEN_TELLENAI": "GitHub personal access token for tellenai organization",
    "GITHUB_TOKEN_THEDOCTORJJ": "GitHub personal access token for thedoctorJJ organization", 
    "DEFAULT_GITHUB_ORG": "Default GitHub organization (tellenai or thedoctorJJ)",
    "SUPABASE_URL": "Supabase project URL",
    "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key"
  },
  "capabilities": [
    "get_startup_guide",
    "load_prd_data",
    "check_available_prds",
    "get_prd_details",
    "create_github_repository",
    "get_agent_library_info"
  ],
  "tools": [
    {
      "name": "get_startup_guide",
      "description": "Get the complete startup guide for Devin AI",
      "use_case": "When Devin starts cold and needs to understand its mission"
    },
    {
      "name": "load_prd_data",
      "description": "Load PRD data from AI Agent Factory into MCP cache",
      "use_case": "When Devin needs to access PRD data for processing"
    },
    {
      "name": "check_available_prds",
      "description": "Check what PRDs are available in the MCP cache",
      "use_case": "When Devin needs to see what work is available"
    },
    {
      "name": "get_prd_details",
      "description": "Get detailed information about a specific PRD",
      "use_case": "When Devin needs to understand PRD requirements"
    },
    {
      "name": "create_github_repository",
      "description": "Create a new GitHub repository for an AI agent",
      "use_case": "When Devin needs to create a repository for the agent code"
    },
    {
      "name": "get_agent_library_info",
      "description": "Get information about available agent libraries and tools",
      "use_case": "When Devin needs to understand available templates and tools"
    }
  ],
  "workflow": {
    "step_1": "Devin calls 'get_startup_guide' to understand its mission",
    "step_2": "Devin calls 'check_available_prds' to see what PRDs are ready",
    "step_3": "Devin calls 'get_prd_details' to understand specific requirements",
    "step_4": "Devin calls 'create_github_repository' to create a repo for the agent",
    "step_5": "Devin implements the agent code using the PRD requirements",
    "step_6": "Devin deploys and updates the agent status"
  }
}
EOF

echo "✅ Created portable MCP config: $SCRIPT_DIR/devin-mcp-config-portable.json"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > "$SCRIPT_DIR/.env" << EOF
# GitHub Multi-Token Configuration
GITHUB_TOKEN_TELLENAI=your_tellenai_token_here
GITHUB_TOKEN_THEDOCTORJJ=your_thedoctorjj_token_here
DEFAULT_GITHUB_ORG=thedoctorJJ

# AI Agent Factory Configuration
ENDCAP_API_URL=http://localhost:8000

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
EOF
    echo "📝 Created .env template. Please update with your actual values."
fi

echo ""
echo "🎯 Next Steps for Devin AI Setup:"
echo ""
echo "1. 📋 Import MCP Configuration:"
echo "   - Copy the contents of: $SCRIPT_DIR/devin-mcp-config-portable.json"
echo "   - Paste into Devin AI's MCP server configuration"
echo ""
echo "2. 🔑 Configure GitHub Tokens:"
echo "   - Update $SCRIPT_DIR/.env with your GitHub tokens"
echo "   - Ensure tokens have 'repo' and 'admin:org' scopes"
echo "   - For tellenai: needs 'repo' scope + organization access"
echo "   - For thedoctorJJ: needs 'repo' scope (personal account)"
echo ""
echo "3. 🚀 Test the Setup:"
echo "   - Start the MCP server: python3 $SCRIPT_DIR/devin-mcp-server.py"
echo "   - Test in Devin AI with the simple startup prompt"
echo ""
echo "📖 For detailed instructions, see: docs/setup/15-devin-mcp-real-integration.md"
echo ""
echo "✅ Setup script completed!"
