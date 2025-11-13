#!/bin/bash
# Generate TypeScript types from OpenAPI specification

set -e

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"
API_SPEC="$PROJECT_ROOT/api-spec/openapi.json"
OUTPUT_FILE="$PROJECT_ROOT/frontend/next-app/types/api.ts"

echo "🚀 Generating TypeScript types from OpenAPI specification..."
echo "=" * 50

# Check if openapi-typescript is installed
if ! command -v npx &> /dev/null; then
    echo "❌ npx is not installed. Please install Node.js and npm."
    exit 1
fi

# Check if openapi.json exists
if [ ! -f "$API_SPEC" ]; then
    echo "❌ OpenAPI spec not found at: $API_SPEC"
    echo "   Run: python3 scripts/api/generate-openapi-spec.py"
    exit 1
fi

# Generate types
echo "📝 Generating TypeScript types..."
cd "$PROJECT_ROOT/frontend/next-app"

npx --yes openapi-typescript "$API_SPEC" -o "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ TypeScript types generated successfully!"
    echo "   Output: $OUTPUT_FILE"
    echo ""
    echo "📊 Type file stats:"
    wc -l "$OUTPUT_FILE" | awk '{print "   Lines:", $1}'
else
    echo "❌ Failed to generate TypeScript types"
    exit 1
fi

