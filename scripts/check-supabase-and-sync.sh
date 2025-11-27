#!/bin/bash
# Check Supabase Status and Sync PRDs
# This script detects if Supabase is paused and guides user to unpause it

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔍 Checking Supabase Status and PRD Count"
echo "=========================================="
echo ""

# Function to check if Supabase is accessible
check_supabase_connection() {
    echo "${BLUE}🔌 Testing Supabase connection...${NC}"
    
    # Try to connect via health check script
    if python3 scripts/health-check-mcp-database.py 2>&1 | grep -q "Database (via MCP): ✅ PASS"; then
        echo "${GREEN}✅ Supabase is accessible${NC}"
        return 0
    else
        echo "${RED}❌ Supabase connection failed${NC}"
        return 1
    fi
}

# Function to check PRD count
check_prd_count() {
    echo ""
    echo "${BLUE}📊 Checking PRD count in database...${NC}"
    
    # Count actual PRD files in queue (source of truth)
    FILE_COUNT=$(find prds/queue -name "*.md" -type f ! -name "README.md" | wc -l | xargs)
    
    # Get database count
    BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"
    DB_COUNT=$(curl -s "$BACKEND_URL/api/v1/prds?limit=100" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))" 2>/dev/null || echo "0")
    
    echo "   Database PRDs: $DB_COUNT"
    echo "   Expected PRDs: $FILE_COUNT (files in prds/queue/)"
    
    if [ "$DB_COUNT" = "$FILE_COUNT" ]; then
        echo "${GREEN}   ✅ PRD count is correct${NC}"
        return 0
    elif [ "$DB_COUNT" = "0" ]; then
        echo "${YELLOW}   ⚠️  PRD count is 0 - database needs sync${NC}"
        return 1
    else
        echo "${YELLOW}   ⚠️  PRD count mismatch (expected $FILE_COUNT, got $DB_COUNT)${NC}"
        return 2
    fi
}

# Function to sync PRDs
sync_prds() {
    echo ""
    echo "${BLUE}🔄 Syncing PRDs from files to database...${NC}"
    ./scripts/prd-management/sync-prds-to-database.sh
}

# Main logic
if ! check_supabase_connection; then
    echo ""
    echo "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${RED}⚠️  SUPABASE IS PAUSED OR UNREACHABLE${NC}"
    echo "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "${YELLOW}📋 To unpause Supabase:${NC}"
    echo "   1. Go to: https://supabase.com/dashboard/project/ssdcbhxctakgysnayzeq"
    echo "   2. Click the 'Resume Project' or 'Unpause' button"
    echo "   3. Wait ~1-2 minutes for database to come online"
    echo "   4. Re-run this script: ./scripts/check-supabase-and-sync.sh"
    echo ""
    echo "${BLUE}💡 Why this happens:${NC}"
    echo "   Supabase Free Tier automatically pauses projects after inactivity"
    echo "   This is expected behavior and happens frequently"
    echo ""
    exit 1
fi

# Check PRD count
echo ""
check_prd_count
PRD_STATUS=$?

if [ $PRD_STATUS -eq 0 ]; then
    # PRD count is correct
    FILE_COUNT=$(find prds/queue -name "*.md" -type f ! -name "README.md" | wc -l | xargs)
    echo ""
    echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${GREEN}✅ All systems operational!${NC}"
    echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "   ✅ Supabase: Connected"
    echo "   ✅ PRD Count: $FILE_COUNT (correct)"
    echo ""
elif [ $PRD_STATUS -eq 1 ]; then
    # PRD count is 0 - need to sync
    echo ""
    echo "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${YELLOW}⚠️  DATABASE NEEDS SYNC${NC}"
    echo "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "${BLUE}Supabase was recently resumed and database is empty.${NC}"
    echo "${BLUE}Syncing PRDs from files (source of truth)...${NC}"
    echo ""
    
    if sync_prds; then
        FILE_COUNT=$(find prds/queue -name "*.md" -type f ! -name "README.md" | wc -l | xargs)
        echo ""
        echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo "${GREEN}✅ PRD sync complete!${NC}"
        echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo "   ✅ Supabase: Connected"
        echo "   ✅ PRD Count: $FILE_COUNT (synced)"
        echo ""
    else
        echo ""
        echo "${RED}❌ PRD sync failed${NC}"
        exit 1
    fi
else
    # PRD count mismatch - unexpected
    echo ""
    echo "${YELLOW}⚠️  Unexpected PRD count - manual review recommended${NC}"
    echo ""
fi

