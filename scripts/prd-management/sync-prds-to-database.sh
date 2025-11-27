#!/bin/bash
# Sync PRD files from local repository to database
# 
# NOTE: This is a LOCAL DEVELOPMENT/FALLBACK script.
# Normal workflow: GitHub → GitHub Actions → Database (automatic)
# 
# Use this script only when:
# - GitHub Actions is unavailable
# - Testing locally before pushing to GitHub
# - Manual sync needed for development
#
# Normal PRD flow:
# 1. ChatGPT/Manual → Commit to GitHub (cloud source of truth)
# 2. GitHub Actions auto-syncs to database (within 30 seconds)
# 3. git pull to sync locally (when needed)

set -e

echo "🔄 Syncing Local PRD Files to Database"
echo "=================================="
echo ""
echo "📋 Source: Local prds/queue/ (synced from GitHub)"
echo "🗄️  Target: Database"
echo "⚠️  Normal workflow uses GitHub Actions (this is a fallback)"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PRD_DIR="prds/queue"
BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"
UPLOADED=0
SKIPPED=0
FAILED=0
UPDATED=0

# Function to check if PRD is in database (normalized title comparison)
check_in_database() {
    local title="$1"
    local normalized_title=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/\*//g' | sed 's/#//g' | xargs)
    
    local response=$(curl -s "$BACKEND_URL/api/v1/prds?limit=100" | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
prds = data.get('prds', [])
normalized = '$normalized_title'
for p in prds:
    p_title = p.get('title', '').strip().lower().replace('*', '').replace('#', '').strip()
    if p_title == normalized:
        print('FOUND|' + p.get('id', ''))
        break
else:
    print('NOT_FOUND')
" 2>/dev/null || echo "ERROR")
    echo "$response"
}

# Function to upload PRD file
upload_prd() {
    local file="$1"
    local title="$2"
    
    echo "${BLUE}📤 Uploading: $title${NC}"
    
    # Upload via API using file upload endpoint (simpler and more reliable)
    response=$(curl -s -X POST "$BACKEND_URL/api/v1/prds/upload" \
        -F "file=@$file" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        prd_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', 'unknown'))" 2>/dev/null || echo "unknown")
        echo "${GREEN}   ✅ Uploaded successfully (ID: ${prd_id:0:8}...)${NC}"
        return 0
    else
        echo "${RED}   ❌ Upload failed: HTTP $http_code${NC}"
        echo "   Response: $body"
        return 1
    fi
}

# Function to update existing PRD
update_prd() {
    local file="$1"
    local title="$2"
    local prd_id="$3"
    
    # Read file content
    local content=$(cat "$file")
    
    echo "${BLUE}🔄 Updating: $title${NC}"
    
    # Update via API
    response=$(curl -s -X PUT "$BACKEND_URL/api/v1/prds/$prd_id" \
        -H "Content-Type: application/json" \
        -d "{
            \"file_content\": $(python3 -c "import json, sys; print(json.dumps(sys.stdin.read()))" <<< "$content")
        }" \
        -w "\n%{http_code}")
    
    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo "${GREEN}   ✅ Updated successfully${NC}"
        return 0
    else
        echo "${YELLOW}   ⚠️  Update failed: HTTP $http_code (may need manual update)${NC}"
        return 1
    fi
}

echo "🔍 Finding PRD files (source of truth)..."
echo ""

# Find all PRD markdown files in queue directory (source of truth)
PRD_FILES=$(find "$PRD_DIR" -name "*.md" -type f ! -name "README.md" | sort)

if [ -z "$PRD_FILES" ]; then
    echo "${RED}❌ No PRD files found in $PRD_DIR/${NC}"
    exit 1
fi

FILE_COUNT=$(echo "$PRD_FILES" | wc -l | xargs)
echo "Found $FILE_COUNT PRD files (source of truth)"
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
    db_result=$(check_in_database "$title")
    db_status=$(echo "$db_result" | cut -d'|' -f1)
    db_prd_id=$(echo "$db_result" | cut -d'|' -f2)
    
    if [ "$db_status" = "FOUND" ]; then
        # PRD exists - check if file is newer (for now, just skip - duplicate detection handles this)
        echo "${GREEN}✅${NC} $title (already in database)"
        SKIPPED=$((SKIPPED + 1))
    else
        # PRD not in database - upload it
        if upload_prd "$file" "$title"; then
            UPLOADED=$((UPLOADED + 1))
        else
            FAILED=$((FAILED + 1))
        fi
        echo ""
    fi
done <<< "$PRD_FILES"

echo "=================================="
echo "📊 Sync Summary:"
echo "   ${GREEN}✅ Uploaded: $UPLOADED${NC}"
echo "   ${GREEN}✅ Already synced: $SKIPPED${NC}"
if [ $UPDATED -gt 0 ]; then
    echo "   ${BLUE}🔄 Updated: $UPDATED${NC}"
fi
if [ $FAILED -gt 0 ]; then
    echo "   ${RED}❌ Failed: $FAILED${NC}"
fi
echo ""

# Verify final count
DB_COUNT=$(curl -s "$BACKEND_URL/api/v1/prds?limit=100" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))" 2>/dev/null || echo "0")
echo "📊 Final Status:"
echo "   Files (source of truth): $FILE_COUNT"
echo "   Database: $DB_COUNT"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "${RED}❌ Some PRDs failed to sync${NC}"
    exit 1
fi

echo "${GREEN}✅ Sync complete!${NC}"
echo ""
echo "📋 Next steps:"
echo "   1. Verify sync: ./scripts/prd-management/verify-prds-sync.sh"
echo "   2. Check for duplicates: ./scripts/prd-management/verify-prds-sync.sh"

