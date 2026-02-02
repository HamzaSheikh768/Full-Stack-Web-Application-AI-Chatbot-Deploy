#!/usr/bin/env python3
"""
Test script to verify the chatbot functionality
"""

import requests
import json
import time

def test_chatbot():
    """
    Test the chatbot functionality by sending a sample request to the backend API
    """
    print("Testing Chatbot API...")

    # Backend server URL
    backend_url = "http://localhost:8000"

    # Sample user ID (would normally come from authentication)
    user_id = "test_user_123"

    # Test message
    test_message = {
        "message": "Add a task to buy groceries",
        "conversation_id": None  # Will create new conversation
    }

    # Headers (would normally include JWT token)
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"  # Would be needed in real scenario
    }

    # API endpoint
    api_url = f"{backend_url}/api/{user_id}/chat"

    print(f"Sending request to: {api_url}")
    print(f"Message: {test_message}")

    try:
        # Send the request
        response = requests.post(api_url, json=test_message, headers=headers)

        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")

            print("\n✅ Chatbot API test PASSED!")
            print("The chat endpoint is working correctly.")
            return True
        else:
            print(f"❌ Chatbot API test FAILED with status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server")
        print("Make sure the backend server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error during chatbot test: {str(e)}")
        return False

def test_server_health():
    """
    Test that the backend server is running and healthy
    """
    print("\nTesting Backend Server Health...")

    backend_url = "http://localhost:8000"
    health_url = f"{backend_url}/health"

    try:
        response = requests.get(health_url)
        print(f"Health Check Status: {response.status_code}")

        if response.status_code == 200:
            health_data = response.json()
            print(f"Health Data: {health_data}")
            print("✅ Backend server is healthy!")
            return True
        else:
            print(f"❌ Backend server health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during health check: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Chatbot Functionality Test")
    print("="*60)

    # Test server health first
    health_ok = test_server_health()

    if health_ok:
        # Test chatbot functionality
        chat_ok = test_chatbot()

        print("\n" + "="*60)
        if chat_ok:
            print("🎉 ALL TESTS PASSED! Chatbot is working correctly.")
        else:
            print("⚠️  CHATBOT TEST FAILED. Check the backend implementation.")
        print("="*60)
    else:
        print("\n❌ BACKEND SERVER IS NOT HEALTHY. Cannot test chatbot.")