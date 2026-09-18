#!/usr/bin/env python3
"""
Debug script to test configuration loading
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_config():
    """Test configuration loading"""
    print("🔍 Testing configuration...")
    
    try:
        from src.config import settings
        print("✅ Configuration loaded successfully")
        print(f"Database URL: {settings.database_url}")
        print(f"LLM Model Type: {settings.llm_model_type}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\n🗄️  Testing database...")
    
    try:
        from src.data.database import init_database
        init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database failed: {e}")
        return False

def main():
    """Main debug function"""
    print("🐛 Debug Script for Railway Operations System")
    print("=" * 50)
    
    # Test configuration
    if not test_config():
        print("\n❌ Configuration test failed")
        return
    
    # Test database
    if not test_database():
        print("\n❌ Database test failed")
        return
    
    print("\n🎉 All tests passed! System is ready to run.")

if __name__ == "__main__":
    main()
