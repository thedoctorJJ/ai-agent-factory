#!/bin/bash
# Verify that PRD files and database are in sync
# Similar to verify-secrets-sync.sh but for PRDs

set -e

echo "🔍 Verifying PRD sync between files and database..."
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"

cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
SYNCED=0
MISSING_IN_DB=0
MISSING_FILES=0
DUPLICATES=0

# Get PRD files (source of truth)
PRD_FILES=$(find prds/queue -name "*.md" -type f ! -name "README.md" | sort)

if [ -z "$PRD_FILES" ]; then
    echo "${RED}❌ No PRD files found in prds/queue/${NC}"
    exit 1
fi

echo "📁 Found $(echo "$PRD_FILES" | wc -l | xargs) PRD files (source of truth)"
echo ""

# Get PRDs from database
echo "🗄️  Fetching PRDs from database..."
DB_PRDS=$(curl -s "$BACKEND_URL/api/v1/prds?limit=100" | python3 -c "
import sys, json
data = json.load(sys.stdin)
prds = data.get('prds', [])
# Output as JSON for processing
import json
print(json.dumps(prds))
" 2>/dev/null || echo "[]")

if [ "$DB_PRDS" = "[]" ] || [ -z "$DB_PRDS" ]; then
    echo "${RED}❌ Failed to fetch PRDs from database${NC}"
    exit 1
fi

DB_COUNT=$(echo "$DB_PRDS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
echo "   Found $DB_COUNT PRDs in database"
echo ""

# Extract titles from files and check sync status
echo "🔍 Checking sync status..."
echo ""

while IFS= read -r file; do
    # Extract title from file
    title=$(grep -m 1 "^## \*\*Title\*\*" "$file" -A 1 2>/dev/null | tail -1 | sed 's/^[[:space:]]*\*\*//;s/\*\*[[:space:]]*$//' | xargs)
    if [ -z "$title" ] || [ "$title" = "" ]; then
        # Try pattern: **Title** on next line
        title=$(grep -A 2 "^## \*\*Title\*\*" "$file" 2>/dev/null | grep "^\*\*" | head -1 | sed 's/^[[:space:]]*\*\*//;s/\*\*[[:space:]]*$//' | xargs)
    fi
    if [ -z "$title" ] || [ "$title" = "" ]; then
        # Fallback to filename
        title=$(basename "$file" .md | sed 's/^[0-9-]*_//')
    fi
    
    # Check if PRD exists in database (normalized title comparison)
    normalized_title=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/\*//g' | sed 's/#//g' | xargs)
    
    found=$(echo "$DB_PRDS" | python3 -c "
import sys, json
prds = json.load(sys.stdin)
normalized = '$normalized_title'
for p in prds:
    p_title = p.get('title', '').strip().lower().replace('*', '').replace('#', '').strip()
    if p_title == normalized:
        print('FOUND')
        break
" 2>/dev/null || echo "NOT_FOUND")
    
    if [ "$found" = "FOUND" ]; then
        title_display=$(echo "$title" | cut -c1-60)
        echo "${GREEN}✅${NC} $title_display"
        ((SYNCED++))
    else
        title_display=$(echo "$title" | cut -c1-60)
        echo "${YELLOW}⚠️${NC}  $title_display (not in database)"
        ((MISSING_IN_DB++))
    fi
done <<< "$PRD_FILES"

# Check for duplicates in database
echo ""
echo "🔍 Checking for duplicates in database..."
DUPLICATE_TITLES=$(echo "$DB_PRDS" | python3 -c "
import sys, json
from collections import defaultdict

prds = json.load(sys.stdin)
titles = defaultdict(list)

for p in prds:
    title = p.get('title', '').strip().lower().replace('*', '').replace('#', '').strip()
    titles[title].append((p.get('id'), p.get('title', '')))

duplicates = {k: v for k, v in titles.items() if len(v) > 1}
if duplicates:
    for norm_title, items in duplicates.items():
        print(f'{norm_title}|{len(items)}')
" 2>/dev/null || echo "")

if [ -n "$DUPLICATE_TITLES" ]; then
    echo "${RED}⚠️  Found duplicates in database:${NC}"
    while IFS='|' read -r norm_title count; do
        if [ -n "$norm_title" ]; then
            echo "   - \"$norm_title\": $count copies"
            ((DUPLICATES++))
        fi
    done <<< "$DUPLICATE_TITLES"
else
    echo "${GREEN}✅ No duplicates found${NC}"
fi

# Check for PRDs in database without files
echo ""
echo "🔍 Checking for PRDs in database without files..."
DB_ONLY=$(echo "$DB_PRDS" | python3 -c "
import sys, json
from pathlib import Path

prds = json.load(sys.stdin)
file_titles = set()

# Get file titles
for f in Path('prds/queue').glob('*.md'):
    if f.name == 'README.md':
        continue
    with open(f, 'r') as file:
        content = file.read()
        for line in content.split('\n')[:30]:
            if '## **Title**' in line or '## Title' in line:
                continue
            if line.strip().startswith('**') and line.strip().endswith('**') and len(line.strip()) > 5:
                title = line.strip().replace('**', '').strip()
                if title and title != 'Description' and title != 'Title':
                    file_titles.add(title.lower().replace('*', '').replace('#', '').strip())
                    break

# Find PRDs not in files
for p in prds:
    title = p.get('title', '').strip().lower().replace('*', '').replace('#', '').strip()
    if title not in file_titles:
        print(f\"{p.get('title', 'N/A')}|{p.get('id', 'N/A')}\")
" 2>/dev/null || echo "")

if [ -n "$DB_ONLY" ]; then
    echo "${YELLOW}⚠️  PRDs in database without files:${NC}"
    while IFS='|' read -r title prd_id; do
        if [ -n "$title" ]; then
            echo "   - $title (ID: ${prd_id:0:8}...)"
            ((MISSING_FILES++))
        fi
    done <<< "$DB_ONLY"
else
    echo "${GREEN}✅ All database PRDs have corresponding files${NC}"
fi

# Summary
echo ""
echo "=================================="
echo "📊 Sync Status Summary:"
echo "   ${GREEN}✅ In sync: $SYNCED${NC}"
if [ $MISSING_IN_DB -gt 0 ]; then
    echo "   ${YELLOW}⚠️  Missing in database: $MISSING_IN_DB${NC}"
fi
if [ $MISSING_FILES -gt 0 ]; then
    echo "   ${YELLOW}⚠️  In database but no file: $MISSING_FILES${NC}"
fi
if [ $DUPLICATES -gt 0 ]; then
    echo "   ${RED}⚠️  Duplicates in database: $DUPLICATES${NC}"
fi
echo ""

# Exit code
if [ $MISSING_IN_DB -eq 0 ] && [ $MISSING_FILES -eq 0 ] && [ $DUPLICATES -eq 0 ]; then
    echo "${GREEN}✅ All PRDs are in sync!${NC}"
    exit 0
else
    echo "${YELLOW}⚠️  PRDs are out of sync. Run ./scripts/prd-management/sync-prds-to-database.sh to fix.${NC}"
    exit 1
fi

