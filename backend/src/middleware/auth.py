from fastapi import HTTPException, status, Request
from typing import Dict, Any, Callable
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def validate_user_isolation(user_id: str, resource_user_id: str):
    """
    Validates that the authenticated user can only access resources they own.
    Raises HTTPException if the user does not have access to the resource.
    """
    if user_id != resource_user_id:
        logger.warning(f"User {user_id} attempted to access resource belonging to {resource_user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )


def require_user_isolation(get_resource_user_id_func: Callable[[Any], str]):
    """
    Decorator to enforce user isolation on route handlers.
    Expects a function that can extract the resource owner's user ID from the resource.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user from kwargs (should be injected by auth dependency)
            current_user = kwargs.get('current_user')
            if not current_user or 'user_id' not in current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Extract resource from kwargs
            resource = kwargs.get('resource') or kwargs.get('task') or kwargs.get('db_task')
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Resource not found in request"
                )
            
            # Get the resource owner's user ID
            resource_user_id = get_resource_user_id_func(resource)
            
            # Validate user isolation
            validate_user_isolation(current_user['user_id'], resource_user_id)
            
            # If validation passes, proceed with the original function
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class UserIsolationMiddleware:
    """
    Middleware to enforce user isolation across the application.
    This middleware checks that users can only access their own resources.
    """
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Only process HTTP requests
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        request = Request(scope)
        
        # Add user isolation validation to the request state
        # This will be used by individual route handlers
        request.state.validate_user_isolation = validate_user_isolation
        
        # Continue with the request
        return await self.app(scope, receive, send)


# Specific validation functions for different resource types
def validate_task_user_isolation(current_user_id: str, task_user_id: str):
    """Specific validation for task resources"""
    validate_user_isolation(current_user_id, task_user_id)


def validate_conversation_user_isolation(current_user_id: str, conversation_user_id: str):
    """Specific validation for conversation resources"""
    validate_user_isolation(current_user_id, conversation_user_id)


def validate_document_user_isolation(current_user_id: str, document_user_id: str):
    """Specific validation for document resources"""
    validate_user_isolation(current_user_id, document_user_id)