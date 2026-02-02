#!/usr/bin/env python3
"""
Start the server in the background and test the registration endpoint
"""

import subprocess
import time
import requests
import signal
import sys
import os

def main():
    print("Starting backend server...")

    # Change to backend directory and start the server in a subprocess
    os.chdir("backend")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload",
        "--log-level", "debug"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())

    print("Waiting for server to start...")
    time.sleep(3)  # Give the server time to start

    # Test the registration endpoint
    test_email = f"test_{int(time.time())}@example.com"
    print(f"Testing registration with email: {test_email}")

    try:
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

        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            print("✓ SUCCESS: Registration is working!")
        else:
            print("✗ FAILED: Registration still not working")

    except requests.exceptions.RequestException as e:
        print(f"✗ ERROR making request: {e}")

    # Check server logs for errors
    try:
        # Poll the process to see if it's still running
        return_code = server_process.poll()
        if return_code is not None:
            # Process has terminated, get the output
            stdout, stderr = server_process.communicate()
            print("\n--- SERVER STDOUT ---")
            print(stdout.decode())
            print("\n--- SERVER STDERR ---")
            print(stderr.decode())
        else:
            # Process is still running, get current output
            stdout, stderr = server_process.stdout.read(), server_process.stderr.read()
            print("\n--- CURRENT OUTPUT ---")
            print(stdout.decode() if stdout else "No stdout")
            print(stderr.decode() if stderr else "No stderr")
    except Exception as e:
        print(f"Could not read server output: {e}")

    # Terminate the server
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()

    print("\nServer test completed.")

if __name__ == "__main__":
    main()