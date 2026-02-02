#!/usr/bin/env python3
"""Simple test server to debug the signup endpoint"""

from src.main import app
import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import sys

# Add global exception handler to see detailed errors
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Exception in request {request.method} {request.url}: {e}")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"type": "InternalServerError", "message": str(e)}}
        )

if __name__ == "__main__":
    print("Starting server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")