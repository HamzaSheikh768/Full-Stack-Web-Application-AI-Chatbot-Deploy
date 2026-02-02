import subprocess
import time
import requests
import threading

def start_server():
    """Start the backend server in a subprocess"""
    import os
    os.chdir(r"E:\Hackathon 2\Pahse-III\Full-Stack-Web-Application-AI-Chatbot\backend")

    process = subprocess.Popen([
        "python", "-m", "uvicorn",
        "src.main:app",
        "--reload",
        "--port", "8000",
        "--log-level", "info"
    ])

    # Wait for server to start
    time.sleep(3)

    return process

def test_registration():
    """Test the registration endpoint"""
    # Wait a bit for server to start
    time.sleep(5)

    print("Testing registration functionality...")

    # Create unique email for test
    import time
    timestamp = int(time.time())
    test_email = f"testuser_{timestamp}@example.com"

    registration_data = {
        "email": test_email,
        "password": "TestPass123!",
        "name": "Test User"
    }

    print(f"Attempting to register user: {test_email}")

    try:
        response = requests.post(
            "http://localhost:8000/api/auth/register",
            headers={"Content-Type": "application/json"},
            json=registration_data
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Registration worked!")
            return True
        else:
            print(f"ERROR: Registration failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Starting server and testing registration...")

    # Start server in background
    server_process = start_server()

    try:
        # Test registration
        success = test_registration()

        if success:
            print("\nSUCCESS: Registration is working!")
        else:
            print("\nFAILURE: Registration still has issues")

    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()