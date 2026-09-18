#!/usr/bin/env python3
"""
Simple run script for Railway Operations System (No Docker required)
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
    """Main run function"""
    print("🚂 Railway Operations System - Simple Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Step 1: Install dependencies
    print("\n📦 Step 1: Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Some dependencies failed to install, but continuing...")
    
    # Step 2: Create directories
    print("\n📁 Step 2: Creating directories...")
    directories = ["data/uploads", "data/sops", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Step 3: Setup database
    print("\n🗄️  Step 3: Setting up SQLite database...")
    
    # Clear any problematic environment variables
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    if run_command("python -m src.cli setup-db", "Initializing database"):
        print("✅ Database initialized")
    else:
        print("❌ Database initialization failed")
        return
    
    # Step 4: Load sample data
    print("\n📊 Step 4: Loading sample data...")
    if run_command("python -m src.cli ingest-sample", "Loading sample data"):
        print("✅ Sample data loaded")
    else:
        print("❌ Sample data loading failed")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the API server: python -m src.cli start-api")
    print("2. Start the UI: python -m src.cli start-ui")
    print("3. Or start both with: python run_simple.py --start-all")
    print("\nAccess the application:")
    print("- API: http://localhost:8000")
    print("- UI: http://localhost:8501")
    print("- API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--start-all":
        print("🚀 Starting all services...")
        print("Starting API server in background...")
        subprocess.Popen(["python", "-m", "src.cli", "start-api"])
        print("Starting UI...")
        subprocess.run(["python", "-m", "src.cli", "start-ui"])
    else:
        main()
