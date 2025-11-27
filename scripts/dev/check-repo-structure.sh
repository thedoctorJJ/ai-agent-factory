#!/bin/bash
# Repository Structure Checker
# Identifies loose files, misplaced items, and organization issues

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   📂 Repository Structure Check                       ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

ISSUES_FOUND=0
WARNINGS_FOUND=0

# Function to report issue
report_issue() {
    echo -e "${RED}❌ ISSUE:${NC} $1"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
}

# Function to report warning
report_warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
    WARNINGS_FOUND=$((WARNINGS_FOUND + 1))
}

# Function to report success
report_success() {
    echo -e "${GREEN}✅${NC} $1"
}

echo -e "${CYAN}Checking for loose files in root directory...${NC}"
echo ""

# Check for loose files in root (files that should be in subdirectories)
LOOSE_FILES=$(find . -maxdepth 1 -type f ! -name ".*" ! -name "*.md" ! -name "*.txt" ! -name "*.json" ! -name "*.yaml" ! -name "*.yml" ! -name "*.toml" ! -name "*.lock" ! -name "Dockerfile" ! -name "docker-compose.yml" 2>/dev/null || true)

if [ -n "$LOOSE_FILES" ]; then
    report_warning "Loose files found in root directory:"
    echo "$LOOSE_FILES" | while read -r file; do
        echo "  • $file"
    done
    echo ""
else
    report_success "No loose files in root directory"
    echo ""
fi

# Check for Python files outside backend/
echo -e "${CYAN}Checking for misplaced Python files...${NC}"
echo ""

MISPLACED_PY=$(find . -name "*.py" -type f ! -path "./backend/*" ! -path "./scripts/*" ! -path "./config/*" ! -path "./.venv/*" ! -path "./venv/*" ! -path "./backend/venv/*" ! -path "./node_modules/*" ! -path "./frontend/next-app/node_modules/*" ! -path "./tests/*" ! -path "./agents/*" 2>/dev/null || true)

if [ -n "$MISPLACED_PY" ]; then
    report_warning "Python files outside expected directories:"
    echo "$MISPLACED_PY" | while read -r file; do
        echo "  • $file"
        echo "    → Consider moving to backend/, scripts/, or config/"
    done
    echo ""
else
    report_success "All Python files are properly organized"
    echo ""
fi

# Check for JavaScript/TypeScript files outside frontend/
echo -e "${CYAN}Checking for misplaced JS/TS files...${NC}"
echo ""

MISPLACED_JS=$(find . \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \) -type f ! -path "./frontend/*" ! -path "./node_modules/*" ! -path "./frontend/next-app/node_modules/*" ! -path "./.next/*" ! -path "./backend/venv/*" ! -name "*.config.js" ! -name "*.config.ts" 2>/dev/null || true)

if [ -n "$MISPLACED_JS" ]; then
    report_warning "JS/TS files outside expected directories:"
    echo "$MISPLACED_JS" | while read -r file; do
        echo "  • $file"
        echo "    → Consider moving to frontend/ or scripts/"
    done
    echo ""
else
    report_success "All JS/TS files are properly organized"
    echo ""
fi

# Check for shell scripts outside scripts/
echo -e "${CYAN}Checking for misplaced shell scripts...${NC}"
echo ""

MISPLACED_SH=$(find . -name "*.sh" -type f ! -path "./scripts/*" ! -path "./node_modules/*" ! -path "./.git/*" ! -path "./setup/*" ! -path "./tests/*" 2>/dev/null || true)

if [ -n "$MISPLACED_SH" ]; then
    report_issue "Shell scripts outside scripts/ directory:"
    echo "$MISPLACED_SH" | while read -r file; do
        echo "  • $file"
        echo "    → Move to scripts/ subdirectory"
    done
    echo ""
else
    report_success "All shell scripts are in scripts/"
    echo ""
fi

# Check for markdown files that should be in docs/
echo -e "${CYAN}Checking for documentation organization...${NC}"
echo ""

LOOSE_DOCS=$(find . -maxdepth 1 -name "*.md" -type f ! -name "README.md" ! -name "CHANGELOG.md" ! -name "LICENSE.md" 2>/dev/null || true)

if [ -n "$LOOSE_DOCS" ]; then
    report_warning "Markdown files in root (should they be in docs/?):"
    echo "$LOOSE_DOCS" | while read -r file; do
        echo "  • $file"
    done
    echo ""
else
    report_success "Root documentation is organized"
    echo ""
fi

# Check for temporary/test files
echo -e "${CYAN}Checking for temporary/test files...${NC}"
echo ""

TEMP_FILES=$(find . -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*~" -o -name "*.bak" -o -name "*.swp" -o -name ".DS_Store" \) ! -path "./.git/*" ! -path "./node_modules/*" 2>/dev/null || true)

if [ -n "$TEMP_FILES" ]; then
    report_issue "Temporary files found (should be cleaned up):"
    echo "$TEMP_FILES" | while read -r file; do
        echo "  • $file"
    done
    echo ""
else
    report_success "No temporary files found"
    echo ""
fi

# Check for large files (> 5MB)
echo -e "${CYAN}Checking for large files...${NC}"
echo ""

LARGE_FILES=$(find . -type f -size +5M ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./.next/*" ! -path "./venv/*" ! -path "./.venv/*" 2>/dev/null || true)

if [ -n "$LARGE_FILES" ]; then
    report_warning "Large files found (> 5MB):"
    echo "$LARGE_FILES" | while read -r file; do
        SIZE=$(du -h "$file" | cut -f1)
        echo "  • $file ($SIZE)"
        echo "    → Consider if this should be tracked in git"
    done
    echo ""
else
    report_success "No large files found"
    echo ""
fi

# Check for empty directories
echo -e "${CYAN}Checking for empty directories...${NC}"
echo ""

EMPTY_DIRS=$(find . -type d -empty ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./.next/*" ! -path "./frontend/next-app/node_modules/*" ! -path "./venv/*" ! -path "./.venv/*" ! -path "./backend/venv/*" 2>/dev/null || true)

if [ -n "$EMPTY_DIRS" ]; then
    report_warning "Empty directories found:"
    echo "$EMPTY_DIRS" | while read -r dir; do
        echo "  • $dir"
        echo "    → Consider removing or adding .gitkeep"
    done
    echo ""
else
    report_success "No empty directories"
    echo ""
fi

# Check expected directory structure
echo -e "${CYAN}Verifying expected directory structure...${NC}"
echo ""

EXPECTED_DIRS=(
    "backend"
    "frontend"
    "scripts"
    "docs"
    "config"
    "prds"
    ".cursor"
    ".github"
)

for dir in "${EXPECTED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir/"
    else
        report_warning "Expected directory missing: $dir/"
    fi
done
echo ""

# Check for duplicate files (same name in different locations)
echo -e "${CYAN}Checking for potential duplicate files...${NC}"
echo ""

# Find all Python files and check for duplicates by basename (excluding venv and node_modules)
DUPLICATE_CHECK=$(find . -name "*.py" -type f ! -path "./.venv/*" ! -path "./venv/*" ! -path "./backend/venv/*" ! -path "./node_modules/*" ! -path "./frontend/next-app/node_modules/*" -exec basename {} \; | sort | uniq -d)

if [ -n "$DUPLICATE_CHECK" ]; then
    # Filter out __init__.py as it's expected
    FILTERED_DUPLICATES=$(echo "$DUPLICATE_CHECK" | grep -v "__init__.py" || true)
    
    if [ -n "$FILTERED_DUPLICATES" ]; then
        report_warning "Potential duplicate file names found:"
        echo "$FILTERED_DUPLICATES" | while read -r filename; do
            echo "  • $filename"
            find . -name "$filename" -type f ! -path "./.venv/*" ! -path "./venv/*" ! -path "./backend/venv/*" ! -path "./node_modules/*" ! -path "./frontend/next-app/node_modules/*" | while read -r path; do
                echo "    - $path"
            done
        done
        echo ""
    else
        report_success "No problematic duplicate files found"
        echo ""
    fi
else
    report_success "No duplicate files found"
    echo ""
fi

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Summary                                             ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

if [ $ISSUES_FOUND -eq 0 ] && [ $WARNINGS_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ Repository structure is clean and well-organized!${NC}"
    echo ""
    exit 0
else
    echo -e "  ${RED}Issues:   $ISSUES_FOUND${NC}"
    echo -e "  ${YELLOW}Warnings: $WARNINGS_FOUND${NC}"
    echo ""
    
    if [ $ISSUES_FOUND -gt 0 ]; then
        echo -e "${RED}❌ Critical issues found - please fix before committing${NC}"
        echo ""
        exit 1
    else
        echo -e "${YELLOW}⚠️  Warnings found - consider cleaning up${NC}"
        echo ""
        exit 0
    fi
fi

