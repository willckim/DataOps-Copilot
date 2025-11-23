#!/bin/bash

# DataOps Copilot - Quick Start Script
# This script helps you get the project running quickly

set -e

echo "🚀 DataOps Copilot - Quick Start"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "📝 Please edit backend/.env and add your API keys:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - GOOGLE_API_KEY (optional but recommended - free tier!)"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start services
echo "🐳 Starting backend services (FastAPI, PostgreSQL, Redis)..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if backend is healthy
echo "🔍 Checking backend health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi
    echo "   Waiting for backend... ($i/30)"
    sleep 2
done

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

echo ""
echo "🎨 Starting frontend development server..."
echo ""
echo "================================"
echo "✅ DataOps Copilot is running!"
echo "================================"
echo ""
echo "🌐 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo "🗄️  pgAdmin:   http://localhost:5050 (optional)"
echo ""
echo "📁 Sample data available at: sample_data/sales_data.csv"
echo ""
echo "Press Ctrl+C to stop the frontend server"
echo "To stop all services: docker-compose down"
echo ""

npm run dev