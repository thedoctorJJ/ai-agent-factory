#!/bin/bash

# Setup Google Cloud Run for AI Agent Factory
# This script helps configure Google Cloud Run for agent deployment

echo "🚀 Setting up Google Cloud Run for AI Agent Factory..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI (gcloud) is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if we're authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "⚠️  Not authenticated with Google Cloud."
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
PROJECT_ID="agent-factory-474201"
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Check if service account key exists
SERVICE_ACCOUNT_KEY="config/google-cloud-service-account.json"
if [ ! -f "$SERVICE_ACCOUNT_KEY" ]; then
    echo "❌ Service account key not found at: $SERVICE_ACCOUNT_KEY"
    echo "Please ensure the Google Cloud service account JSON file is in the config directory."
    exit 1
fi

# Authenticate with service account
echo "🔐 Authenticating with service account..."
gcloud auth activate-service-account --key-file="$SERVICE_ACCOUNT_KEY"

# Test the deployment script
echo "🧪 Testing Google Cloud Run deployment script..."
cd scripts/mcp
python3 google-cloud-run-deploy.py

if [ $? -eq 0 ]; then
    echo "✅ Google Cloud Run setup completed successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Share the Google Cloud credentials with Devin AI"
    echo "2. Devin can now use the 'deploy_to_google_cloud_run' MCP tool"
    echo "3. No credit card required for basic Google Cloud Run usage"
    echo ""
    echo "📋 Credentials to share with Devin:"
    echo "   - Project ID: $PROJECT_ID"
    echo "   - Service Account Key: $SERVICE_ACCOUNT_KEY"
    echo "   - Region: us-central1"
else
    echo "❌ Google Cloud Run setup failed. Please check the errors above."
    exit 1
fi
