import subprocess
import time
import requests
import signal
import sys
import os

def test_registration():
    # Change to backend directory
    os.chdir("backend")

    # Start the server in the background
    print("Starting server...")
    process = subprocess.Popen([
        "python", "-m", "uvicorn",
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ])

    # Wait for server to start
    time.sleep(5)

    try:
        # Test the registration endpoint
        test_email = f"test_{int(time.time())}@example.com"
        print(f"Testing registration with: {test_email}")

        response = requests.post(
            "http://127.0.0.1:8000/api/auth/register",
            headers={"Content-Type": "application/json"},
            json={
                "email": test_email,
                "password": "TestPass123!",
                "name": "Test User"
            },
            timeout=10
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Terminate the server
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    test_registration()