#!/bin/bash
# Lint Python files in the backend

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🐍 Python Linting${NC}"
echo "=================="
echo ""

# Change to backend directory
cd backend

echo -e "${YELLOW}Running Black (formatter)...${NC}"
python3 -m black fastapi_app/ --check || {
    echo -e "${RED}❌ Black found formatting issues${NC}"
    echo "Run: python3 -m black fastapi_app/ --fix to auto-fix"
    exit 1
}
echo -e "${GREEN}✅ Black passed${NC}"
echo ""

echo -e "${YELLOW}Running isort (import sorter)...${NC}"
python3 -m isort fastapi_app/ --check-only || {
    echo -e "${RED}❌ isort found import issues${NC}"
    echo "Run: python3 -m isort fastapi_app/ to auto-fix"
    exit 1
}
echo -e "${GREEN}✅ isort passed${NC}"
echo ""

echo -e "${YELLOW}Running Flake8 (linter)...${NC}"
python3 -m flake8 fastapi_app/ || {
    echo -e "${RED}❌ Flake8 found linting issues${NC}"
    exit 1
}
echo -e "${GREEN}✅ Flake8 passed${NC}"
echo ""

echo -e "${YELLOW}Running MyPy (type checker)...${NC}"
python3 -m mypy fastapi_app/ || {
    echo -e "${YELLOW}⚠️  MyPy found type issues (non-blocking)${NC}"
}
echo ""

echo -e "${GREEN}✅ Python linting complete!${NC}"

