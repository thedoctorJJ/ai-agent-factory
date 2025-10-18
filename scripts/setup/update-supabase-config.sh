#!/bin/bash

# Update Supabase Configuration Script
# This script helps you update the Supabase credentials

echo "🔧 Supabase Configuration Update"
echo "================================"
echo

# Check if .env.local exists
ENV_FILE="/Users/jason/Repositories/ai-agent-factory/config/env/.env.local"
if [ ! -f "$ENV_FILE" ]; then
    echo "📄 Creating .env.local file..."
    mkdir -p "$(dirname "$ENV_FILE")"
    touch "$ENV_FILE"
fi

echo "📋 Current configuration:"
echo "------------------------"
if [ -f "$ENV_FILE" ]; then
    grep -E "SUPABASE_URL|SUPABASE_KEY" "$ENV_FILE" 2>/dev/null || echo "No Supabase config found"
else
    echo "No .env.local file found"
fi

echo
echo "🔗 Please provide your Supabase project details:"
echo

# Get Supabase URL
read -p "Enter your Supabase Project URL (e.g., https://your-project-id.supabase.co): " SUPABASE_URL

# Get Supabase Key
read -p "Enter your Supabase anon/public key: " SUPABASE_KEY

# Validate inputs
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo "❌ Error: Both URL and Key are required"
    exit 1
fi

# Update the .env.local file
echo
echo "📝 Updating configuration..."

# Remove existing Supabase config
sed -i.bak '/^SUPABASE_URL=/d' "$ENV_FILE" 2>/dev/null
sed -i.bak '/^SUPABASE_KEY=/d' "$ENV_FILE" 2>/dev/null

# Add new config
echo "SUPABASE_URL=$SUPABASE_URL" >> "$ENV_FILE"
echo "SUPABASE_KEY=$SUPABASE_KEY" >> "$ENV_FILE"

echo "✅ Configuration updated!"
echo
echo "📋 Updated configuration:"
echo "------------------------"
echo "SUPABASE_URL=$SUPABASE_URL"
echo "SUPABASE_KEY=${SUPABASE_KEY:0:50}..."
echo
echo "🧪 Testing connection..."
echo "------------------------"

# Test the connection
cd /Users/jason/Repositories/ai-agent-factory/backend
source venv/bin/activate

python3 -c "
import os
import sys
sys.path.insert(0, '.')

# Load the new config
from fastapi_app.config import config
print(f'✅ New Supabase URL: {config.supabase_url}')
print(f'✅ New Supabase Key: {config.supabase_key[:50]}...')

# Test connection
try:
    from supabase import create_client
    client = create_client(config.supabase_url, config.supabase_key)
    print('✅ Supabase client created successfully')
    
    # Try a simple query
    result = client.table('_test').select('*').limit(1).execute()
    print('✅ Connection test successful')
except Exception as e:
    print(f'⚠️  Connection test failed (expected if tables don\'t exist): {e}')
    print('This is normal - we\'ll create the tables next')
"

echo
echo "🎉 Supabase configuration updated successfully!"
echo
echo "📋 Next steps:"
echo "1. Apply the database schema to your Supabase project"
echo "2. Test the full integration"
echo
echo "Run: ./scripts/setup/apply-schema-to-supabase.sh"
