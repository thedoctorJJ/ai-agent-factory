#!/bin/bash
# Lint shell scripts

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🐚 Shell Script Linting${NC}"
echo "======================="
echo ""

echo -e "${YELLOW}Running ShellCheck...${NC}"
echo ""

SCRIPTS=$(find scripts/ -name "*.sh" -type f)
FAILED=0

for script in $SCRIPTS; do
    echo -n "Checking $script... "
    if shellcheck "$script"; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All shell scripts passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED script(s) have linting issues${NC}"
    exit 1
fi

