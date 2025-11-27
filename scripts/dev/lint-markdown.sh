#!/bin/bash
# Lint Markdown files

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📝 Markdown Linting${NC}"
echo "==================="
echo ""

echo -e "${YELLOW}Running markdownlint...${NC}"
echo ""

markdownlint "**/*.md" --ignore node_modules --ignore .next --ignore build --ignore dist || {
    echo -e "${RED}❌ Markdownlint found issues${NC}"
    echo "Run: markdownlint \"**/*.md\" --fix to auto-fix some issues"
    exit 1
}

echo ""
echo -e "${GREEN}✅ All markdown files passed!${NC}"

