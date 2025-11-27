#!/bin/bash
# Sync secrets from local encrypted storage to Google Cloud Secrets Manager
# This script ensures cloud secrets match local secrets (source of truth)

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"

echo "🔄 Syncing secrets from local storage to Google Cloud Secrets Manager..."
echo ""

# Enable Secrets Manager API (if not already enabled)
gcloud services enable secretmanager.googleapis.com --project="$PROJECT_ID" &>/dev/null || true

# Required secrets
REQUIRED_SECRETS=(
    "SUPABASE_URL"
    "SUPABASE_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
    "OPENAI_API_KEY"
    "GITHUB_TOKEN"
    "GOOGLE_CLOUD_PROJECT_ID"
)

echo "📦 Loading secrets from local encrypted storage..."
python3 scripts/load-secrets-helper.py | while IFS='|' read -r key value; do
    if [ -n "$key" ] && [ -n "$value" ]; then
        # Check if secret already exists
        if gcloud secrets describe "$key" --project="$PROJECT_ID" &>/dev/null; then
            # Get current version value
            CURRENT_VALUE=$(gcloud secrets versions access latest --secret="$key" --project="$PROJECT_ID" 2>/dev/null || echo "")
            
            if [ "$CURRENT_VALUE" = "$value" ]; then
                echo "✅ $key: Already in sync"
            else
                echo "🔄 $key: Updating (value changed)"
                echo -n "$value" | gcloud secrets versions add "$key" \
                    --data-file=- \
                    --project="$PROJECT_ID" > /dev/null
                echo "   ✅ Updated"
            fi
        else
            echo "➕ $key: Creating new secret"
            echo -n "$value" | gcloud secrets create "$key" \
                --data-file=- \
                --project="$PROJECT_ID" \
                --replication-policy="automatic" > /dev/null
            echo "   ✅ Created"
        fi
    fi
done

echo ""
echo "✅ Sync complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Verify sync: ./scripts/verify-secrets-sync.sh"
echo "   2. If new secrets added: ./scripts/grant-secret-access.sh"
echo "   3. Update Cloud Run: ./scripts/deploy-with-secrets.sh"

