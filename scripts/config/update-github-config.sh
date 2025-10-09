#!/bin/bash

# Script to update GitHub configuration in .env file

echo "🐙 Updating GitHub configuration in .env file..."

# Backup the current .env file
cp .env .env.backup.github
echo "✅ Created backup: .env.backup.github"

# Update GitHub configuration (user needs to provide their own credentials)
echo "⚠️  Please manually update GitHub credentials in your .env file:"
echo "   - GITHUB_APP_ID: Your GitHub App ID"
echo "   - GITHUB_PRIVATE_KEY: Path to your GitHub App private key file"
echo "   - GITHUB_WEBHOOK_SECRET: Your GitHub App webhook secret"
echo "   - GITHUB_ORG_NAME: Your GitHub organization name"

echo "✅ GitHub configuration template ready!"
echo ""
echo "📋 Next steps:"
echo "  1. Create a GitHub App in your organization"
echo "  2. Set appropriate permissions (Contents, Metadata, Pull requests, Issues)"
echo "  3. Generate and download the private key"
echo "  4. Update the .env file with your actual values"
echo "  5. Run 'python3 scripts/validate-config.py' to test"