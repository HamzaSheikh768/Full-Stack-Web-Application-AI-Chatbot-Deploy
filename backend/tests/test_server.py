#!/usr/bin/env python3
"""
Test script to start server and capture actual error
"""

import subprocess
import time
import threading
import sys
import os

def run_server():
    """Function to run the server in a subprocess"""
    os.chdir("backend")

    # Start the server
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload",
        "--log-level", "debug"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the server output as it comes
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"[SERVER] {output.strip()}")

    # Get return code
    rc = process.poll()
    return rc

if __name__ == "__main__":
    print("Starting server to capture error logs...")
    run_server()