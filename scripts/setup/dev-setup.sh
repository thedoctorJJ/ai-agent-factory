#!/bin/bash

# END_CAP Agent Factory - Development Setup Script

set -e

echo "🚀 Setting up END_CAP Agent Factory for development..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ is required but not installed."
    exit 1
fi

# Check if Node.js 18+ is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ is required but not installed."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend/next-app
npm install
cd ../..

# Copy environment file
echo "⚙️ Setting up environment configuration..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Created .env file from template. Please update with your actual values."
fi

# Start infrastructure services
echo "🐳 Starting infrastructure services..."
cd infra
docker-compose up -d postgres redis
cd ..

echo "✅ Development setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your actual configuration values"
echo "2. Start the backend: cd backend && source venv/bin/activate && uvicorn fastapi_app.main:app --reload"
echo "3. Start the frontend: cd frontend/next-app && npm run dev"
echo "4. Visit http://localhost:3000 to see the dashboard"
echo ""
echo "📚 Documentation: ./docs/"
echo "🏗️ Infrastructure: ./infra/"
