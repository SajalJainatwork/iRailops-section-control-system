#!/usr/bin/env python3
"""
Open Source Model Setup Script for Railway Operations System
"""

import subprocess
import sys
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("❌ Ollama is not responding")
            return False
    except:
        print("❌ Ollama is not running")
        return False

def install_ollama_model(model_name="llama2"):
    """Install Ollama model"""
    print(f"🔄 Installing Ollama model: {model_name}")
    try:
        result = subprocess.run(f"ollama pull {model_name}", shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Model {model_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install model {model_name}: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🤖 Open Source Model Setup")
    print("=" * 50)
    
    # Install Python dependencies
    if not run_command("pip install ollama sentence-transformers transformers torch", "Installing open-source model dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check if Ollama is installed
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
        else:
            print("❌ Ollama is not installed")
            print("Please install Ollama from: https://ollama.ai")
            print("Or run: curl -fsSL https://ollama.ai/install.sh | sh")
            sys.exit(1)
    except:
        print("❌ Ollama is not installed")
        print("Please install Ollama from: https://ollama.ai")
        sys.exit(1)
    
    # Check if Ollama is running
    if not check_ollama():
        print("🔄 Starting Ollama...")
        try:
            subprocess.Popen("ollama serve", shell=True)
            import time
            time.sleep(3)  # Wait for Ollama to start
        except:
            print("❌ Failed to start Ollama")
            print("Please start Ollama manually: ollama serve")
    
    # Install recommended models
    models = ["llama2", "mistral"]
    for model in models:
        if install_ollama_model(model):
            break  # Install at least one model
    
    print("\n🎉 Open Source Model Setup Completed!")
    print("\nAvailable models:")
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        print(result.stdout)
    except:
        print("Could not list models")
    
    print("\nNext steps:")
    print("1. Run: python setup.py")
    print("2. Start services: python -m src.cli start-api")
    print("3. Access UI: http://localhost:8501")

if __name__ == "__main__":
    main()
