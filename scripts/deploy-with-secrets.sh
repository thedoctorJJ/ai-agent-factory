#!/bin/bash
# Deploy Cloud Run service with secrets from Secrets Manager

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"
SERVICE_NAME="ai-agent-factory-backend"
BACKEND_URL="https://ai-agent-factory-backend-952475323593.us-central1.run.app"

echo "🚀 Deploying Cloud Run service with Secrets Manager..."
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

# Build --update-secrets flag
SECRETS_FLAG=""
for SECRET in "${REQUIRED_SECRETS[@]}"; do
    # Check if secret exists
    if ! gcloud secrets describe "$SECRET" --project="$PROJECT_ID" &>/dev/null; then
        echo "⚠️  Secret $SECRET does not exist. Skipping..."
        continue
    fi
    
    if [ -z "$SECRETS_FLAG" ]; then
        SECRETS_FLAG="--update-secrets=${SECRET}=${SECRET}:latest"
    else
        SECRETS_FLAG="${SECRETS_FLAG},${SECRET}=${SECRET}:latest"
    fi
done

if [ -z "$SECRETS_FLAG" ]; then
    echo "❌ No secrets found! Run ./scripts/setup-cloud-secrets.sh first"
    exit 1
fi

echo "📋 Updating Cloud Run service..."
echo "   Secrets: ${REQUIRED_SECRETS[*]}"
echo ""

gcloud run services update "$SERVICE_NAME" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  $SECRETS_FLAG \
  --set-env-vars="ENVIRONMENT=production"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Service updated successfully!"
    echo ""
    echo "🧪 Testing the updated service..."
    sleep 10  # Wait for deployment to be ready
    
    # Test the health endpoint
    echo "   Testing health endpoint..."
    if curl -sf "${BACKEND_URL}/api/v1/health" > /dev/null; then
        echo "   ✅ Health check passed!"
        
        # Get detailed health status
        echo ""
        echo "📊 Health status:"
        curl -s "${BACKEND_URL}/api/v1/health" | python3 -m json.tool || echo "   (Response not JSON)"
    else
        echo "   ⚠️  Health check failed (service may still be starting)"
    fi
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "📋 Verify secrets are loaded:"
    echo "   curl ${BACKEND_URL}/api/v1/config"
else
    echo "❌ Failed to update service!"
    exit 1
fi

