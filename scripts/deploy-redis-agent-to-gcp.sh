#!/bin/bash

# Deploy Redis Caching Agent to Google Cloud Run
# This script migrates the Redis agent from Fly.io to Google Cloud Run

set -e

# Configuration
PROJECT_ID="agent-factory-474201"
REGION="us-central1"
SERVICE_NAME="redis-caching-agent"
IMAGE_NAME="gcr.io/${PROJECT_ID}/redis-caching-agent"
AGENT_DIR="/Users/jason/Repositories/ai-agent-factory/agents/redis-caching-agent"

echo "🚀 Deploying Redis Caching Agent to Google Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo "Image: ${IMAGE_NAME}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if we're authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Set the project
echo "🔧 Setting project to ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}

# Navigate to agent directory
cd ${AGENT_DIR}

# Build and push the Docker image
echo "🔨 Building and pushing Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 1 \
    --set-env-vars REDIS_HOST=10.1.93.195,REDIS_PORT=6379,REDIS_URL=redis://10.1.93.195:6379,ENVIRONMENT=production

# Get the service URL
echo "🔍 Getting service URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo "✅ Redis Caching Agent deployed successfully!"
echo "🌐 Service URL: ${SERVICE_URL}"
echo "📊 Health Check: ${SERVICE_URL}/health"
echo "📚 API Docs: ${SERVICE_URL}/docs"
echo "📈 Metrics: ${SERVICE_URL}/metrics"

# Test the deployment
echo ""
echo "🧪 Testing the deployment..."

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s "${SERVICE_URL}/health" || echo "Failed")
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed: ${HEALTH_RESPONSE}"
fi

# Test cache operations
echo "Testing cache operations..."

# Test set
echo "Testing cache set..."
SET_RESPONSE=$(curl -s -X POST "${SERVICE_URL}/cache" \
    -H "Content-Type: application/json" \
    -d '{"key": "test-key", "value": "test-value", "ttl": 60}' || echo "Failed")

if [[ $SET_RESPONSE == *"success"* ]]; then
    echo "✅ Cache set operation passed"
else
    echo "❌ Cache set operation failed: ${SET_RESPONSE}"
fi

# Test get
echo "Testing cache get..."
GET_RESPONSE=$(curl -s "${SERVICE_URL}/cache/test-key" || echo "Failed")

if [[ $GET_RESPONSE == *"test-value"* ]]; then
    echo "✅ Cache get operation passed"
else
    echo "❌ Cache get operation failed: ${GET_RESPONSE}"
fi

# Test stats
echo "Testing cache stats..."
STATS_RESPONSE=$(curl -s "${SERVICE_URL}/cache/stats" || echo "Failed")

if [[ $STATS_RESPONSE == *"total_keys"* ]]; then
    echo "✅ Cache stats operation passed"
else
    echo "❌ Cache stats operation failed: ${STATS_RESPONSE}"
fi

echo ""
echo "🎉 Redis Caching Agent migration to Google Cloud Run completed!"
echo ""
echo "Next steps:"
echo "1. Update the agent registration in the AI Agent Factory platform"
echo "2. Test all endpoints thoroughly"
echo "3. Monitor performance and adjust scaling as needed"
echo "4. Consider decommissioning the Fly.io deployment once confirmed working"
