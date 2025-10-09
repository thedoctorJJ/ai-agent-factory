#!/bin/bash

# Script to update OpenAI configuration in .env file

echo "🤖 Updating OpenAI configuration in .env file..."

# Backup the current .env file
cp .env .env.backup.openai
echo "✅ Created backup: .env.backup.openai"

# Update OpenAI API key (user needs to provide their own key)
echo "⚠️  Please manually update OPENAI_API_KEY in your .env file with your actual API key"
echo ""
echo "📋 Next steps:"
echo "  1. Get your API key from https://platform.openai.com/api-keys"
echo "  2. Update OPENAI_API_KEY in your .env file"
echo "  3. Run 'python3 scripts/validate-config.py' to test"

echo "✅ OpenAI configuration template ready!"