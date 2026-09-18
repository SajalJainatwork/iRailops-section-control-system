#!/usr/bin/env python3
"""
Setup script for Railway Operations System
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚂 Railway Operations System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create necessary directories
    directories = [
        "data/uploads",
        "data/sops", 
        "data/raw/external",
        "models",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Copy environment file
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            run_command("cp .env.example .env", "Creating environment file")
            print("📝 Please edit .env file with your configuration")
        else:
            print("⚠️  No .env.example found, please create .env manually")
    
    # Initialize database
    print("\n🗄️  Database Setup")
    print("Please ensure PostgreSQL is running and create the 'irailops' database")
    print("You can use Docker Compose: docker-compose up -d postgres")
    
    # Setup database
    if run_command("python -m src.cli setup-db", "Initializing database"):
        print("✅ Database initialized")
    else:
        print("⚠️  Database initialization failed - please check your database connection")
    
    # Ingest sample data
    if run_command("python -m src.cli ingest-sample", "Ingesting sample data"):
        print("✅ Sample data ingested")
    else:
        print("⚠️  Sample data ingestion failed")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Start the API server: python -m src.cli start-api")
    print("2. Start the UI: python -m src.cli start-ui")
    print("3. Or use Docker Compose: docker-compose up")
    print("\nAccess the application:")
    print("- API: http://localhost:8000")
    print("- UI: http://localhost:8501")
    print("- API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
