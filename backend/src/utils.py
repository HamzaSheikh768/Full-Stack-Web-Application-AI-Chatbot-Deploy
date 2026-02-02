from datetime import datetime, timedelta
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from pytz import utc
import bcrypt

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def calculate_next_occurrence(due_date: datetime, recurrence_pattern: str) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the recurrence pattern

    Args:
        due_date: Original due date
        recurrence_pattern: 'none', 'daily', or 'weekly'

    Returns:
        New datetime for next occurrence or None if no recurrence
    """
    if recurrence_pattern == "none":
        return None
    elif recurrence_pattern == "daily":
        return due_date + timedelta(days=1)
    elif recurrence_pattern == "weekly":
        return due_date + timedelta(days=7)
    else:
        # Unknown recurrence pattern, return None
        return None


def get_next_occurrence_from_now(recurrence_pattern: str) -> Optional[datetime]:
    """
    Calculate the next occurrence date from the current time based on the recurrence pattern

    Args:
        recurrence_pattern: 'none', 'daily', or 'weekly'

    Returns:
        New datetime for next occurrence or None if no recurrence
    """
    if recurrence_pattern == "none":
        return None
    elif recurrence_pattern == "daily":
        return datetime.now() + timedelta(days=1)
    elif recurrence_pattern == "weekly":
        return datetime.now() + timedelta(days=7)
    else:
        # Unknown recurrence pattern, return None
        return None


def normalize_timezone(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Normalize a datetime to UTC timezone if it has timezone info
    If the datetime is naive (no timezone), assume it's UTC

    Args:
        dt: Datetime to normalize

    Returns:
        Normalized datetime in UTC
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # Naive datetime, assume UTC
        return dt.replace(tzinfo=utc)
    else:
        # Convert to UTC
        return dt.astimezone(utc)


def is_valid_recurrence_pattern(pattern: str) -> bool:
    """
    Check if the recurrence pattern is valid

    Args:
        pattern: Recurrence pattern to validate

    Returns:
        True if valid, False otherwise
    """
    return pattern in ["none", "daily", "weekly"]


def create_recurring_task_data(original_task_data: dict) -> dict:
    """
    Create data for a new recurring task instance based on the original task

    Args:
        original_task_data: Data of the original task that is recurring

    Returns:
        New task data with updated fields for the next occurrence
    """
    # Copy the original data
    new_task_data = original_task_data.copy()

    # Update the relevant fields for the new occurrence
    new_task_data['completed'] = False  # New tasks are not completed

    # Calculate and update due date based on recurrence
    if new_task_data.get('due_date') and new_task_data.get('recurrence'):
        new_due_date = calculate_next_occurrence(new_task_data['due_date'], new_task_data['recurrence'])
        if new_due_date:
            new_task_data['due_date'] = new_due_date

    # Remove the ID to generate a new one
    new_task_data.pop('id', None)

    # Update timestamps
    now = datetime.now()
    new_task_data['created_at'] = now
    new_task_data['updated_at'] = now

    return new_task_data


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with a salt

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to compare against

    Returns:
        True if passwords match, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# JWT Utilities
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional, Dict, Any


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the specified data and expiration

    Args:
        data: Data to encode in the token (typically user info)
        expires_delta: Optional timedelta for token expiration (defaults to 15 minutes)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    # Set default expiration to 15 minutes if not provided
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)

    # Set expiration time
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    # Get secret key from environment - ensure consistency with Better Auth
    secret_key = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY") or "fallback-secret-key-for-development"

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token with the specified data and expiration

    Args:
        data: Data to encode in the token (typically user info)
        expires_delta: Optional timedelta for token expiration (defaults to 7 days)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    # Set default expiration to 7 days if not provided
    if expires_delta is None:
        expires_delta = timedelta(days=7)

    # Set expiration time
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    # Add a 'type' claim to distinguish refresh tokens
    to_encode.update({"type": "refresh"})

    # Get secret key from environment - ensure consistency with Better Auth
    secret_key = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY") or "fallback-secret-key-for-development"

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return its payload if valid

    Args:
        token: JWT token string to verify

    Returns:
        Token payload dictionary if valid, None if invalid/expired
    """
    try:
        # Get secret key from environment - ensure consistency with Better Auth
        secret_key = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY") or "fallback-secret-key-for-development"

        # Decode the token
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None


import re


def is_valid_email(email: str) -> bool:
    """
    Validate email address format according to RFC 5322 standards

    Args:
        email: Email address string to validate

    Returns:
        True if email format is valid, False otherwise
    """
    # RFC 5322 compliant email regex pattern
    # This is a simplified version that covers most common cases
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        # Additional checks for length limits
        if len(email) > 254:  # RFC 5321 limit for email addresses
            return False

        # Split email into local and domain parts
        local_part, domain_part = email.rsplit('@', 1)

        # Check local part length (RFC 5321 limit)
        if len(local_part) > 64:
            return False

        return True

    return False


def is_strong_password(password: str) -> bool:
    """
    Validate password strength following security requirements:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character

    Args:
        password: Password string to validate

    Returns:
        True if password meets strength requirements, False otherwise
    """
    # Check minimum length
    if len(password) < 12:
        return False

    # Check for at least one uppercase letter
    has_upper = any(c.isupper() for c in password)
    if not has_upper:
        return False

    # Check for at least one lowercase letter
    has_lower = any(c.islower() for c in password)
    if not has_lower:
        return False

    # Check for at least one digit
    has_digit = any(c.isdigit() for c in password)
    if not has_digit:
        return False

    # Check for at least one special character
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    has_special = any(c in special_chars for c in password)
    if not has_special:
        return False

    # All checks passed
    return True