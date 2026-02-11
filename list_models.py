"""
List available Gemini models
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    print("Please set GEMINI_API_KEY in your .env file")
    sys.exit(1)

print("🔍 Checking available Gemini models...")
print()

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    print("Available models:")
    print("-" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Input limit: {model.input_token_limit} tokens")
            print(f"  Output limit: {model.output_token_limit} tokens")
            print()
    
    print("-" * 60)
    print()
    print("💡 Recommended models:")
    print("  - gemini-flash-latest (default, fast & efficient)")
    print("  - gemini-pro")
    print("  - gemini-1.5-flash")
    print()
    print("To use a specific model, add to .env:")
    print("  GEMINI_MODEL=gemini-flash-latest")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Common issues:")
    print("  1. Invalid API key")
    print("  2. API not enabled in Google Cloud")
    print("  3. Network connection issue")
    sys.exit(1)
