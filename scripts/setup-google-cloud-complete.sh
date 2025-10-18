#!/bin/bash

# Complete Google Cloud Setup Script for AI Agent Factory
# This script sets up all required Google Cloud services and APIs

set -e

PROJECT_ID="agent-factory-474201"
REGION="us-central1"
SERVICE_ACCOUNT_EMAIL="agent-factory@agent-factory-474201.iam.gserviceaccount.com"

echo "🚀 Setting up Google Cloud for AI Agent Factory"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Account: $SERVICE_ACCOUNT_EMAIL"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
echo "🔐 Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ No active Google Cloud authentication found."
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
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

# Wait for APIs to propagate
echo "⏳ Waiting for APIs to propagate (30 seconds)..."
sleep 30

# Create Redis instance
echo "🗄️  Setting up Redis instance..."
REDIS_INSTANCE="ai-agent-factory-redis"

# Check if Redis instance already exists
if gcloud redis instances describe $REDIS_INSTANCE --region=$REGION --project=$PROJECT_ID &> /dev/null; then
    echo "✅ Redis instance '$REDIS_INSTANCE' already exists"
else
    echo "  Creating Redis instance: $REDIS_INSTANCE"
    gcloud redis instances create $REDIS_INSTANCE \
        --size=1 \
        --region=$REGION \
        --redis-version=redis_6_x \
        --project=$PROJECT_ID
    
    echo "✅ Redis instance created successfully!"
fi

# Get Redis connection info
echo "📊 Getting Redis connection information..."
REDIS_INFO=$(gcloud redis instances describe $REDIS_INSTANCE --region=$REGION --project=$PROJECT_ID --format="json")
REDIS_HOST=$(echo $REDIS_INFO | jq -r '.host')
REDIS_PORT=$(echo $REDIS_INFO | jq -r '.port')

echo "✅ Redis instance details:"
echo "   Host: $REDIS_HOST"
echo "   Port: $REDIS_PORT"
echo "   URL: redis://$REDIS_HOST:$REDIS_PORT"

# Test Cloud Run deployment
echo "🚀 Testing Cloud Run deployment..."
TEST_SERVICE="test-agent-service"

# Check if test service already exists
if gcloud run services describe $TEST_SERVICE --region=$REGION --project=$PROJECT_ID &> /dev/null; then
    echo "✅ Test service '$TEST_SERVICE' already exists"
    SERVICE_URL=$(gcloud run services describe $TEST_SERVICE --region=$REGION --project=$PROJECT_ID --format="value(status.url)")
    echo "   Service URL: $SERVICE_URL"
else
    echo "  Creating test Cloud Run service..."
    
    # Create a simple test service
    cat > /tmp/test-service.py << 'EOF'
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Google Cloud Run!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "test-agent"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

    cat > /tmp/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
EOF

    cat > /tmp/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY test-service.py .

EXPOSE 8080

CMD ["python", "test-service.py"]
EOF

    # Build and deploy
    gcloud builds submit --tag gcr.io/$PROJECT_ID/test-agent /tmp --project=$PROJECT_ID
    
    gcloud run deploy $TEST_SERVICE \
        --image gcr.io/$PROJECT_ID/test-agent \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --project $PROJECT_ID \
        --port 8080 \
        --memory 512Mi \
        --cpu 1 \
        --max-instances 5
    
    SERVICE_URL=$(gcloud run services describe $TEST_SERVICE --region=$REGION --project=$PROJECT_ID --format="value(status.url)")
    echo "✅ Test service deployed successfully!"
    echo "   Service URL: $SERVICE_URL"
    
    # Clean up temp files
    rm -f /tmp/test-service.py /tmp/requirements.txt /tmp/Dockerfile
fi

# Test the service
echo "🧪 Testing the deployed service..."
if curl -s "$SERVICE_URL/health" | grep -q "healthy"; then
    echo "✅ Service is responding correctly!"
else
    echo "⚠️  Service may not be responding yet (this is normal for new deployments)"
fi

# Create environment file template
echo "📝 Creating environment configuration..."
cat > .env.google-cloud << EOF
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID
GOOGLE_CLOUD_REGION=$REGION
GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY=config/google-cloud-service-account.json

# Redis Configuration
REDIS_HOST=$REDIS_HOST
REDIS_PORT=$REDIS_PORT
REDIS_URL=redis://$REDIS_HOST:$REDIS_PORT

# Cloud Run Configuration
CLOUD_RUN_REGION=$REGION
CLOUD_RUN_PROJECT_ID=$PROJECT_ID
EOF

echo "✅ Environment configuration saved to .env.google-cloud"

# Summary
echo ""
echo "🎉 Google Cloud setup completed successfully!"
echo ""
echo "📊 Summary:"
echo "   Project ID: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Redis Host: $REDIS_HOST"
echo "   Redis Port: $REDIS_PORT"
echo "   Test Service URL: $SERVICE_URL"
echo ""
echo "📋 Next steps:"
echo "   1. Copy the Google Cloud configuration from .env.google-cloud to your main .env file"
echo "   2. Run 'python3 scripts/config/validate-config.py' to verify the setup"
echo "   3. Test your application with the new Google Cloud services"
echo ""
echo "🔧 To clean up the test service later, run:"
echo "   gcloud run services delete $TEST_SERVICE --region=$REGION --project=$PROJECT_ID"
