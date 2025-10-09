#!/bin/bash

# Install pre-commit hook to prevent sensitive files from being committed

echo "🔒 Installing pre-commit security hook..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create the pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook to prevent sensitive files from being committed

echo "🔒 Running security check..."

# List of sensitive file patterns
SENSITIVE_PATTERNS=(
    "*.pem"
    "*-key.json"
    "*service-account*.json"
    ".env*"
    "*backup*"
    "*api-key*"
    "*secret*"
    "*token*"
    "*credentials*"
)

# Check if any sensitive files are staged
SENSITIVE_FOUND=false

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git diff --cached --name-only | grep -q "$pattern"; then
        echo "❌ SECURITY ALERT: Found sensitive file matching pattern: $pattern"
        SENSITIVE_FOUND=true
    fi
done

if [ "$SENSITIVE_FOUND" = true ]; then
    echo ""
    echo "🚨 COMMIT BLOCKED: Sensitive files detected!"
    echo ""
    echo "The following files contain sensitive information:"
    git diff --cached --name-only | grep -E "($(IFS="|"; echo "${SENSITIVE_PATTERNS[*]}"))"
    echo ""
    echo "🔧 To fix this:"
    echo "1. Remove sensitive files from staging:"
    echo "   git reset HEAD <sensitive-file>"
    echo ""
    echo "2. Use the secure commit script:"
    echo "   ./scripts/secure-commit.sh \"Your commit message\""
    echo ""
    echo "❌ Commit blocked for security reasons."
    exit 1
fi

echo "✅ Security check passed. No sensitive files detected."
exit 0
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit security hook installed successfully!"
echo ""
echo "🔒 This hook will automatically prevent sensitive files from being committed."
echo "   If you need to bypass it temporarily, use: git commit --no-verify"
echo ""
echo "📝 For safe commits, use: ./scripts/secure-commit.sh \"Your message\""
