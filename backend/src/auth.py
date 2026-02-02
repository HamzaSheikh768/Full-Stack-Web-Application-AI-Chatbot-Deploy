from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import os

from .utils import verify_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get the current authenticated user from the JWT token.
    This validates the token and extracts user information.
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from the token payload
    user_id = payload.get("sub")  # 'sub' is standard JWT claim for subject/user ID

    # For compatibility with different auth systems, also check for 'user_id'
    if not user_id:
        user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user information",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user information
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "username": payload.get("username")
    }


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource.
    Returns True if the user owns the resource, False otherwise.
    """
    return user_id == resource_user_id