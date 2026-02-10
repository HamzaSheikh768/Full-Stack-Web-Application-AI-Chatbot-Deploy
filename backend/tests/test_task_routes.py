"""
Test script to verify task route functionality
"""
import asyncio
import httpx
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

async def test_task_routes():
    """Test task route functionality"""
    base_url = "http://localhost:8000"

    print("Testing TASKAPP task route functionality...")
    print("="*60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test health check
        print("\n1. Testing health check...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"   Health check response: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ Health check passed")
            else:
                print("   ⚠ Health check failed")
        except Exception as e:
            print(f"   ⚠ Health check failed: {e}")
            print("   Note: The backend server might not be running. Please start the server first.")

        # Test that the routes exist
        print("\n2. Testing route existence...")
        try:
            # Try to access a route that requires authentication
            # This should return 401/403 rather than 404 if the route exists
            response = await client.get(f"{base_url}/api/nonexistent_user/tasks")
            print(f"   Tasks route response: {response.status_code}")
            
            # If we get 404, the route doesn't exist
            # If we get 401/403, the route exists but requires auth
            if response.status_code in [401, 403]:
                print("   ✓ Tasks route exists and requires authentication")
            elif response.status_code == 404:
                print("   ⚠ Tasks route does not exist")
            else:
                print(f"   ? Tasks route exists with status {response.status_code}")
                
        except Exception as e:
            print(f"   ⚠ Error testing route: {e}")
            print("   Note: The backend server might not be running. Please start the server first.")

    print("\n⚠ Server needs to be running to fully test the routes.")
    print("Please start the backend server with 'python -m uvicorn src.main:app --reload' before running this test.")

if __name__ == "__main__":
    asyncio.run(test_task_routes())