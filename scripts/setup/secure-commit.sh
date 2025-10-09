#!/bin/bash

# Secure commit script for END_CAP Agent Factory
# This script ensures sensitive files are never committed

echo "🔒 Secure Commit Script for END_CAP Agent Factory"
echo "=================================================="

# Check for sensitive files in staging area
echo "🔍 Checking for sensitive files in staging area..."

# List of sensitive file patterns (converted to regex)
SENSITIVE_PATTERNS=(
    "\.pem$"
    "-key\.json$"
    "service-account.*\.json$"
    "\.env"
    "backup"
    "api-key"
    "secret"
    "token"
    "credentials"
)

# Check if any sensitive files are staged
SENSITIVE_FOUND=false
SENSITIVE_FILES=()

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only)

for file in $STAGED_FILES; do
    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            echo "❌ Found sensitive file matching pattern: $pattern"
            echo "   File: $file"
            SENSITIVE_FOUND=true
            SENSITIVE_FILES+=("$file")
            break
        fi
    done
done

if [ "$SENSITIVE_FOUND" = true ]; then
    echo ""
    echo "🚨 SECURITY ALERT: Sensitive files detected in staging area!"
    echo ""
    echo "The following files contain sensitive information and should NOT be committed:"
    for file in "${SENSITIVE_FILES[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "🔧 To fix this:"
    echo "1. Remove sensitive files from staging:"
    for file in "${SENSITIVE_FILES[@]}"; do
        echo "   git reset HEAD '$file'"
    done
    echo ""
    echo "2. Add sensitive files to .gitignore (if not already there)"
    echo ""
    echo "3. Commit only the safe files:"
    echo "   git commit -m \"Your commit message\""
    echo ""
    echo "❌ Commit aborted for security reasons."
    exit 1
fi

echo "✅ No sensitive files detected. Proceeding with commit..."

# If we get here, it's safe to commit
if [ $# -eq 0 ]; then
    echo "📝 Please provide a commit message:"
    echo "Usage: ./scripts/setup/secure-commit.sh \"Your commit message\""
    exit 1
fi

COMMIT_MESSAGE="$1"
echo "📝 Committing with message: $COMMIT_MESSAGE"

git commit -m "$COMMIT_MESSAGE"
echo "✅ Commit successful!"