from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import task_routes, public_task_routes, chat_routes
from .api import dashboard_routes, auth_routes
from .database.db import create_db_and_tables
from sqlmodel import SQLModel
import asyncio
from .middleware import LoggingMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup"""
    try:
        # Attempt to initialize database tables with timeout/error handling
        # Since we've already run migrations, we may not need this during startup
        # Only run if needed, and handle potential connection issues gracefully
        create_db_and_tables()  # Sync function call
    except Exception as e:
        print(f"Warning: Could not initialize database tables on startup: {e}")
        # Continue starting the app even if DB initialization fails
    yield
    # Shutdown operations would go here

# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    description="Secure, RESTful API for todo application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend/backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Next.js default
        "http://localhost:3001",    # Next.js alternative
        "http://127.0.0.1:3000",    # Next.js default alternative
        "http://127.0.0.1:3001",    # Next.js alternative
        "https://localhost:3000",   # HTTPS for local development if needed
        "https://localhost:3001",   # HTTPS for local development if needed
        os.getenv("NEXT_PUBLIC_FRONTEND_URL", "http://localhost:3000"),  # Production frontend URL from env
        "*"  # Allow all origins for development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    # Allow credentials (for cookies, authorization headers)
    # This is important for auth flows
)

# Add middleware
app.add_middleware(LoggingMiddleware)



# Include public task routes for dashboard and public access
app.include_router(public_task_routes.router, prefix="/api", tags=["public-tasks"])

# Include dashboard routes
app.include_router(dashboard_routes.router, prefix="/api", tags=["dashboard"])

# Include task routes - authenticated access
# Routes now have full path structure like /users/{user_id}/tasks
app.include_router(task_routes.router, prefix="/api", tags=["tasks"])





# Include chat routes for AI assistant
app.include_router(chat_routes.router, prefix="/api", tags=["chat"])

# Include auth routes
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Todo API - Welcome!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add exception handlers
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "details": exc.errors()
            }
        }
    )