#!/usr/bin/env python3
"""
This is a minimal script to test the Gemini API directly.
"""

import google.generativeai as genai

def test_gemini():
    # Your API key 
    API_KEY = "AIzaSyAB5jKOflFnIQ5-4bPoYKbeDIr9DZ-f3Lc"
    
    # Configure Gemini
    genai.configure(api_key=API_KEY)
    
    # Create model
    model = genai.GenerativeModel("gemini-pro")
    
    # Test prompt
    response = model.generate_content("Hello, is this working?")
    
    # Print response
    print(response.text)
    
    print("\nSuccess! The Gemini API is working correctly.")

if __name__ == "__main__":
    try:
        test_gemini()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPossible solutions:")
        print("1. Ensure your API key is valid")
        print("2. Enable the Gemini API for your project")
        print("3. The key needs permission to access the Gemini API")
        print("4. Try accessing https://makersuite.google.com/ with your Google account to verify access") 