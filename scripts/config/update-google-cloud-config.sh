#!/bin/bash

# Script to update Google Cloud configuration in .env file

echo "☁️  Updating Google Cloud configuration in .env file..."

# Backup the current .env file
cp .env .env.backup.gcp
echo "✅ Created backup: .env.backup.gcp"

# Update Google Cloud configuration (user needs to provide their own credentials)
echo "⚠️  Please manually update Google Cloud credentials in your .env file:"
echo "   - GOOGLE_CLOUD_PROJECT_ID: Your Google Cloud project ID"
echo "   - GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY: Path to your service account JSON file"

echo "✅ Google Cloud configuration template ready!"
echo ""
echo "📋 Next steps:"
echo "  1. Create a Google Cloud project"
echo "  2. Enable required APIs (Cloud Run, Cloud Build, Secret Manager)"
echo "  3. Create a service account and download the JSON key"
echo "  4. Update the .env file with your actual values"
echo "  5. Run 'python3 scripts/validate-config.py' to test"