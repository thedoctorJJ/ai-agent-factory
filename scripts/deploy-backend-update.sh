#!/bin/bash

# Deploy Backend Update to Google Cloud Run
# This script updates the backend with the latest schema fixes

echo "🚀 Deploying backend update to Google Cloud Run..."

# Set variables
PROJECT_ID="agent-factory-474201"
SERVICE_NAME="ai-agent-factory-backend"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI (gcloud) is not installed."
    exit 1
fi

# Set the project
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Navigate to backend directory
cd backend

echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

echo "📤 Pushing image to Google Container Registry..."
docker push $IMAGE_NAME

echo "🚀 Deploying to Google Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars ENVIRONMENT=production \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 1

if [ $? -eq 0 ]; then
    echo "✅ Backend deployment completed successfully!"
    echo ""
    echo "🔗 Service URL: https://$SERVICE_NAME-$REGION.a.run.app"
    echo "📊 API Docs: https://$SERVICE_NAME-$REGION.a.run.app/docs"
    echo ""
    echo "🧪 Testing the deployment..."
    
    # Test the health endpoint
    sleep 10  # Wait for deployment to be ready
    curl -f "https://$SERVICE_NAME-$REGION.a.run.app/api/v1/health" && echo "✅ Health check passed" || echo "❌ Health check failed"
    
    # Test the agents endpoint
    curl -f "https://$SERVICE_NAME-$REGION.a.run.app/api/v1/agents" && echo "✅ Agents endpoint working" || echo "❌ Agents endpoint failed"
    
else
    echo "❌ Backend deployment failed!"
    exit 1
fi
