#!/bin/bash
# Update DATABASE_URL in MCP config with new password

set -e

MCP_CONFIG="$HOME/.cursor/mcp.json"

echo "🔧 Update DATABASE_URL in MCP Configuration"
echo "============================================================"
echo ""
echo "Enter your new database password:"
read -s DB_PASSWORD

if [ -z "$DB_PASSWORD" ]; then
    echo "❌ Password cannot be empty"
    exit 1
fi

# Build the DATABASE_URL
DATABASE_URL="postgresql://postgres:${DB_PASSWORD}@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres"

echo ""
echo "Updating MCP configuration..."

python3 << EOF
import json
import sys

mcp_config_path = "$MCP_CONFIG"

try:
    with open(mcp_config_path, 'r') as f:
        config = json.load(f)
    
    # Ensure the structure exists
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    if 'ai-agent-factory' not in config['mcpServers']:
        config['mcpServers']['ai-agent-factory'] = {
            "command": "python3",
            "args": ["/Users/jason/Repositories/ai-agent-factory/scripts/mcp/cursor-agent-mcp-server.py"],
            "env": {}
        }
    if 'env' not in config['mcpServers']['ai-agent-factory']:
        config['mcpServers']['ai-agent-factory']['env'] = {}
    
    # Update DATABASE_URL
    config['mcpServers']['ai-agent-factory']['env']['DATABASE_URL'] = "$DATABASE_URL"
    
    with open(mcp_config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ DATABASE_URL updated successfully!")
    print(f"   File: {mcp_config_path}")
    print(f"   Format: postgresql://postgres:***@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres")
        
except Exception as e:
    print(f"❌ Error updating config: {e}")
    sys.exit(1)
EOF

echo ""
echo "✅ Configuration updated!"
echo ""
echo "📋 Next steps:"
echo "   1. Restart Cursor (Cmd+Q, then reopen)"
echo "   2. Test the MCP server with: execute_supabase_sql tool"







