#!/usr/bin/env python3
"""
Diagnostic script to check Cohere API configuration and connectivity
"""

import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend/src"))

from src.config import get_settings
import openai
from openai import OpenAI


def check_environment():
    """Check if environment variables are properly set"""
    print("🔍 Checking Environment Variables...")

    # Load settings to check if they can be loaded
    try:
        settings = get_settings()
        print("✅ Settings loaded successfully")

        # Check if COHERE_API_KEY is present and not empty
        if settings.COHERE_API_KEY and settings.COHERE_API_KEY.strip():
            print("✅ COHERE_API_KEY is present in environment")

            # Check if it looks like a real API key (not a placeholder)
            api_key = settings.COHERE_API_KEY.strip()
            if len(api_key) >= 20 and not api_key.startswith("YOUR_") and not api_key.startswith("your_"):
                print("✅ COHERE_API_KEY appears to be a valid format")
                return True
            else:
                print("❌ COHERE_API_KEY appears to be a placeholder or invalid")
                return False
        else:
            print("❌ COHERE_API_KEY is missing or empty")
            return False

    except Exception as e:
        print(f"❌ Failed to load settings: {str(e)}")
        return False


def test_cohere_client_configuration():
    """Test if the Cohere client can be properly instantiated"""
    print("\n🔍 Testing Cohere Client Configuration...")

    try:
        # Create the OpenAI client with Cohere configuration
        client = OpenAI(
            api_key=os.getenv("COHERE_API_KEY"),
            base_url="https://api.cohere.ai/v1"
        )

        print("✅ Cohere client instantiated successfully")
        print(f"   Base URL: https://api.cohere.ai/v1")
        print(f"   Model: command-r-plus")
        return client

    except Exception as e:
        print(f"❌ Failed to instantiate Cohere client: {str(e)}")
        return None


def test_basic_connection(client):
    """Test basic connection to Cohere API"""
    print("\n🔍 Testing Basic Connection to Cohere API...")

    try:
        # Make a simple test call (non-tool-related to avoid complexity)
        response = client.chat.completions.create(
            model="command-r-plus",
            messages=[{"role": "user", "content": "Hello, are you available?"}],
            max_tokens=10,
            temperature=0
        )

        print("✅ Successfully connected to Cohere API")
        print(f"   Response received: {response.choices[0].message.content[:50]}...")
        return True

    except openai.AuthenticationError as e:
        print(f"❌ Authentication failed: {str(e)}")
        print("   This indicates the API key is invalid or expired")
        return False
    except openai.RateLimitError as e:
        print(f"⚠️  Rate limit exceeded: {str(e)}")
        print("   The API key is valid but has hit usage limits")
        return True  # Key is valid, just limited
    except openai.APIConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        print("   This might indicate network issues or incorrect endpoint")
        return False
    except openai.NotFoundError as e:
        print(f"❌ Model not found: {str(e)}")
        print("   The model 'command-r-plus' might not be available")
        return False
    except Exception as e:
        error_msg = str(e).lower()
        if '401' in error_msg or 'auth' in error_msg or 'key' in error_msg:
            print(f"❌ Authentication error: {str(e)}")
            print("   This indicates the API key is invalid or expired")
            return False
        elif '405' in error_msg or 'method' in error_msg:
            print(f"❌ Method not allowed: {str(e)}")
            print("   The API endpoint might not support the required method")
            return False
        else:
            print(f"❌ Connection test failed: {str(e)}")
            return False


def main():
    print("="*60)
    print("Cohere API Diagnostic Tool")
    print("="*60)

    # Check environment
    env_ok = check_environment()

    if not env_ok:
        print("\n❌ DIAGNOSIS: Environment configuration issue detected!")
        print("   Please ensure your .env file contains a valid COHERE_API_KEY")
        print("   Get your API key from: https://dashboard.cohere.com/")
        return False

    # Test client configuration
    client = test_cohere_client_configuration()

    if not client:
        print("\n❌ DIAGNOSIS: Client configuration issue detected!")
        print("   There might be an issue with the Cohere API endpoint configuration")
        return False

    # Test basic connection
    connection_ok = test_basic_connection(client)

    if not connection_ok:
        print("\n❌ DIAGNOSIS: Connection to Cohere API failed!")
        print("   Please check:")
        print("   1. Your COHERE_API_KEY is valid and active")
        print("   2. Your internet connection is working")
        print("   3. There are no firewall restrictions blocking the API")
        return False

    print("\n✅ DIAGNOSIS: All tests passed! Cohere API is accessible.")
    print("   The chatbot should be able to connect to the AI service.")
    return True


if __name__ == "__main__":
    success = main()
    print("\n" + "="*60)
    if success:
        print("🎉 CONCLUSION: Cohere API is properly configured and accessible!")
    else:
        print("⚠️  CONCLUSION: Issues were detected with the Cohere API configuration.")
    print("="*60)