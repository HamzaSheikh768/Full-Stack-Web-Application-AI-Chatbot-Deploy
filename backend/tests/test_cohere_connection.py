#!/usr/bin/env python3
"""
Test script to verify Cohere API connectivity and configuration
"""

import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_settings
from src.agent.core import client
from openai import OpenAI


def test_cohere_connection():
    """Test the Cohere API connection"""
    print("Testing Cohere API Connection...")

    try:
        # Get settings to check if API key is available
        settings = get_settings()
        print(f"✅ Successfully loaded settings")
        print(f"   API key is {'present' if settings.COHERE_API_KEY else 'missing'}")

        if not settings.COHERE_API_KEY:
            print("❌ COHERE_API_KEY is not set in environment")
            return False

        # Test a simple API call to check connectivity
        print("\nMaking a test call to Cohere API...")

        response = client.chat.completions.create(
            model="command-r-plus",
            messages=[{"role": "user", "content": "Hello, test connection"}],
            max_tokens=10
        )

        print(f"✅ Successfully connected to Cohere API")
        print(f"   Response received: {response.choices[0].message.content[:50]}...")
        return True

    except Exception as e:
        print(f"❌ Failed to connect to Cohere API: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False


def test_tool_definitions():
    """Test that the tool definitions are properly loaded"""
    print("\nTesting tool definitions...")

    try:
        from src.mcp.tools import all_tools
        print(f"✅ Successfully loaded {len(all_tools)} tools:")
        for tool in all_tools:
            print(f"   - {tool.__name__}")

        return True
    except Exception as e:
        print(f"❌ Failed to load tools: {str(e)}")
        return False


def test_agent_creation():
    """Test that an agent can be created properly"""
    print("\nTesting agent creation...")

    try:
        from src.agent.core import get_agent
        agent_data = get_agent("test_user_123")

        print(f"✅ Successfully created agent")
        print(f"   Model: {agent_data['model']}")
        print(f"   Number of tools: {len(agent_data['tools'])}")

        return True
    except Exception as e:
        print(f"❌ Failed to create agent: {str(e)}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("Cohere API Connection Test")
    print("="*60)

    success_count = 0
    total_tests = 3

    if test_cohere_connection():
        success_count += 1

    if test_tool_definitions():
        success_count += 1

    if test_agent_creation():
        success_count += 1

    print("\n" + "="*60)
    print(f"Test Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! Cohere API is properly configured.")
    else:
        print("⚠️  Some tests failed. Please check your Cohere API configuration.")

    print("="*60)