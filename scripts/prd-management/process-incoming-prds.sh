#!/bin/bash
# Process all PRD files in the incoming folder

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INCOMING_DIR="$PROJECT_ROOT/prds/incoming"
BACKEND_URL="${BACKEND_URL:-https://ai-agent-factory-backend-952475323593.us-central1.run.app}"

echo "🔍 Processing PRD files in incoming folder..."
echo ""

# Check if incoming directory exists
if [ ! -d "$INCOMING_DIR" ]; then
    echo "${RED}❌ Incoming directory not found: $INCOMING_DIR${NC}"
    exit 1
fi

# Find all .md files (excluding README.md)
PRD_FILES=$(find "$INCOMING_DIR" -name "*.md" -type f ! -name "README.md" | sort)

if [ -z "$PRD_FILES" ]; then
    echo "${YELLOW}⚠️  No PRD files found in $INCOMING_DIR${NC}"
    exit 0
fi

FILE_COUNT=$(echo "$PRD_FILES" | wc -l | xargs)
echo "Found $FILE_COUNT PRD file(s) to process"
echo ""

UPLOADED=0
FAILED=0

while IFS= read -r file; do
    filename=$(basename "$file")
    echo "${BLUE}📤 Processing: $filename${NC}"
    
    # Upload via API
    response=$(curl -s -X POST "$BACKEND_URL/api/v1/prds/upload" \
        -F "file=@$file" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        prd_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', 'unknown'))" 2>/dev/null || echo "unknown")
        title=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('title', 'unknown'))" 2>/dev/null || echo "unknown")
        
        echo "${GREEN}   ✅ Uploaded successfully${NC}"
        echo "   Title: $title"
        echo "   ID: ${prd_id:0:8}..."
        
        # Move to uploaded directory
        uploaded_path="$PROJECT_ROOT/prds/uploaded/$filename"
        mv "$file" "$uploaded_path"
        echo "   📁 Moved to: prds/uploaded/$filename"
        
        UPLOADED=$((UPLOADED + 1))
    else
        echo "${RED}   ❌ Upload failed: HTTP $http_code${NC}"
        echo "   Response: $body"
        FAILED=$((FAILED + 1))
    fi
    echo ""
done <<< "$PRD_FILES"

echo "=================================="
echo "📊 Processing Summary:"
echo "   ${GREEN}✅ Uploaded: $UPLOADED${NC}"
if [ $FAILED -gt 0 ]; then
    echo "   ${RED}❌ Failed: $FAILED${NC}"
fi
echo ""



