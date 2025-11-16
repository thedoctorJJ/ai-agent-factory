#!/bin/bash
# Pull secrets from Google Cloud Secrets Manager to local storage
# EMERGENCY USE ONLY: Use when local encrypted storage is lost
# WARNING: This will overwrite local secrets!

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"

echo "⚠️  WARNING: This will overwrite local encrypted storage!"
echo "   This should only be used if local storage is lost."
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Cancelled."
    exit 1
fi

echo ""
echo "📥 Pulling secrets from Google Cloud Secrets Manager..."
echo ""

# Required secrets
REQUIRED_SECRETS=(
    "SUPABASE_URL"
    "SUPABASE_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
    "OPENAI_API_KEY"
    "GITHUB_TOKEN"
    "GOOGLE_CLOUD_PROJECT_ID"
)

# Create temporary .env file
TEMP_ENV="/tmp/pulled_secrets.env"
echo "# Secrets pulled from Google Cloud Secrets Manager" > "$TEMP_ENV"
echo "# Date: $(date)" >> "$TEMP_ENV"
echo "" >> "$TEMP_ENV"

PULLED=0
MISSING=0

for SECRET in "${REQUIRED_SECRETS[@]}"; do
    if gcloud secrets describe "$SECRET" --project="$PROJECT_ID" &>/dev/null; then
        VALUE=$(gcloud secrets versions access latest --secret="$SECRET" --project="$PROJECT_ID" 2>/dev/null || echo "")
        if [ -n "$VALUE" ]; then
            echo "$SECRET=$VALUE" >> "$TEMP_ENV"
            echo "✅ Pulled: $SECRET"
            ((PULLED++))
        else
            echo "⚠️  $SECRET: Secret exists but has no value"
            ((MISSING++))
        fi
    else
        echo "❌ $SECRET: Not found in cloud"
        ((MISSING++))
    fi
done

if [ $PULLED -eq 0 ]; then
    echo ""
    echo "❌ No secrets found in cloud!"
    rm -f "$TEMP_ENV"
    exit 1
fi

echo ""
echo "📦 Importing to local encrypted storage..."
python3 config/secure-api-manager.py import "$TEMP_ENV"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Secrets imported to local storage!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Verify: python3 config/secure-api-manager.py list"
    echo "   2. Create .env: python3 config/secure-api-manager.py create"
else
    echo ""
    echo "❌ Failed to import secrets!"
    exit 1
fi

# Cleanup
rm -f "$TEMP_ENV"

echo ""
echo "✅ Pull complete! Local storage restored from cloud."

