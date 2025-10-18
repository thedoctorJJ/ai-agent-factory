#!/bin/bash

# Simple script to enable required Google Cloud APIs
# Run this with your personal Google account that has project owner permissions

PROJECT_ID="agent-factory-474201"

echo "🔧 Enabling required Google Cloud APIs for project: $PROJECT_ID"

# Required APIs for AI Agent Factory
APIS=(
    "cloudresourcemanager.googleapis.com"
    "serviceusage.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "redis.googleapis.com"
    "iam.googleapis.com"
    "compute.googleapis.com"
    "container.googleapis.com"
    "secretmanager.googleapis.com"
    "logging.googleapis.com"
    "monitoring.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "  Enabling $api..."
    gcloud services enable $api --project=$PROJECT_ID
done

echo "✅ All APIs enabled successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Wait 2-3 minutes for APIs to propagate"
echo "   2. Run: ./scripts/setup-google-cloud-complete.sh"
echo "   3. Or test individual services with the existing scripts"
