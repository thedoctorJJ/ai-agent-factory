#!/bin/bash
# Verify that local encrypted storage and Google Cloud Secrets Manager are in sync

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"

echo "🔍 Verifying secrets sync between local and cloud..."
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

# Load local secrets
echo "📦 Loading local secrets..."

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" && python3 "$SCRIPT_DIR/load-secrets-helper.py" > /tmp/local_secrets.txt

# Compare with cloud
SYNCED=0
MISSING=0
DIFFERENT=0
NOT_IN_CLOUD=0

while IFS='|' read -r key value; do
    if [ -n "$key" ] && [ -n "$value" ]; then
        # Check if secret exists in cloud
        if gcloud secrets describe "$key" --project="$PROJECT_ID" &>/dev/null; then
            # Get cloud value
            CLOUD_VALUE=$(gcloud secrets versions access latest --secret="$key" --project="$PROJECT_ID" 2>/dev/null || echo "")
            
            if [ "$CLOUD_VALUE" = "$value" ]; then
                echo "✅ $key: In sync"
                ((SYNCED++))
            else
                echo "⚠️  $key: Different values"
                echo "   Local:  ${value:0:20}... (length: ${#value})"
                echo "   Cloud:  ${CLOUD_VALUE:0:20}... (length: ${#CLOUD_VALUE})"
                ((DIFFERENT++))
            fi
        else
            echo "❌ $key: Not in cloud"
            ((NOT_IN_CLOUD++))
        fi
    fi
done < /tmp/local_secrets.txt

# Check for secrets in cloud but not in local
echo ""
echo "🔍 Checking for cloud-only secrets..."
for SECRET in "${REQUIRED_SECRETS[@]}"; do
    if gcloud secrets describe "$SECRET" --project="$PROJECT_ID" &>/dev/null; then
        if ! grep -q "^${SECRET}|" /tmp/local_secrets.txt; then
            echo "⚠️  $SECRET: In cloud but not in local"
            ((MISSING++))
        fi
    fi
done

# Summary
echo ""
echo "📊 Sync Status Summary:"
echo "   ✅ In sync: $SYNCED"
if [ $DIFFERENT -gt 0 ]; then
    echo "   ⚠️  Different: $DIFFERENT"
fi
if [ $NOT_IN_CLOUD -gt 0 ]; then
    echo "   ❌ Not in cloud: $NOT_IN_CLOUD"
fi
if [ $MISSING -gt 0 ]; then
    echo "   ⚠️  In cloud but not local: $MISSING"
fi

# Cleanup
rm -f /tmp/local_secrets.txt

# Exit code
if [ $DIFFERENT -eq 0 ] && [ $NOT_IN_CLOUD -eq 0 ] && [ $MISSING -eq 0 ]; then
    echo ""
    echo "✅ All secrets are in sync!"
    exit 0
else
    echo ""
    echo "⚠️  Secrets are out of sync. Run ./scripts/sync-secrets-to-cloud.sh to fix."
    exit 1
fi

