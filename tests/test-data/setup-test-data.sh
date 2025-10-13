#!/bin/bash

# Test Data Setup Script for AI Agent Factory
# Creates sample agents to demonstrate one-to-many PRD-to-Agent relationships

set -e

echo "🚀 Setting up test data for AI Agent Factory..."
echo "📋 This will create sample agents to demonstrate PRD-to-Agent relationships"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/fastapi_app/main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    echo "   Expected: /path/to/end-cap-agent-factory/"
    exit 1
fi

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found"
    echo "   Please run: ./scripts/setup/dev-setup.sh"
    exit 1
fi

# Check if sample PRDs exist
echo "🔍 Checking for sample PRDs..."
cd backend
source venv/bin/activate

# Check if PRDs exist by making a simple API call
python -c "
import asyncio
import sys
sys.path.append('.')
from fastapi_app.services.prd_service import prd_service

async def check_prds():
    try:
        prds = await prd_service.get_prds(limit=1)
        if prds.total > 0:
            print(f'✅ Found {prds.total} PRDs in the system')
            return True
        else:
            print('❌ No PRDs found. Please create sample PRDs first:')
            print('   python ../scripts/create-sample-prds.py')
            return False
    except Exception as e:
        print(f'❌ Error checking PRDs: {e}')
        return False

if not asyncio.run(check_prds()):
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "💡 To create sample PRDs first, run:"
    echo "   python ../scripts/create-sample-prds.py"
    exit 1
fi

echo ""
echo "🤖 Creating sample agents..."

# Create test agents
python ../tests/test-data/create-sample-agents.py

echo ""
echo "🎉 Test data setup completed!"
echo ""
echo "📱 You can now view the results at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/docs"
echo ""
echo "🧹 To clean up test data later, run:"
echo "   python ../tests/test-data/cleanup-test-data.py"
echo ""
echo "✨ The UI will now show:"
echo "   - Agent count badges on PRD cards"
echo "   - Agents grouped by PRD in the Agents tab"
echo "   - One-to-many relationship demonstration"
