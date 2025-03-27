#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import sys

def main():
    # Print current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        print(f".env file found at: {env_path}")
        # Read raw contents of .env file
        with open(env_path, 'r') as f:
            print("\nRaw .env file contents:")
            print("="*50)
            for line in f:
                if 'API_KEY' in line:
                    # Only show first few and last few chars of API keys
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        key, value = parts
                        value = value.strip()
                        if len(value) > 10:
                            censored = f"{value[:5]}...{value[-4:]}"
                            print(f"{key}={censored}")
                        else:
                            print(line.strip())
                else:
                    print(line.strip())
            print("="*50)
    else:
        print(f"ERROR: .env file not found at: {env_path}")
    
    # Try to load environment variables
    print("\nAttempting to load environment variables...")
    load_dotenv(env_path)
    
    # Check environment variables
    gemini_key = os.getenv("GEMINI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print("\nEnvironment variables after loading:")
    print(f"GEMINI_API_KEY: {gemini_key[:5]}...{gemini_key[-4:] if gemini_key and len(gemini_key) > 10 else 'Not set'}")
    print(f"GOOGLE_API_KEY: {google_key[:5]}...{google_key[-4:] if google_key and len(google_key) > 10 else 'Not set'}")
    
    # Test direct import of genai
    print("\nTesting direct import of google.generativeai...")
    try:
        import google.generativeai as genai
        print("Successfully imported google.generativeai")
        
        # Try to configure genai
        if gemini_key:
            print(f"Configuring genai with API key: {gemini_key[:5]}...")
            genai.configure(api_key=gemini_key)
            print("Successfully configured genai with API key")
            
            # Try to create a model
            print("Attempting to create a model instance...")
            model_name = "gemini-pro"  # Use a known working model
            model = genai.GenerativeModel(model_name)
            print(f"Successfully created model instance with model: {model_name}")
            
            # Try a simple test prompt
            print("Testing with a simple prompt...")
            response = model.generate_content("Hello, are you working?")
            print(f"Response from model: {response.text[:50]}...")
            
            print("\n✅ SUCCESS: API key is working correctly!")
        else:
            print("❌ ERROR: No API key available to configure genai")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main() 