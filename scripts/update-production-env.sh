#!/bin/bash

# Update Production Environment Variables
# This script updates the production backend with proper environment variables

echo "🔧 Updating production backend environment variables..."

# Set variables
SERVICE_NAME="ai-agent-factory-backend"
REGION="us-central1"

# Get environment variables from secure config
echo "📋 Getting environment variables from secure config..."

# Create a temporary script to get the actual values
cat > /tmp/get_env_vars.py << 'EOF'
import sys
import os
sys.path.append('.')
from config.secure_config import SecureConfig

config = SecureConfig()
env_vars = config.get_all_environment_variables()

# Print the variables we need for production
required_vars = [
    'SUPABASE_URL',
    'SUPABASE_KEY', 
    'SUPABASE_SERVICE_ROLE_KEY',
    'OPENAI_API_KEY',
    'GITHUB_TOKEN',
    'GOOGLE_CLOUD_PROJECT_ID'
]

for var in required_vars:
    if var in env_vars:
        print(f"{var}={env_vars[var]}")
    else:
        print(f"# {var} not found")
EOF

# Run the script to get environment variables
cd /Users/jason/Repositories/ai-agent-factory
python3 /tmp/get_env_vars.py > /tmp/env_vars.txt

# Read the environment variables
ENV_VARS=""
while IFS= read -r line; do
    if [[ ! $line =~ ^# ]]; then
        ENV_VARS="$ENV_VARS,$line"
    fi
done < /tmp/env_vars.txt

# Remove leading comma
ENV_VARS="${ENV_VARS#,}"

echo "🚀 Updating Cloud Run service with environment variables..."
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --set-env-vars="ENVIRONMENT=production,$ENV_VARS"

if [ $? -eq 0 ]; then
    echo "✅ Environment variables updated successfully!"
    echo ""
    echo "🧪 Testing the updated service..."
    sleep 10  # Wait for deployment to be ready
    
    # Test the health endpoint
    curl -f "https://ai-agent-factory-backend-952475323593.us-central1.run.app/api/v1/health" && echo "✅ Health check passed" || echo "❌ Health check failed"
    
else
    echo "❌ Failed to update environment variables!"
    exit 1
fi

# Clean up
rm -f /tmp/get_env_vars.py /tmp/env_vars.txt
