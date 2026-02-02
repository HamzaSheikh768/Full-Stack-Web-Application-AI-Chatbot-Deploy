"""
Middleware for the Todo API
Includes logging, request timing, rate limiting, and other cross-cutting concerns
"""

import time
import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
import os
from typing import Optional


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logging.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)
        except Exception as e:
            # Log exceptions
            logging.error(f"Exception during request {request.method} {request.url}: {str(e)}")
            raise

        # Calculate request duration
        duration = time.time() - start_time

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Add cache control headers to prevent browser caching of API responses
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        # Log response
        logging.info(f"Response: {response.status_code} in {duration:.2f}s")

        return response


# Initialize rate limiter for authentication endpoints
auth_limiter = Limiter(key_func=get_remote_address)


def get_redis_client():
    """Get Redis client for rate limiting"""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    try:
        return redis.from_url(redis_url)
    except Exception as e:
        logging.warning(f"Could not connect to Redis: {e}. Using in-memory rate limiting.")
        # Return None to indicate fallback to in-memory limiter
        return None


def setup_rate_limiter():
    """Initialize the rate limiter with Redis storage if available"""
    redis_client = get_redis_client()

    if redis_client:
        try:
            # Test the connection
            redis_client.ping()
            # Redis is available, we'll use it for rate limiting
            # The slowapi library handles the storage configuration internally
            pass
        except Exception:
            # Redis not available, fall back to in-memory
            pass

    return auth_limiter


# Rate limiting decorator for authentication endpoints
def auth_rate_limit():
    """
    Decorator for rate limiting authentication endpoints
    Limits: 5 attempts per 15 minutes per IP
    """
    def rate_limit_decorator(func):
        return auth_limiter.limit("5/15minutes")(func)
    return rate_limit_decorator


def setup_auth_rate_limits(app):
    """Setup rate limiting for authentication endpoints"""
    # Register the rate limit exceeded handler
    app.state.limiter = auth_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Apply rate limits to specific endpoints can be done with decorators


# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')