#!/bin/bash

# Apply Database Schema to Supabase
# This script applies the database schema to your Supabase project

echo "🗄️  Applying Database Schema to Supabase"
echo "========================================"
echo

# Check if .env.local exists
ENV_FILE="/Users/jason/Repositories/ai-agent-factory/config/env/.env.local"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: .env.local file not found at $ENV_FILE"
    echo "Please run the environment setup first"
    exit 1
fi

# Load environment variables
source "$ENV_FILE"

# Check if required variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local"
    exit 1
fi

echo "🔧 Supabase Configuration:"
echo "URL: $SUPABASE_URL"
echo "Service Role Key: ${SUPABASE_SERVICE_ROLE_KEY:0:50}..."
echo

# Check if schema file exists
SCHEMA_FILE="/Users/jason/Repositories/ai-agent-factory/infra/database/schema.sql"
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "❌ Error: Schema file not found at $SCHEMA_FILE"
    exit 1
fi

echo "📄 Schema file found: $SCHEMA_FILE"
echo

# Create a Python script to apply the schema
PYTHON_SCRIPT="/tmp/apply_schema.py"
cat > "$PYTHON_SCRIPT" << 'EOF'
import os
import sys
import asyncio
from supabase import create_client

async def apply_schema():
    # Load environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        return False
    
    try:
        # Create Supabase client
        client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # Read schema file
        schema_file = "/Users/jason/Repositories/ai-agent-factory/infra/database/schema.sql"
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        print("📄 Schema file loaded")
        
        # Note: Supabase client doesn't support raw SQL execution
        # We need to use the Supabase REST API or CLI
        print("⚠️  Note: Supabase client doesn't support raw SQL execution")
        print("📋 Please apply the schema manually through the Supabase dashboard:")
        print("   1. Go to your Supabase project dashboard")
        print("   2. Navigate to SQL Editor")
        print("   3. Copy and paste the contents of schema.sql")
        print("   4. Execute the SQL")
        print()
        print("🔗 Supabase Dashboard: https://supabase.com/dashboard/project")
        print()
        print("📄 Schema file location: $SCHEMA_FILE")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(apply_schema())
    sys.exit(0 if success else 1)
EOF

echo "🐍 Running schema application script..."
cd /Users/jason/Repositories/ai-agent-factory/backend
source venv/bin/activate

python3 "$PYTHON_SCRIPT"

# Clean up
rm -f "$PYTHON_SCRIPT"

echo
echo "🎉 Schema application process completed!"
echo
echo "📋 Next steps:"
echo "1. Apply the schema manually through Supabase dashboard"
echo "2. Test the connection with: python3 -c \"from fastapi_app.utils.database import db_manager; print('Testing...'); import asyncio; asyncio.run(db_manager.test_connection())\""
echo "3. Restart your application to use Supabase"