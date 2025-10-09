#!/bin/bash

# Secure commit script for END_CAP Agent Factory
# This script ensures sensitive files are never committed

echo "🔒 Secure Commit Script for END_CAP Agent Factory"
echo "=================================================="

# Check for sensitive files in staging area
echo "🔍 Checking for sensitive files in staging area..."

# List of sensitive file patterns
SENSITIVE_PATTERNS=(
    "\.pem$"
    "-key\.json$"
    "service-account.*\.json$"
    "\.env$"
    "\.env\."
    "backup"
    "api-key"
    "secret"
    "token"
    "credentials"
)

# Check if any sensitive files are staged
SENSITIVE_FOUND=false

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git diff --cached --name-only | grep -E "$pattern" >/dev/null 2>&1; then
        echo "❌ Found sensitive file matching pattern: $pattern"
        SENSITIVE_FOUND=true
    fi
done

if [ "$SENSITIVE_FOUND" = true ]; then
    echo ""
    echo "🚨 SECURITY ALERT: Sensitive files detected in staging area!"
    echo ""
echo "The following files contain sensitive information and should NOT be committed:"
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    git diff --cached --name-only | grep -E "$pattern" 2>/dev/null || true
done
    echo ""
    echo "🔧 To fix this:"
    echo "1. Remove sensitive files from staging:"
    echo "   git reset HEAD <sensitive-file>"
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
    echo "Usage: ./scripts/secure-commit.sh \"Your commit message\""
    exit 1
fi

COMMIT_MESSAGE="$1"
echo "📝 Committing with message: $COMMIT_MESSAGE"

git commit -m "$COMMIT_MESSAGE"
echo "✅ Commit successful!"
