#!/bin/bash
# Organize resolution summaries with date prefixes
# Renames files to YYYY-MM-DD-description.md format for better sorting

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📂 Organizing Resolution Summaries${NC}"
echo "===================================="
echo ""

cd docs/resolution-summaries

# Function to rename with date prefix
rename_with_date() {
    local old_name="$1"
    local new_name="$2"
    
    if [ -f "$old_name" ] && [ ! -f "$new_name" ]; then
        echo -e "${GREEN}✅${NC} $old_name → $new_name"
        git mv "$old_name" "$new_name" 2>/dev/null || mv "$old_name" "$new_name"
    elif [ -f "$new_name" ]; then
        echo -e "${YELLOW}⚠️${NC}  $new_name already exists, skipping"
    else
        echo -e "${YELLOW}⚠️${NC}  $old_name not found, skipping"
    fi
}

# Rename files with proper date prefixes
echo "Renaming files to date-prefix format..."
echo ""

# Files without dates - need manual date assignment
if [ -f "agent-display-issue-resolution.md" ]; then
    echo -e "${YELLOW}⚠️  agent-display-issue-resolution.md - No date in filename${NC}"
    echo "   Please manually add date prefix: YYYY-MM-DD-agent-display-issue-resolution.md"
fi

if [ -f "secrets-management-implementation-resolution.md" ]; then
    echo -e "${YELLOW}⚠️  secrets-management-implementation-resolution.md - No date in filename${NC}"
    echo "   Please manually add date prefix: YYYY-MM-DD-secrets-management-implementation-resolution.md"
fi

# Files with dates but wrong format (nov-16-2025 instead of 2025-11-16)
rename_with_date \
    "agents-endpoint-500-error-resolution-nov-16-2025.md" \
    "2025-11-16-agents-endpoint-500-error-resolution.md"

# Files with correct date format but date at end
rename_with_date \
    "ai-agent-workflow-implementation-2025-11-27.md" \
    "2025-11-27-ai-agent-workflow-implementation.md"

rename_with_date \
    "comprehensive-linting-system-implementation-2025-11-27.md" \
    "2025-11-27-comprehensive-linting-system-implementation.md"

rename_with_date \
    "file-based-prd-system-and-redis-agent-resolution-2025-11-16.md" \
    "2025-11-16-file-based-prd-system-and-redis-agent-resolution.md"

rename_with_date \
    "mcp-database-health-check-implementation-resolution-2025-11-16.md" \
    "2025-11-16-mcp-database-health-check-implementation-resolution.md"

rename_with_date \
    "mcp-supabase-sql-execution-resolution-2025-11-16.md" \
    "2025-11-16-mcp-supabase-sql-execution-resolution.md"

rename_with_date \
    "prd-count-inconsistency-resolution-2025-11-16.md" \
    "2025-11-16-prd-count-inconsistency-resolution.md"

rename_with_date \
    "proactive-prd-syncing-implementation-resolution-2025-11-16.md" \
    "2025-11-16-proactive-prd-syncing-implementation-resolution.md"

rename_with_date \
    "redis-agent-registration-fix-resolution-2025-11-16.md" \
    "2025-11-16-redis-agent-registration-fix-resolution.md"

rename_with_date \
    "secrets-sync-database-url-fix-resolution-2025-11-16.md" \
    "2025-11-16-secrets-sync-database-url-fix-resolution.md"

rename_with_date \
    "startup-prompt-prd-sync-enhancement-2025-11-27.md" \
    "2025-11-27-startup-prompt-prd-sync-enhancement.md"

echo ""
echo -e "${GREEN}✅ Organization complete!${NC}"
echo ""
echo "Files now follow the format: YYYY-MM-DD-description.md"
echo "This allows for natural sorting by date."

