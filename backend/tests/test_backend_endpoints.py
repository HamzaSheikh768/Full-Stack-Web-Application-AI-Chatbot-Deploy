import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:8000"

def test_backend_endpoints():
    """Test if the backend API endpoints are working properly"""
    print("Testing Backend API Endpoints...")

    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health endpoint failed: {e}")

    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")

    # Try to test the signup endpoint (will fail with validation error, but should be accessible)
    try:
        response = requests.post(f"{BASE_URL}/api/signup", json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        })
        print(f"Signup endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Signup response: {response.text}")
    except Exception as e:
        print(f"Signup endpoint failed: {e}")

    print("Backend API test completed.")

if __name__ == "__main__":
    test_backend_endpoints()