@echo off
echo 🚀 Setting up Incident Response Platform...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available. Please install Docker Desktop with Compose.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist data mkdir data

REM Copy environment file if it doesn't exist
if not exist backend\.env (
    echo 📋 Setting up environment configuration...
    copy backend\.env.example backend\.env >nul 2>&1 || echo Please configure backend\.env file with your settings
)

REM Build and start services
echo 🏗️  Building and starting services...
docker-compose up --build -d

REM Wait for services to start
echo ⏳ Waiting for services to initialize...
timeout /t 30 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service health...
docker-compose ps | find "Up" >nul
if %errorlevel% equ 0 (
    echo ✅ Services are running successfully!
    echo.
    echo 🌐 Access the application:
    echo    Frontend: http://localhost:3000
    echo    Backend API: http://localhost:8000
    echo    API Documentation: http://localhost:8000/docs
    echo.
    echo 📊 Database Information:
    echo    PostgreSQL: localhost:5432
    echo    Database: incident_response_db
    echo    Username: incident_user
    echo.
    echo 🔧 To stop services: docker-compose down
    echo 📝 To view logs: docker-compose logs -f
) else (
    echo ❌ Some services failed to start. Check logs with: docker-compose logs
)

pause
