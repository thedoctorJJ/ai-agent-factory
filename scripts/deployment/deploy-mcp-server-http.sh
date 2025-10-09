#!/bin/bash

set -e

echo "🚀 Deploying END_CAP Agent Factory HTTP MCP Server to Google Cloud Run..."

# Configuration
PROJECT_ID="agent-factory-474201"
SERVICE_NAME="end-cap-mcp-server-http"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/mcp-server-http"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set Google Cloud project
echo "📋 Setting Google Cloud project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com

# Build and push Docker image
echo "🏗️  Building Docker image..."
cd scripts
docker build --platform linux/amd64 -f mcp-server-http-dockerfile -t ${IMAGE_NAME}:latest .
cd .. # Go back to the root directory

echo "📤 Pushing image to Google Container Registry..."
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME}:latest \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --port 8001 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars="GITHUB_ORG_NAME=thedoctorJJ,ENDCAP_API_URL=https://end-cap-agent-factory-backend-xxxxx-uc.a.run.app,GITHUB_TOKEN=placeholder,SUPABASE_SERVICE_ROLE_KEY=placeholder,GCP_SERVICE_ACCOUNT_KEY=placeholder,OPENAI_API_KEY=placeholder"

echo "🎉 HTTP MCP Server deployment initiated!"
echo "Monitor deployment status here: https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}/revisions?project=${PROJECT_ID}"

# Get the service URL
echo "🔗 Getting service URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')
echo "Service URL: ${SERVICE_URL}"

echo "✅ HTTP MCP Server deployed successfully!"
echo "📋 Next steps:"
echo "1. Test the service: curl ${SERVICE_URL}/health"
echo "2. Update Devin AI MCP configuration with: ${SERVICE_URL}/mcp"
echo "3. Update ChatGPT MCP configuration with: ${SERVICE_URL}/mcp"
