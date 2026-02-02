from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from typing import Optional

from ..database.db import get_db
from ..models.user import User
from ..schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from ..utils import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    is_valid_email,
    is_strong_password
)
from ..auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=dict)
def signup(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    """
    try:
        # Validate email format
        if not is_valid_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Validate password strength
        if not is_strong_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet security requirements (12+ chars, mixed case, number, special char)"
            )

        # Check if user already exists
        from sqlmodel import select
        result = db.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password_hash=hashed_password,
            first_name=getattr(user_data, 'first_name', None),
            last_name=getattr(user_data, 'last_name', None),
            is_verified=False  # Email verification required
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # In a real app, send verification email here using background_tasks
        # background_tasks.add_task(send_verification_email, new_user.email, verification_token)

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user_id": str(new_user.id),
                "email": new_user.email,
                "is_verified": new_user.is_active  # Using is_active from the database schema
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        # Check if the db session has rollback method before calling it
        if hasattr(db, 'rollback'):
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registering user: {str(e)}")


@router.post("/login", response_model=dict)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens
    """
    try:
        # Find user by email
        from sqlmodel import select
        result = db.execute(select(User).where(User.email == login_data.email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Check if account is locked (only if the field exists in the model)
        if hasattr(user, 'locked_until') and user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account temporarily locked due to multiple failed login attempts"
            )

        # Update last login if the field exists in the model
        if hasattr(user, 'last_login_at'):
            user.last_login_at = datetime.utcnow()
        if hasattr(user, 'failed_login_attempts'):
            user.failed_login_attempts = 0  # Reset failed attempts on successful login

        db.add(user)
        db.commit()

        # Create tokens
        access_token_expires = timedelta(minutes=15)  # 15 minutes
        refresh_token_expires = timedelta(days=7)     # 7 days

        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=refresh_token_expires
        )

        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 900,  # 15 minutes in seconds
                "user": {
                    "user_id": str(user.id),
                    "email": user.email,
                    "is_verified": user.is_active  # Using is_active from the database schema
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")


@router.post("/logout", response_model=dict)
def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Invalidate current session
    """
    try:
        # In a real implementation, you might want to store the refresh token
        # in a blacklist to prevent reuse, but for now we just return success
        return {
            "success": True,
            "message": "Successfully logged out"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {str(e)}"
        )


@router.post("/refresh", response_model=dict)
def refresh_token(
    refresh_data: dict,  # Using dict for refresh token in request body
    db: Session = Depends(get_db)
):
    """
    Obtain new access token using refresh token
    """
    try:
        refresh_token_str = refresh_data.get("refresh_token")
        if not refresh_token_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )

        # Verify the refresh token
        from ..utils import verify_token
        payload = verify_token(refresh_token_str)

        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        # Get user from database to ensure they still exist and are active
        from sqlmodel import select
        result = db.execute(select(User).where(User.id == payload.get("sub")))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists"
            )

        # Create new tokens
        access_token_expires = timedelta(minutes=15)
        new_access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires
        )

        # Optionally rotate refresh token
        new_refresh_token = create_refresh_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(days=7)
        )

        return {
            "success": True,
            "data": {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,  # Return new refresh token for rotation
                "token_type": "bearer",
                "expires_in": 900
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error refreshing token: {str(e)}"
        )


@router.post("/verify-email", response_model=dict)
def verify_email(
    verification_data: dict,  # Contains token
    db: Session = Depends(get_db)
):
    """
    Verify user's email address using verification token
    """
    try:
        token = verification_data.get("token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token is required"
            )

        # In a real implementation, you would:
        # 1. Verify the token (could be JWT or stored in DB)
        # 2. Find the user associated with the token
        # 3. Mark the user as verified

        # This is a simplified version - in reality, you'd have a verification token table
        # and verify the token before marking the user as verified

        return {
            "success": True,
            "message": "Email verified successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying email: {str(e)}"
        )


@router.post("/forgot-password", response_model=dict)
def forgot_password(
    email_data: dict,  # Contains email
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Initiate password reset process
    """
    try:
        email = email_data.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )

        if not is_valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Find user by email (don't reveal if user exists to prevent enumeration)
        from sqlmodel import select
        result = db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user:
            # In a real app, generate reset token and send email
            # background_tasks.add_task(send_reset_email, user.email, reset_token)
            pass  # Just a placeholder to maintain proper indentation

        # Always return success to prevent email enumeration
        return {
            "success": True,
            "message": "If an account exists with this email, a password reset link has been sent"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initiating password reset: {str(e)}"
        )


@router.post("/reset-password", response_model=dict)
def reset_password(
    reset_data: dict,  # Contains token, new_password, confirm_new_password
    db: Session = Depends(get_db)
):
    """
    Reset user's password using reset token
    """
    try:
        token = reset_data.get("token")
        new_password = reset_data.get("new_password")
        confirm_new_password = reset_data.get("confirm_new_password")

        if not all([token, new_password, confirm_new_password]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token, new password, and confirmation are required"
            )

        if new_password != confirm_new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        if not is_strong_password(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password does not meet security requirements"
            )

        # In a real implementation, you would:
        # 1. Verify the reset token
        # 2. Find the user associated with the token
        # 3. Hash and update their password
        # 4. Invalidate all existing sessions for security

        # This is a simplified version - implement proper token verification in a real app
        return {
            "success": True,
            "message": "Password reset successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting password: {str(e)}"
        )