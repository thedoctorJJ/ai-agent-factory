#!/bin/bash

# Deploy Backend Update to Google Cloud Run
# This script builds locally with Docker and deploys to Google Cloud Run

echo "🚀 Deploying backend update to Google Cloud Run..."
echo ""

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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    exit 1
fi

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo "❌ Docker daemon is not running."
    echo "   Please start Docker Desktop or the Docker daemon."
    exit 1
fi

# Set the project
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Authenticate Docker with GCR
echo "🔐 Configuring Docker authentication for Google Container Registry..."
gcloud auth configure-docker gcr.io --quiet

# Navigate to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo "   Script dir: $SCRIPT_DIR"
echo "   Project root: $PROJECT_ROOT"
echo "   Backend dir: $BACKEND_DIR"

if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found at: $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"

echo ""
echo "🔨 Building Docker image locally for AMD64 (Cloud Run requirement)..."
echo "   Image: $IMAGE_NAME"
echo "   Platform: linux/amd64"
if ! docker build --platform linux/amd64 -t $IMAGE_NAME .; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo ""
echo "📤 Pushing image to Google Container Registry..."
if ! docker push $IMAGE_NAME; then
    echo "❌ Docker push failed!"
    exit 1
fi

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
    echo ""
    echo "✅ Backend deployment completed successfully!"
    echo ""
    
    # Get the actual service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)' 2>/dev/null)
    
    if [ -z "$SERVICE_URL" ]; then
        # Fallback to standard URL format
        SERVICE_URL="https://$SERVICE_NAME-952475323593.$REGION.run.app"
    fi
    
    echo "🔗 Service URL: $SERVICE_URL"
    echo "📊 API Docs: $SERVICE_URL/docs"
    echo ""
    echo "🧪 Testing the deployment..."
    echo ""
    
    # Wait for deployment to be ready
    echo "⏳ Waiting 15 seconds for deployment to stabilize..."
    sleep 15
    
    # Test the health endpoint
    echo "1️⃣ Testing health endpoint..."
    if curl -sf "$SERVICE_URL/api/v1/health" > /dev/null; then
        echo "   ✅ Health check passed"
    else
        echo "   ❌ Health check failed"
    fi
    
    # Test the agents endpoint
    echo "2️⃣ Testing agents endpoint..."
    if curl -sf "$SERVICE_URL/api/v1/agents" > /dev/null; then
        echo "   ✅ Agents endpoint working"
        echo ""
        echo "   📊 Testing with detailed output..."
        curl -s "$SERVICE_URL/api/v1/agents" | python3 -m json.tool | head -10
    else
        echo "   ❌ Agents endpoint failed"
    fi
    
    echo ""
    echo "🎉 Deployment complete!"
    
else
    echo "❌ Backend deployment failed!"
    exit 1
fi
