#!/bin/bash

# Script to add Devin AI configuration to .env file

echo "🤖 Adding Devin AI configuration to .env file..."

# Backup the current .env file
cp .env .env.backup.devin
echo "✅ Created backup: .env.backup.devin"

# Add Devin AI configuration after OpenAI section
sed -i '' '/^OPENAI_API_KEY=/a\
\
# Devin AI Configuration\
DEVIN_AI_API_KEY=your-devin-ai-api-key\
DEVIN_AI_BASE_URL=https://api.devin.ai\
DEVIN_AI_MODEL=devin-ai\
DEVIN_AI_TIMEOUT=300' .env

echo "✅ Devin AI configuration added successfully!"
echo ""
echo "📋 Added configuration:"
echo "  - DEVIN_AI_API_KEY: [placeholder - add your actual key]"
echo "  - DEVIN_AI_BASE_URL: https://api.devin.ai"
echo "  - DEVIN_AI_MODEL: devin-ai"
echo "  - DEVIN_AI_TIMEOUT: 300"
echo ""
echo "🔧 Next steps:"
echo "  1. Get your Devin AI API key from https://devin.ai"
echo "  2. Replace 'your-devin-ai-api-key' with your actual key"
echo "  3. Run 'python3 scripts/validate-config.py' to test"
