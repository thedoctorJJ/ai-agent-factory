#!/bin/bash
# Validate API responses against OpenAPI specification

set -e

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"
API_SPEC="$PROJECT_ROOT/api-spec/openapi.json"
API_URL="${1:-https://ai-agent-factory-backend-952475323593.us-central1.run.app}"

echo "🔍 Validating API contract..."
echo "=" * 50
echo "   API URL: $API_URL"
echo "   Spec: $API_SPEC"
echo ""

# Check if spec exists
if [ ! -f "$API_SPEC" ]; then
    echo "❌ OpenAPI spec not found at: $API_SPEC"
    echo "   Run: python3 scripts/api/generate-openapi-spec.py"
    exit 1
fi

# Check if swagger-cli is available
if ! command -v npx &> /dev/null; then
    echo "❌ npx is not installed. Please install Node.js and npm."
    exit 1
fi

# Validate the spec itself
echo "1️⃣ Validating OpenAPI specification..."
if npx --yes swagger-cli validate "$API_SPEC" 2>&1; then
    echo "   ✅ OpenAPI spec is valid"
else
    echo "   ❌ OpenAPI spec validation failed"
    exit 1
fi

echo ""
echo "2️⃣ Testing API endpoints against spec..."
echo "   (This is a basic check - full validation requires additional tools)"

# Test a few key endpoints
ENDPOINTS=(
    "/api/v1/health"
    "/api/v1/agents"
    "/api/v1/prds"
)

for endpoint in "${ENDPOINTS[@]}"; do
    echo -n "   Testing $endpoint... "
    if curl -sf "${API_URL}${endpoint}" > /dev/null; then
        echo "✅"
    else
        echo "❌"
    fi
done

echo ""
echo "✅ Basic validation complete"
echo ""
echo "💡 For full contract validation, consider using:"
echo "   - schemathesis (Python): pip install schemathesis"
echo "   - dredd (Node.js): npm install -g dredd"

