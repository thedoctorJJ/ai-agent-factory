#!/bin/bash

echo "🚀 Starting AI Agent Factory with MCP Integration"
echo "=================================================="

# Get the current directory
CURRENT_DIR=$(pwd)
MCP_SERVER_PATH="$CURRENT_DIR/scripts/mcp/mcp-http-server.py"

echo "📁 Current directory: $CURRENT_DIR"
echo "📁 MCP Server path: $MCP_SERVER_PATH"

# Check if MCP server exists
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at: $MCP_SERVER_PATH"
    exit 1
fi

echo "✅ MCP server found"

# Start the MCP HTTP server in the background
echo "🔧 Starting MCP HTTP server on port 8001..."
cd "$CURRENT_DIR/scripts/mcp"
python3 mcp-http-server.py &
MCP_PID=$!
echo "✅ MCP HTTP server started with PID: $MCP_PID"

# Wait a moment for the MCP server to start
sleep 3

# Start the main backend application
echo "🔧 Starting main backend application on port 8000..."
cd "$CURRENT_DIR/backend"
source venv/bin/activate
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "✅ Backend application started with PID: $BACKEND_PID"

# Wait a moment for the backend to start
sleep 3

# Start the frontend application
echo "🔧 Starting frontend application on port 3000..."
cd "$CURRENT_DIR/frontend/next-app"
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend application started with PID: $FRONTEND_PID"

echo ""
echo "🎉 All services started successfully!"
echo "=================================="
echo "📊 Service Status:"
echo "  - MCP HTTP Server: http://localhost:8001 (PID: $MCP_PID)"
echo "  - Backend API: http://localhost:8000 (PID: $BACKEND_PID)"
echo "  - Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "🔗 Quick Links:"
echo "  - Main Application: http://localhost:3000"
echo "  - API Documentation: http://localhost:8000/docs"
echo "  - MCP Server Health: http://localhost:8001/health"
echo "  - MCP Tools: http://localhost:8001/mcp/tools"
echo ""
echo "🛑 To stop all services, press Ctrl+C or run:"
echo "   kill $MCP_PID $BACKEND_PID $FRONTEND_PID"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $MCP_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for any process to exit
wait
