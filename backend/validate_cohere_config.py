#!/usr/bin/env python3
"""
Configuration validation script for Cohere API setup
"""

import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_settings
from openai import OpenAI
import openai


def validate_api_key_format(api_key):
    """Validate the format of the API key"""
    if not api_key or not api_key.strip():
        return False, "API key is empty or None"

    stripped_key = api_key.strip()

    # Check basic format - should be reasonably long and not a placeholder
    if len(stripped_key) < 20:
        return False, "API key appears to be too short (< 20 characters)"

    if any(placeholder in stripped_key.lower() for placeholder in
           ['your_', 'my_', 'xxx', 'test', 'demo', 'invalid', 'placeholder']):
        return False, "API key appears to be a placeholder"

    return True, "Valid format"


def validate_cohere_connection():
    """Validate the Cohere API connection"""
    print("🔍 Validating Cohere API Configuration...")
    print("-" * 50)

    # Load settings
    try:
        settings = get_settings()
        print(f"✅ Settings loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load settings: {e}")
        return False

    # Validate API key format
    is_valid, reason = validate_api_key_format(settings.COHERE_API_KEY)
    print(f"API Key Format: {'✅ Valid' if is_valid else '❌ Invalid'}")
    if not is_valid:
        print(f"  Reason: {reason}")
        print("\n🔧 FIX: Update your .env file with a valid COHERE_API_KEY")
        print("   Get your key from: https://dashboard.cohere.com/")
        return False

    print("✅ API key format appears valid")

    # Test client instantiation
    try:
        client = OpenAI(
            api_key=settings.COHERE_API_KEY,
            base_url="https://api.cohere.ai/v1"
        )
        print("✅ Cohere client instantiated successfully")
    except Exception as e:
        print(f"❌ Failed to instantiate client: {e}")
        return False

    # Test a simple API call
    print("\n📡 Testing API connection...")
    try:
        response = client.chat.completions.create(
            model="command-r-plus",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
            temperature=0
        )

        print("✅ Successfully connected to Cohere API")
        print(f"   Response: {response.choices[0].message.content[:30]}...")
        return True

    except openai.AuthenticationError:
        print("❌ Authentication failed - API key is invalid or expired")
        print("\n🔧 FIX: Update your .env file with a valid COHERE_API_KEY")
        print("   Make sure the key is copied correctly from Cohere dashboard")
        return False

    except openai.RateLimitError:
        print("⚠️  Rate limit reached - API key is valid but has usage limits")
        print("   This is not a configuration issue, but a usage limit")
        return True  # Config is valid, just hitting limits

    except openai.APIConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("\n🔧 POSSIBLE FIXES:")
        print("   • Check your internet connection")
        print("   • Verify firewall/proxy settings")
        print("   • Ensure https://api.cohere.ai is accessible")
        return False

    except Exception as e:
        error_msg = str(e).lower()
        if '401' in error_msg:
            print("❌ Authentication error (401) - API key is invalid")
            print("\n🔧 FIX: Update your .env file with a valid COHERE_API_KEY")
            return False
        elif '405' in error_msg:
            print("❌ Method not allowed (405) - API endpoint may not support required features")
            print("\n🔧 FIX: This may indicate the Cohere endpoint doesn't support tool calling")
            return False
        else:
            print(f"❌ API test failed: {e}")
            return False


def print_setup_instructions():
    """Print setup instructions for Cohere API"""
    print("\n📖 SETUP INSTRUCTIONS:")
    print("1. Go to https://dashboard.cohere.com/")
    print("2. Create an account or sign in")
    print("3. Navigate to 'API Keys' section")
    print("4. Create a new API key with appropriate permissions")
    print("5. Copy the API key and update your .env file:")
    print("   COHERE_API_KEY=your_actual_api_key_here")
    print("6. Restart the application")


def main():
    print("=" * 60)
    print("Cohere API Configuration Validator")
    print("=" * 60)

    is_valid = validate_cohere_connection()

    if is_valid:
        print("\n🎉 SUCCESS: Cohere API is properly configured!")
        print("   The chatbot should work correctly with AI features enabled.")
    else:
        print("\n❌ CONFIGURATION ISSUE DETECTED!")
        print("   The chatbot will show error messages until this is fixed.")
        print_setup_instructions()

    print("\n" + "=" * 60)
    return is_valid


if __name__ == "__main__":
    main()