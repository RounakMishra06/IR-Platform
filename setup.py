#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python
    success, output = run_command("python --version")
    if not success:
        print("❌ Python is not installed or not in PATH")
        return False
    print(f"✅ {output.strip()}")
    
    # Check Node.js
    success, output = run_command("node --version")
    if not success:
        print("❌ Node.js is not installed or not in PATH")
        return False
    print(f"✅ Node.js {output.strip()}")
    
    # Check npm
    success, output = run_command("npm --version")
    if not success:
        print("❌ npm is not installed or not in PATH")
        return False
    print(f"✅ npm {output.strip()}")
    
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🐍 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    print("Creating virtual environment...")
    success, _ = run_command("python -m venv venv", cwd=backend_dir)
    if not success:
        print("❌ Failed to create virtual environment")
        return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/MacOS
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print("Installing backend dependencies...")
    success, output = run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir)
    if not success:
        print(f"❌ Failed to install backend dependencies: {output}")
        return False
    
    print("✅ Backend setup complete")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n⚛️  Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    print("Installing frontend dependencies...")
    success, output = run_command("npm install", cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install frontend dependencies: {output}")
        return False
    
    print("✅ Frontend setup complete")
    return True

def create_env_file():
    """Create environment file if it doesn't exist"""
    env_file = Path("backend/.env")
    if env_file.exists():
        print("✅ Environment file already exists")
        return
    
    print("📋 Creating environment file...")
    env_content = """# Database Configuration
DATABASE_URL=sqlite:///./incident_response.db

# Application Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379

# SIEM Integration (Optional)
# SPLUNK_HOST=your-splunk-server.com
# SPLUNK_TOKEN=your-splunk-token

# Threat Intelligence APIs (Optional)  
# VIRUSTOTAL_API_KEY=your-virustotal-api-key
# ALIENVAULT_API_KEY=your-alienvault-api-key

# Firewall API (Optional)
# FIREWALL_API_URL=https://your-firewall-api.com
# FIREWALL_API_KEY=your-api-key
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created")

def main():
    """Main setup function"""
    print("🚀 Incident Response Platform Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing dependencies.")
        return 1
    
    # Create environment file
    create_env_file()
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        return 1
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        return 1
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   Backend:  cd backend && python main.py")
    print("   Frontend: cd frontend && npm start")
    print("\n🌐 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n📝 Configuration:")
    print("   Edit backend/.env to configure integrations")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
