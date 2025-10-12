#!/bin/bash

echo "🗄️  AI Agent Factory Database Setup"
echo "=================================="

# Get the current directory
CURRENT_DIR=$(pwd)
SCHEMA_FILE="$CURRENT_DIR/infra/database/schema.sql"

echo "📁 Current directory: $CURRENT_DIR"
echo "📄 Schema file: $SCHEMA_FILE"

# Check if schema file exists
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "❌ Error: Schema file not found at $SCHEMA_FILE"
    exit 1
fi

echo "✅ Schema file found"

# Check if .env.local exists
ENV_FILE="$CURRENT_DIR/config/env/.env.local"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: Environment file not found at $ENV_FILE"
    echo "Please create the environment file with your Supabase credentials"
    exit 1
fi

echo "✅ Environment file found"

# Load environment variables
source "$ENV_FILE"

# Check if required environment variables are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo "❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in $ENV_FILE"
    echo "Please add the following to your .env.local file:"
    echo "SUPABASE_URL=your-supabase-url"
    echo "SUPABASE_KEY=your-supabase-key"
    exit 1
fi

echo "✅ Supabase credentials found"

# Test database connection
echo "🔌 Testing database connection..."
python3 -c "
import os
import sys
sys.path.append('$CURRENT_DIR/backend')
from fastapi_app.utils.database import db_manager
import asyncio

async def test_connection():
    try:
        if db_manager.is_connected():
            print('✅ Database connection successful')
            return True
        else:
            print('❌ Database connection failed')
            return False
    except Exception as e:
        print(f'❌ Database connection error: {e}')
        return False

result = asyncio.run(test_connection())
sys.exit(0 if result else 1)
"

if [ $? -ne 0 ]; then
    echo "❌ Database connection test failed"
    echo ""
    echo "📋 Manual Setup Instructions:"
    echo "1. Go to your Supabase dashboard: https://supabase.com/dashboard"
    echo "2. Select your project"
    echo "3. Go to the SQL Editor"
    echo "4. Copy and paste the contents of $SCHEMA_FILE"
    echo "5. Run the SQL script"
    echo ""
    echo "📄 Schema file location: $SCHEMA_FILE"
    exit 1
fi

echo "✅ Database connection test passed"

# Test if tables exist
echo "🔍 Checking if tables exist..."
python3 -c "
import os
import sys
sys.path.append('$CURRENT_DIR/backend')
from fastapi_app.utils.database import db_manager
import asyncio

async def check_tables():
    try:
        # Try to query each table
        tables = ['prds', 'agents', 'devin_tasks']
        for table in tables:
            try:
                result = db_manager.client.table(table).select('id').limit(1).execute()
                print(f'✅ Table {table} exists')
            except Exception as e:
                print(f'❌ Table {table} does not exist or is not accessible: {e}')
                return False
        return True
    except Exception as e:
        print(f'❌ Error checking tables: {e}')
        return False

result = asyncio.run(check_tables())
sys.exit(0 if result else 1)
"

if [ $? -ne 0 ]; then
    echo "❌ Some tables are missing"
    echo ""
    echo "📋 Manual Setup Instructions:"
    echo "1. Go to your Supabase dashboard: https://supabase.com/dashboard"
    echo "2. Select your project"
    echo "3. Go to the SQL Editor"
    echo "4. Copy and paste the contents of $SCHEMA_FILE"
    echo "5. Run the SQL script"
    echo ""
    echo "📄 Schema file location: $SCHEMA_FILE"
    exit 1
fi

echo "✅ All tables exist"

# Test CRUD operations
echo "🧪 Testing CRUD operations..."
python3 -c "
import os
import sys
sys.path.append('$CURRENT_DIR/backend')
from fastapi_app.utils.database import db_manager
from fastapi_app.services.prd_service import PRDService
from fastapi_app.models.prd import PRDCreate, PRDType
import asyncio

async def test_crud():
    try:
        # Test PRD creation
        prd_service = PRDService()
        prd_data = PRDCreate(
            title='Test PRD for Database Integration',
            description='This is a test PRD to verify database integration',
            requirements=['Test requirement 1', 'Test requirement 2'],
            prd_type=PRDType.AGENT
        )
        
        prd = await prd_service.create_prd(prd_data)
        print(f'✅ PRD created successfully: {prd.id}')
        
        # Test PRD retrieval
        retrieved_prd = await prd_service.get_prd(prd.id)
        print(f'✅ PRD retrieved successfully: {retrieved_prd.title}')
        
        # Test PRD listing
        prds = await prd_service.get_prds()
        print(f'✅ PRDs listed successfully: {len(prds.prds)} PRDs found')
        
        # Clean up test PRD
        await prd_service.delete_prd(prd.id)
        print(f'✅ Test PRD deleted successfully')
        
        return True
    except Exception as e:
        print(f'❌ CRUD test failed: {e}')
        return False

result = asyncio.run(test_crud())
sys.exit(0 if result else 1)
"

if [ $? -ne 0 ]; then
    echo "❌ CRUD operations test failed"
    exit 1
fi

echo "✅ CRUD operations test passed"

echo ""
echo "🎉 Database setup completed successfully!"
echo ""
echo "📊 Database Status:"
echo "  - Connection: ✅ Connected"
echo "  - Tables: ✅ All tables exist"
echo "  - CRUD Operations: ✅ Working"
echo ""
echo "🚀 Your AI Agent Factory is now ready with persistent database storage!"
echo ""
echo "📋 Next Steps:"
echo "1. Start your backend server: cd backend && python -m uvicorn fastapi_app.main:app --reload"
echo "2. Start your frontend: cd frontend/next-app && npm run dev"
echo "3. Test the application at http://localhost:3000"
echo ""
echo "💡 The system will now persist all data across restarts!"
