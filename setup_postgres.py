#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Railway Operations System
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"INFO: {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed: {e.stderr}")
        return False

def check_postgres():
    """Check if PostgreSQL is running"""
    try:
        result = subprocess.run("pg_isready", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS: PostgreSQL is running")
            return True
        else:
            print("ERROR: PostgreSQL is not running")
            return False
    except:
        print("ERROR: PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    """Create the irailops database"""
    try:
        # Check if database exists
        result = subprocess.run(
            'psql -lqt | cut -d \\| -f 1 | grep -qw irailops',
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("SUCCESS: Database 'irailops' already exists")
            return True
        
        # Create database
        result = subprocess.run(
            'createdb irailops',
            shell=True, check=True, capture_output=True, text=True
        )
        print("SUCCESS: Database 'irailops' created")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create database: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("PostgreSQL Setup for Railway Operations System")
    print("=" * 50)
    
    # Check if PostgreSQL is running
    if not check_postgres():
        print("\nPlease install and start PostgreSQL:")
        print("1. Install PostgreSQL from: https://www.postgresql.org/download/")
        print("2. Start PostgreSQL service")
        print("3. Run this script again")
        return
    
    # Create database
    if not create_database():
        print("\nFailed to create database. Please check PostgreSQL permissions.")
        return
    
    # Install Python dependencies
    print("\nInstalling Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("WARNING: Some dependencies failed to install")
    
    # Create directories
    directories = ["data/uploads", "data/sops", "models", "logs"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"SUCCESS: Created directory: {directory}")
    
    # Setup database tables
    print("\nSetting up database tables...")
    if run_command("python -m src.cli setup-db", "Initializing database tables"):
        print("SUCCESS: Database tables created")
    else:
        print("ERROR: Failed to create database tables")
        return
    
    print("\nPostgreSQL setup completed successfully!")
    print("\nNext steps:")
    print("1. Ingest real data: python -m src.cli ingest-real-csv")
    print("2. Start API: python -m src.cli start-api")
    print("3. Start UI: python -m src.cli start-ui")

if __name__ == "__main__":
    main()
