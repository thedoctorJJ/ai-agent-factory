#!/bin/bash
# Lint JavaScript/TypeScript files in the frontend

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}⚛️  Frontend Linting${NC}"
echo "==================="
echo ""

# Change to frontend directory
cd frontend/next-app

echo -e "${YELLOW}Running Prettier (formatter)...${NC}"
npx prettier --check "**/*.{ts,tsx,js,jsx,json,css}" || {
    echo -e "${RED}❌ Prettier found formatting issues${NC}"
    echo "Run: npx prettier --write \"**/*.{ts,tsx,js,jsx,json,css}\" to auto-fix"
    exit 1
}
echo -e "${GREEN}✅ Prettier passed${NC}"
echo ""

echo -e "${YELLOW}Running ESLint (linter)...${NC}"
npx eslint "**/*.{ts,tsx,js,jsx}" --max-warnings 0 || {
    echo -e "${RED}❌ ESLint found linting issues${NC}"
    echo "Run: npx eslint \"**/*.{ts,tsx,js,jsx}\" --fix to auto-fix some issues"
    exit 1
}
echo -e "${GREEN}✅ ESLint passed${NC}"
echo ""

echo -e "${YELLOW}Running TypeScript type check...${NC}"
npx tsc --noEmit || {
    echo -e "${RED}❌ TypeScript found type errors${NC}"
    exit 1
}
echo -e "${GREEN}✅ TypeScript passed${NC}"
echo ""

echo -e "${GREEN}✅ Frontend linting complete!${NC}"

