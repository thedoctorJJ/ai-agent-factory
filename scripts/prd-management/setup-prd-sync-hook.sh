#!/bin/bash
# Setup git hook to automatically sync PRDs after commit
# This enables proactive syncing for local development

set -e

HOOK_FILE=".git/hooks/post-commit"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔧 Setting up PRD sync git hook..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Create post-commit hook
cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# Post-commit hook: Auto-sync PRDs if PRD files changed

# Get list of changed files in the last commit
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

# Check if any PRD files were changed
if echo "$CHANGED_FILES" | grep -q "^prds/"; then
    echo ""
    echo "📋 PRD files changed - syncing to database..."
    echo ""
    
    # Run sync script (non-blocking, don't fail commit if sync fails)
    cd "$(git rev-parse --show-toplevel)"
    ./scripts/prd-management/sync-prds-to-database.sh || echo "⚠️  PRD sync failed (non-blocking)"
fi
EOF

chmod +x "$HOOK_FILE"

echo "✅ Git hook installed: $HOOK_FILE"
echo ""
echo "📋 The hook will automatically sync PRDs to database when PRD files are committed."
echo ""
echo "💡 To disable: rm .git/hooks/post-commit"
echo "💡 To manually sync: ./scripts/prd-management/sync-prds-to-database.sh"

