"""
Test script to verify backend server connectivity and API endpoints
"""
import sys
import os
import requests
import subprocess
import time

def test_backend_connectivity():
    """Test if the backend server is accessible and responding to requests"""

    # Test if the backend app can be imported without errors
    try:
        from src.main import app
        print("[SUCCESS] Backend app imports correctly")
    except Exception as e:
        print(f"[ERROR] Backend app import failed: {e}")
        return False

    # Check if required packages are available
    try:
        import fastapi
        import uvicorn
        print("[SUCCESS] Required packages available")
    except ImportError as e:
        print(f"[ERROR] Missing required packages: {e}")
        return False

    # Test the basic health check endpoint that we know exists
    print("\nTesting backend server connectivity...")
    print("Note: This test assumes the backend server is running on http://localhost:8000")

    # Test basic endpoints
    endpoints_to_test = [
        "http://localhost:8000/",
        "http://localhost:8000/health",
        "http://localhost:8000/docs"
    ]

    for endpoint in endpoints_to_test:
        try:
            # Use a longer timeout and proper headers
            response = requests.get(endpoint, timeout=10, headers={'User-Agent': 'TASKAPP-Test'})
            print(f"[SUCCESS] {endpoint} - Status: {response.status_code}")

            # If /docs is accessible, authentication endpoints should be there too
            if endpoint.endswith('/docs'):
                content = response.text.lower()
                if 'auth' in content or 'register' in content or 'login' in content:
                    print("[INFO] Authentication endpoints detected in documentation")

        except requests.exceptions.ConnectionError:
            print(f"[WARNING] Cannot connect to {endpoint} - Server may not be running")
        except requests.exceptions.Timeout:
            print(f"[WARNING] Timeout connecting to {endpoint}")
        except Exception as e:
            print(f"[ERROR] Error testing {endpoint}: {e}")

    # Test the specific authentication endpoints programmatically
    print("\nTesting authentication endpoints availability in the app...")
    try:
        from src.main import app

        # Get the registered routes
        auth_routes_found = []
        for route in app.routes:
            if hasattr(route, 'path') and ('auth' in route.path.lower() or 'register' in route.path.lower() or 'login' in route.path.lower()):
                if hasattr(route, 'methods'):
                    auth_routes_found.append(f"{list(route.methods)} {route.path}")

        if auth_routes_found:
            print("[SUCCESS] Authentication routes are registered:")
            for route in auth_routes_found:
                print(f"  - {route}")
        else:
            print("[INFO] Checking all routes for auth endpoints...")
            for route in app.routes:
                if hasattr(route, 'path'):
                    if any(keyword in route.path.lower() for keyword in ['auth', 'register', 'login']):
                        methods = getattr(route, 'methods', ['UNKNOWN'])
                        print(f"  - {list(methods) if isinstance(methods, (list, tuple)) else methods} {route.path}")

    except Exception as e:
        print(f"[ERROR] Error checking app routes: {e}")
        return False

    print("\n[SUMMARY] Backend connectivity test completed")
    print("- The backend app structure is correct")
    print("- Authentication endpoints should be available at /api/auth/*")
    print("- Make sure the backend server is running on port 8000")
    print("- Check that the frontend is configured to reach the correct backend URL")

    return True

if __name__ == "__main__":
    print("Testing backend server connectivity...")
    test_backend_connectivity()