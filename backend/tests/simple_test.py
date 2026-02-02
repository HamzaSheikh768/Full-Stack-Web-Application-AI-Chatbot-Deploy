#!/usr/bin/env python3
"""
Simple test to check Cohere API configuration
"""

import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_settings
from openai import OpenAI
import openai

def test_api_key():
    """Test the Cohere API key configuration"""
    print("Checking Cohere API Configuration...")

    # Load settings
    try:
        settings = get_settings()
        print("[OK] Settings loaded successfully")

        # Check if API key exists
        api_key = settings.COHERE_API_KEY
        print(f"[OK] COHERE_API_KEY found in settings")

        if api_key and len(api_key.strip()) > 0:
            print(f"[OK] API key is present (length: {len(api_key)})")

            # Check if it looks like a real key (not a placeholder)
            if len(api_key) >= 20 and not api_key.startswith("YOUR_") and not api_key.startswith("your_"):
                print("[OK] API key appears to be in valid format")

                # Test client creation
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.cohere.ai/v1"
                    )
                    print("[OK] Cohere client created successfully")

                    # Try a simple test call
                    try:
                        print("Attempting API connection test...")
                        response = client.chat.completions.create(
                            model="command-r-plus",
                            messages=[{"role": "user", "content": "test"}],
                            max_tokens=5,
                            temperature=0
                        )

                        print("[OK] Successfully connected to Cohere API")
                        print(f"Response: {response.choices[0].message.content}")
                        return True

                    except openai.AuthenticationError as e:
                        print(f"[ERROR] Authentication failed: {e}")
                        print("The API key is invalid or expired")
                        return False

                    except Exception as e:
                        print(f"[ERROR] API test failed: {e}")
                        error_msg = str(e).lower()
                        if '401' in error_msg:
                            print("[ERROR] Authentication error (401) - API key is invalid")
                        elif '405' in error_msg:
                            print("[ERROR] Method not allowed (405) - API endpoint may not support required features")
                        elif '404' in error_msg:
                            print("[ERROR] Endpoint not found (404) - API endpoint may be incorrect")
                        return False

                except Exception as e:
                    print(f"[ERROR] Client creation failed: {e}")
                    return False
            else:
                print("[ERROR] API key appears to be a placeholder")
                print(f"Current key: {api_key[:20]}...")
                return False
        else:
            print("[ERROR] API key is missing or empty")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to load settings: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Simple Cohere API Configuration Test")
    print("=" * 60)

    success = test_api_key()

    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: Cohere API is properly configured!")
    else:
        print("FAILURE: Cohere API configuration needs to be fixed.")
        print("\nTO FIX:")
        print("1. Get a valid API key from https://dashboard.cohere.com/")
        print("2. Update your .env file with COHERE_API_KEY=your_actual_key")
        print("3. Restart the application")
    print("=" * 60)