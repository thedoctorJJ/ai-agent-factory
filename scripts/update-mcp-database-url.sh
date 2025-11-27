#!/bin/bash
# Helper script to update DATABASE_URL in MCP config after getting password from dashboard

set -e

MCP_CONFIG="$HOME/.cursor/mcp.json"

echo "🔧 Update DATABASE_URL in MCP Configuration"
echo "=" * 60
echo ""
echo "📋 Instructions:"
echo "1. Go to: https://supabase.com/dashboard"
echo "2. Select project: ssdcbhxctakgysnayzeq"
echo "3. Go to: Settings → Database"
echo "4. Copy the 'Connection string' → 'URI'"
echo ""
echo "Paste the full DATABASE_URL here (or press Enter to edit manually):"
read -r DATABASE_URL

if [ -n "$DATABASE_URL" ]; then
    # Update the MCP config
    python3 << EOF
import json
import sys

mcp_config_path = "$MCP_CONFIG"

try:
    with open(mcp_config_path, 'r') as f:
        config = json.load(f)
    
    # Update DATABASE_URL
    if 'mcpServers' in config and 'ai-agent-factory' in config['mcpServers']:
        if 'env' not in config['mcpServers']['ai-agent-factory']:
            config['mcpServers']['ai-agent-factory']['env'] = {}
        
        config['mcpServers']['ai-agent-factory']['env']['DATABASE_URL'] = "$DATABASE_URL"
        
        with open(mcp_config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ DATABASE_URL updated successfully!")
        print(f"   File: {mcp_config_path}")
    else:
        print("❌ Could not find ai-agent-factory in MCP config")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error updating config: {e}")
    sys.exit(1)
EOF
else
    echo ""
    echo "📝 Opening config file for manual editing..."
    echo "   File: $MCP_CONFIG"
    echo ""
    echo "   Update the DATABASE_URL in the 'env' section"
    ${EDITOR:-nano} "$MCP_CONFIG"
fi

echo ""
echo "✅ Next steps:"
echo "   1. Restart Cursor (Cmd+Q, then reopen)"
echo "   2. Test with: execute_supabase_sql tool"







