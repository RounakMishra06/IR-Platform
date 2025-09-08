#!/bin/bash

# Incident Response Platform Setup Script

echo "🚀 Setting up Incident Response Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Copy environment file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📋 Setting up environment configuration..."
    cp backend/.env.example backend/.env 2>/dev/null || echo "Please configure backend/.env file with your settings"
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running successfully!"
    echo ""
    echo "🌐 Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📊 Database Information:"
    echo "   PostgreSQL: localhost:5432"
    echo "   Database: incident_response_db"
    echo "   Username: incident_user"
    echo ""
    echo "🔧 To stop services: docker-compose down"
    echo "📝 To view logs: docker-compose logs -f"
else
    echo "❌ Some services failed to start. Check logs with: docker-compose logs"
fi
