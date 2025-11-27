#!/bin/bash
# Check which linting tools are available
# AI agents should run this at session start

echo "🔍 Checking Linting Tools Status"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TOOLS_AVAILABLE=0
TOOLS_MISSING=0

# Function to check if command exists
check_tool() {
    local tool=$1
    local name=$2
    
    if command -v "$tool" &> /dev/null; then
        echo -e "${GREEN}✅${NC} $name"
        TOOLS_AVAILABLE=$((TOOLS_AVAILABLE + 1))
        return 0
    else
        echo -e "${RED}❌${NC} $name"
        TOOLS_MISSING=$((TOOLS_MISSING + 1))
        return 1
    fi
}

echo "Python Linters:"
check_tool "black" "Black (formatter)"
check_tool "flake8" "Flake8 (linter)"
check_tool "mypy" "MyPy (type checker)"
check_tool "isort" "isort (import sorter)"
check_tool "pylint" "Pylint (linter)"

echo ""
echo "JavaScript/TypeScript Linters:"
check_tool "eslint" "ESLint"
check_tool "prettier" "Prettier"

echo ""
echo "Shell Linters:"
check_tool "shellcheck" "ShellCheck"

echo ""
echo "Markdown Linters:"
check_tool "markdownlint" "Markdownlint"

echo ""
echo "Other Tools:"
check_tool "pre-commit" "Pre-commit hooks"

echo ""
echo "=================================="
echo "Summary:"
echo -e "  ${GREEN}Available: $TOOLS_AVAILABLE${NC}"
echo -e "  ${RED}Missing:   $TOOLS_MISSING${NC}"
echo ""

if [ $TOOLS_MISSING -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Some linting tools are missing${NC}"
    echo ""
    echo "Linting System Status: 🚧 INCOMPLETE"
    echo ""
    echo "📋 Recommendations:"
    echo "  1. Review .cursor/LINTING_SYSTEM.md for current status"
    echo "  2. Use available tools for minimal linting"
    echo "  3. Suggest setting up comprehensive linting system"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ All linting tools are available!${NC}"
    echo ""
    echo "Linting System Status: ✅ COMPLETE"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Run ./scripts/dev/lint-all.sh to lint all files"
    echo "  2. Follow AI_AGENT_WORKFLOW.md for linting during development"
    echo ""
    exit 0
fi

