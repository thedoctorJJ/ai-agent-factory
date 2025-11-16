#!/bin/bash
# Grant Cloud Run service account access to secrets in Secrets Manager

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"
SERVICE_NAME="ai-agent-factory-backend"

echo "🔐 Granting secret access to Cloud Run service account..."
echo ""

# Get Cloud Run service account
echo "📋 Getting service account..."
SERVICE_ACCOUNT=$(gcloud run services describe "$SERVICE_NAME" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --format="value(spec.template.spec.serviceAccountName)" 2>/dev/null || echo "")

# If no service account, use default compute service account
if [ -z "$SERVICE_ACCOUNT" ]; then
    SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
    echo "⚠️  No service account found, using default: $SERVICE_ACCOUNT"
else
    echo "✅ Found service account: $SERVICE_ACCOUNT"
fi

# Required secrets
REQUIRED_SECRETS=(
    "SUPABASE_URL"
    "SUPABASE_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
    "OPENAI_API_KEY"
    "GITHUB_TOKEN"
    "GOOGLE_CLOUD_PROJECT_ID"
)

echo ""
echo "🔑 Granting access to secrets..."

for SECRET in "${REQUIRED_SECRETS[@]}"; do
    # Check if secret exists
    if ! gcloud secrets describe "$SECRET" --project="$PROJECT_ID" &>/dev/null; then
        echo "⚠️  Secret $SECRET does not exist. Skipping..."
        continue
    fi
    
    echo "   Granting access to $SECRET..."
    gcloud secrets add-iam-policy-binding "$SECRET" \
        --member="serviceAccount:${SERVICE_ACCOUNT}" \
        --role="roles/secretmanager.secretAccessor" \
        --project="$PROJECT_ID" \
        --quiet || echo "   ⚠️  Failed to grant access (may already have access)"
done

echo ""
echo "✅ Secret access granted!"
echo ""
echo "📋 Next step:"
echo "   Run: ./scripts/deploy-with-secrets.sh"

