#!/bin/bash


set -e

echo "=== MCP Server Test Script ==="
echo ""

echo "1. Checking required environment variables..."
REQUIRED_VARS=("GITHUB_TOKEN" "OPENAI_API_KEY" "SUPABASE_SERVICE_ROLE_KEY" "GCP_SERVICE_ACCOUNT_KEY" "GITHUB_ORG_NAME" "ENDCAP_API_URL")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "   ❌ $var is NOT set"
        MISSING_VARS+=("$var")
    else
        echo "   ✅ $var is set"
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Warning: ${#MISSING_VARS[@]} environment variable(s) missing: ${MISSING_VARS[*]}"
    echo "   The MCP server may not work correctly without these."
fi

echo ""
echo "2. Testing MCP server tools/list..."

cd "$(dirname "$0")"
RESPONSE=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python3 mcp-server.py 2>&1)

if echo "$RESPONSE" | grep -q '"tools"'; then
    echo "   ✅ MCP server responded successfully"
    echo ""
    echo "3. Available tools:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | grep -A 1 '"name":' | grep '"name"' | sed 's/.*"name": "\(.*\)".*/      - \1/'
    echo ""
    echo "✅ MCP server test PASSED"
    exit 0
else
    echo "   ❌ MCP server did not respond correctly"
    echo ""
    echo "Response:"
    echo "$RESPONSE"
    echo ""
    echo "❌ MCP server test FAILED"
    exit 1
fi
