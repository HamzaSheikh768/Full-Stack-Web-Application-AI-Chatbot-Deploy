from fastapi import HTTPException, status, Request
from typing import Dict
import time
from collections import defaultdict
import asyncio

# Simple in-memory rate limiter (in production, use Redis or similar)
class InMemoryRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if a request from the given identifier is allowed based on rate limits.
        """
        now = time.time()
        # Clean old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if now - req_time < window_seconds
        ]
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False

# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from the request.
    """
    # Check for forwarded IP headers first (for when behind proxies/load balancers)
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # Take the first IP in the list (client's original IP)
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    
    # Fallback to direct client IP
    return request.client.host


def rate_limit(max_requests: int, window_seconds: int):
    """
    Decorator to apply rate limiting to FastAPI endpoints.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request object from kwargs
            request = kwargs.get('request')
            if not request:
                # Look for request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            # Get client IP for rate limiting
            client_ip = get_client_ip(request)
            
            # Check if request is allowed
            if not rate_limiter.is_allowed(client_ip, max_requests, window_seconds):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {max_requests} requests per {window_seconds} seconds"
                )
            
            # If allowed, proceed with the original function
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Predefined rate limits for different types of endpoints
DEFAULT_RATE_LIMITS = {
    'api': (100, 3600),  # 100 requests per hour for general API
    'auth': (5, 60),     # 5 requests per minute for auth endpoints
    'search': (30, 60),  # 30 requests per minute for search
    'create': (20, 60),  # 20 create requests per minute
}


def apply_rate_limit(endpoint_type: str = 'api'):
    """
    Apply a predefined rate limit based on endpoint type.
    """
    if endpoint_type not in DEFAULT_RATE_LIMITS:
        endpoint_type = 'api'  # default
    
    max_req, window = DEFAULT_RATE_LIMITS[endpoint_type]
    return rate_limit(max_req, window)


class RateLimitMiddleware:
    """
    Middleware to apply rate limiting globally or to specific routes.
    """
    
    def __init__(self, app, default_limits: tuple = (100, 3600)):
        self.app = app
        self.default_max_requests, self.default_window = default_limits
        self.rate_limiter = InMemoryRateLimiter()

    async def __call__(self, scope, receive, send):
        # Only process HTTP requests
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        request = Request(scope)
        
        # Get client IP
        client_ip = get_client_ip(request)
        
        # Apply default rate limit (can be overridden by route-specific limits)
        if not self.rate_limiter.is_allowed(
            client_ip, 
            self.default_max_requests, 
            self.default_window
        ):
            # Create a response for rate limit exceeded
            async def send_response():
                response_headers = [
                    (b"content-type", b"text/plain"),
                    (b"x-rate-limit", f"{self.default_max_requests}".encode()),
                    (b"x-rate-window", f"{self.default_window}".encode()),
                ]
                await send({
                    "type": "http.response.start",
                    "status": 429,
                    "headers": response_headers
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Rate limit exceeded",
                    "more_body": False
                })
            
            await send_response()
            return
        
        # Add rate limiter to request state for route-specific usage
        request.state.rate_limiter = self.rate_limiter
        
        # Continue with the request
        return await self.app(scope, receive, send)