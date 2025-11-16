#!/bin/bash
# Setup Google Cloud Secrets Manager
# Creates secrets in Secrets Manager from local encrypted storage

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"

echo "🔐 Setting up Google Cloud Secrets Manager..."
echo ""

# Enable Secrets Manager API
echo "📋 Enabling Secrets Manager API..."
gcloud services enable secretmanager.googleapis.com --project="$PROJECT_ID" || true

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

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Run Python helper script
cd "$PROJECT_ROOT" && python3 "$SCRIPT_DIR/load-secrets-helper.py" | while IFS='|' read -r key value; do
    if [ -n "$key" ] && [ -n "$value" ]; then
        # Check if secret already exists
        if gcloud secrets describe "$key" --project="$PROJECT_ID" &>/dev/null; then
            echo "⚠️  Secret $key already exists. Updating..."
            echo -n "$value" | gcloud secrets versions add "$key" \
                --data-file=- \
                --project="$PROJECT_ID"
        else
            echo "✅ Creating secret: $key"
            echo -n "$value" | gcloud secrets create "$key" \
                --data-file=- \
                --project="$PROJECT_ID" \
                --replication-policy="automatic"
        fi
    fi
done

echo ""
echo "✅ Secrets created in Google Cloud Secrets Manager!"
echo ""
echo "📋 Next steps:"
echo "   1. Run: ./scripts/grant-secret-access.sh"
echo "   2. Run: ./scripts/deploy-with-secrets.sh"

