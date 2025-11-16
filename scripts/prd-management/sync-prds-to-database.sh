#!/bin/bash
# Sync PRD files from repository to database
# This script uploads all PRD files that aren't in the database

set -e

echo "🔄 Syncing PRD Files to Database"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PRD_DIR="prds"
BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"
UPLOADED=0
SKIPPED=0
FAILED=0

# Function to check if PRD is in database
check_in_database() {
    local title="$1"
    local response=$(curl -s "$BACKEND_URL/api/v1/prds" | \
        python3 -c "import sys, json; data = json.load(sys.stdin); prds = [p for p in data['prds'] if p['title'].strip('*') == '$title' or '$title' in p['title']]; print('FOUND' if prds else 'NOT_FOUND')" 2>/dev/null || echo "ERROR")
    echo "$response"
}

# Function to upload PRD file
upload_prd() {
    local file="$1"
    local title="$2"
    
    echo "${BLUE}📤 Uploading: $title${NC}"
    
    response=$(curl -s -X POST "$BACKEND_URL/api/v1/prds/upload" \
        -F "file=@$file" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        prd_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "unknown")
        echo "${GREEN}   ✅ Uploaded successfully (ID: ${prd_id:0:8}...)${NC}"
        return 0
    else
        echo "${RED}   ❌ Upload failed: HTTP $http_code${NC}"
        echo "   Response: $body"
        return 1
    fi
}

echo "🔍 Finding PRD files..."
echo ""

# Find all PRD markdown files (excluding READMEs and templates)
PRD_FILES=$(find "$PRD_DIR" -name "*.md" -type f ! -name "README.md" ! -path "*/templates/*" | sort)

if [ -z "$PRD_FILES" ]; then
    echo "${RED}❌ No PRD files found in $PRD_DIR/${NC}"
    exit 1
fi

echo "Found $(echo "$PRD_FILES" | wc -l | xargs) PRD files"
echo ""

while IFS= read -r file; do
    # Extract title from file - try multiple patterns
    title=$(grep -m 1 "^## \*\*Title\*\*" "$file" -A 1 2>/dev/null | tail -1 | sed 's/^[[:space:]]*\*\*//;s/\*\*[[:space:]]*$//' | xargs)
    if [ -z "$title" ] || [ "$title" = "" ]; then
        # Try pattern: **Title** on next line
        title=$(grep -A 2 "^## \*\*Title\*\*" "$file" 2>/dev/null | grep "^\*\*" | head -1 | sed 's/^[[:space:]]*\*\*//;s/\*\*[[:space:]]*$//' | xargs)
    fi
    if [ -z "$title" ] || [ "$title" = "" ]; then
        # Fallback to filename
        title=$(basename "$file" .md | sed 's/^[0-9-]*_//')
    fi
    
    # Check if already in database
    db_status=$(check_in_database "$title")
    
    if [ "$db_status" = "FOUND" ]; then
        echo "${YELLOW}⏭️  Skipping: $title (already in database)${NC}"
        SKIPPED=$((SKIPPED + 1))
    else
        if upload_prd "$file" "$title"; then
            UPLOADED=$((UPLOADED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        echo ""
    fi
done <<< "$PRD_FILES"

echo "=================================="
echo "Sync Summary:"
echo "  ${GREEN}Uploaded: $UPLOADED${NC}"
echo "  ${YELLOW}Skipped: $SKIPPED${NC}"
echo "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -gt 0 ]; then
    exit 1
fi

