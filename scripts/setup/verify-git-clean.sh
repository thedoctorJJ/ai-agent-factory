#!/bin/bash

# Script to verify git repository is clean
# This helps Devin AI confirm the repository state

echo "🔍 Checking git repository status..."

# Check working directory
if git diff --quiet; then
    echo "✅ Working directory is clean"
else
    echo "❌ Working directory has uncommitted changes"
    git diff --name-only
    exit 1
fi

# Check staged changes
if git diff --cached --quiet; then
    echo "✅ Index is clean (no staged changes)"
else
    echo "❌ Index has staged changes"
    git diff --cached --name-only
    exit 1
fi

# Check untracked files
untracked=$(git ls-files --others --exclude-standard)
if [ -z "$untracked" ]; then
    echo "✅ No untracked files"
else
    echo "❌ Untracked files found:"
    echo "$untracked"
    exit 1
fi

echo "🎉 Git repository is completely clean!"
exit 0
