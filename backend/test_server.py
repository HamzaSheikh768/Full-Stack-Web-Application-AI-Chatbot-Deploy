import sys
import os
import threading
import time

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_server():
    try:
        from src.main import app
        import uvicorn
        
        print("Starting server...")
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the server in a thread to allow timeout
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a bit to see if there are any startup errors
    time.sleep(10)
    
    print("Server startup completed or timed out.")