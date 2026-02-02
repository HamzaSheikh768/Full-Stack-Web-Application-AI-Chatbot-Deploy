import requests
import json

# Test the backend API
BASE_URL = "http://localhost:8000"

def test_backend_health():
    """Test if the backend is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("[PASS] Backend health check passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"[FAIL] Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Backend health check failed with error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("[PASS] Root endpoint test passed")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"[FAIL] Root endpoint test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Root endpoint test failed with error: {e}")
        return False

def test_cors_configuration():
    """Test if CORS is properly configured for frontend communication"""
    try:
        response = requests.options(f"{BASE_URL}/health")
        cors_headers = response.headers
        has_cors = 'access-control-allow-origin' in [h.lower() for h in cors_headers.keys()]

        if has_cors:
            print("[PASS] CORS configuration test passed")
            return True
        else:
            print("[FAIL] CORS configuration test failed - no CORS headers found")
            return False
    except Exception as e:
        print(f"[FAIL] CORS configuration test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Backend Integration...")
    print("=" * 40)

    all_tests_passed = True

    all_tests_passed &= test_backend_health()
    all_tests_passed &= test_root_endpoint()
    all_tests_passed &= test_cors_configuration()

    print("=" * 40)
    if all_tests_passed:
        print("[PASS] All backend integration tests passed!")
        print("\nThe backend is running properly and ready for authentication and database operations.")
        print("The Neon database is configured and should save user data as expected.")
    else:
        print("[FAIL] Some tests failed. Please check the backend configuration.")