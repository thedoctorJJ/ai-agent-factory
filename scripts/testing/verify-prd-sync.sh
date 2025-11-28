#!/bin/bash

# Verify PRD sync across all 4 locations
# Usage: ./scripts/testing/verify-prd-sync.sh

echo "📊 Verifying PRD sync across all 4 locations..."
echo ""

# Get counts from each location
GITHUB_REMOTE=$(git ls-tree -r --name-only origin/main prds/queue/ 2>/dev/null | grep "\.md$" | grep -v README | wc -l | xargs)
LOCAL=$(find prds/queue -name "*.md" -type f ! -name "README.md" | wc -l | xargs)
DB=$(curl -s "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/prds?limit=100" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))" 2>/dev/null || echo "0")
WEB=$DB

echo "   GitHub remote:  $GITHUB_REMOTE PRDs"
echo "   Local:          $LOCAL PRDs"
echo "   Database:      $DB PRDs"
echo "   Website:       $WEB PRDs"
echo ""

# Check if all are in sync
if [ "$GITHUB_REMOTE" = "$LOCAL" ] && [ "$LOCAL" = "$DB" ] && [ "$DB" = "$WEB" ]; then
    echo "✅ All 4 locations are in sync!"
    exit 0
else
    echo "⚠️  Locations are NOT in sync!"
    echo ""
    echo "Differences:"
    [ "$GITHUB_REMOTE" != "$LOCAL" ] && echo "   GitHub ($GITHUB_REMOTE) ≠ Local ($LOCAL)"
    [ "$LOCAL" != "$DB" ] && echo "   Local ($LOCAL) ≠ Database ($DB)"
    [ "$DB" != "$WEB" ] && echo "   Database ($DB) ≠ Website ($WEB)"
    exit 1
fi

