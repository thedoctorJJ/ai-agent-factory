#!/bin/bash
# Run all linters

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}   🔍 AI Agent Factory - Comprehensive Linting         ${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

FAILED=0

# Python
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if ./scripts/dev/lint-python.sh; then
    echo -e "${GREEN}✅ Python linting passed${NC}"
else
    echo -e "${RED}❌ Python linting failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Frontend
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if ./scripts/dev/lint-frontend.sh; then
    echo -e "${GREEN}✅ Frontend linting passed${NC}"
else
    echo -e "${RED}❌ Frontend linting failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Shell scripts
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if ./scripts/dev/lint-scripts.sh; then
    echo -e "${GREEN}✅ Shell script linting passed${NC}"
else
    echo -e "${RED}❌ Shell script linting failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Markdown
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if ./scripts/dev/lint-markdown.sh; then
    echo -e "${GREEN}✅ Markdown linting passed${NC}"
else
    echo -e "${RED}❌ Markdown linting failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Summary
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All linting passed!${NC}"
    echo -e "${GREEN}✅ Python ✅ Frontend ✅ Shell Scripts ✅ Markdown${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED category/categories failed${NC}"
    echo ""
    echo -e "${YELLOW}To auto-fix some issues:${NC}"
    echo "  Python:     python3 -m black backend/fastapi_app/ && python3 -m isort backend/fastapi_app/"
    echo "  Frontend:   cd frontend/next-app && npx prettier --write \"**/*.{ts,tsx,js,jsx}\" && npx eslint \"**/*.{ts,tsx,js,jsx}\" --fix"
    echo "  Markdown:   markdownlint \"**/*.md\" --fix"
    exit 1
fi

