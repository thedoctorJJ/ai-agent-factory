#!/bin/bash
# Discover all PRD files in the repository
# This script finds all PRD files and reports their status

set -e

echo "🔍 Discovering PRD Files in Repository"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PRD_DIR="prds"
TOTAL_FOUND=0

# Function to check if PRD is in database
check_in_database() {
    local title="$1"
    local response=$(curl -s "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds" | \
        python3 -c "import sys, json; data = json.load(sys.stdin); prds = [p for p in data['prds'] if p['title'].strip('*') == '$title' or '$title' in p['title']]; print('FOUND' if prds else 'NOT_FOUND')" 2>/dev/null || echo "ERROR")
    echo "$response"
}

echo "📁 Searching for PRD files in $PRD_DIR/..."
echo ""

# Find all PRD markdown files (excluding READMEs and templates)
PRD_FILES=$(find "$PRD_DIR" -name "*.md" -type f ! -name "README.md" ! -path "*/templates/*" | sort)

if [ -z "$PRD_FILES" ]; then
    echo "${RED}❌ No PRD files found in $PRD_DIR/${NC}"
    exit 1
fi

echo "Found PRD files:"
echo "----------------"
echo ""

IN_DB=0
NOT_IN_DB=0

while IFS= read -r file; do
    TOTAL_FOUND=$((TOTAL_FOUND + 1))
    
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
    
    # Get file status directory
    status_dir=$(dirname "$file" | sed "s|^$PRD_DIR/||")
    
    # Check if in database
    db_status=$(check_in_database "$title")
    
    if [ "$db_status" = "FOUND" ]; then
        echo "${GREEN}✅${NC} $file"
        echo "   Title: $title"
        echo "   Location: $status_dir/"
        echo "   Database: ${GREEN}✓ Loaded${NC}"
        IN_DB=$((IN_DB + 1))
    elif [ "$db_status" = "ERROR" ]; then
        echo "${YELLOW}⚠️${NC}  $file"
        echo "   Title: $title"
        echo "   Location: $status_dir/"
        echo "   Database: ${YELLOW}? Unknown${NC}"
    else
        echo "${RED}❌${NC} $file"
        echo "   Title: $title"
        echo "   Location: $status_dir/"
        echo "   Database: ${RED}✗ Not loaded${NC}"
        NOT_IN_DB=$((NOT_IN_DB + 1))
    fi
    echo ""
done <<< "$PRD_FILES"

echo "======================================"
echo "Summary:"
echo "  Total PRD files found: $TOTAL_FOUND"
echo "  ${GREEN}In database: $IN_DB${NC}"
echo "  ${RED}Not in database: $NOT_IN_DB${NC}"
echo ""

if [ $NOT_IN_DB -gt 0 ]; then
    echo "${YELLOW}💡 Tip: Run ./scripts/prd-management/sync-prds-to-database.sh to upload missing PRDs${NC}"
fi

