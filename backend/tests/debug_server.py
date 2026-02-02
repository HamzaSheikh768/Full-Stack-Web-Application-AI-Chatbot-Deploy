#!/usr/bin/env python3
"""Debug server to identify the exact error"""

from src.main import app
import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import sys

# Add global exception handler
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
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)