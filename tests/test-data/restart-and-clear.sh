#!/bin/bash
#
# Restart backend and clear all data
# This will clear in-memory storage and any database data
#

echo "🔄 Restarting backend to clear all data..."

# Find and kill the backend process
BACKEND_PID=$(lsof -ti:8000)
if [ ! -z "$BACKEND_PID" ]; then
    echo "🛑 Stopping backend (PID: $BACKEND_PID)..."
    kill -9 $BACKEND_PID
    sleep 2
    echo "✅ Backend stopped"
else
    echo "ℹ️  No backend process found on port 8000"
fi

# Start the backend
echo "🚀 Starting backend..."
cd "$(dirname "$0")/../../backend"
source venv/bin/activate
nohup uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &

echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
    
    # Check data status
    AGENT_COUNT=$(curl -s http://localhost:8000/api/v1/agents | jq '.agents | length')
    PRD_COUNT=$(curl -s http://localhost:8000/api/v1/prds | jq '.prds | length')
    
    echo ""
    echo "📊 Current data status:"
    echo "  - Agents: $AGENT_COUNT"
    echo "  - PRDs: $PRD_COUNT"
    
    if [ "$AGENT_COUNT" -eq 0 ] && [ "$PRD_COUNT" -eq 0 ]; then
        echo ""
        echo "✅ All data cleared successfully!"
        echo "🎉 You now have a clean slate!"
    else
        echo ""
        echo "⚠️  Some data still exists"
    fi
else
    echo "❌ Backend failed to start"
    exit 1
fi

