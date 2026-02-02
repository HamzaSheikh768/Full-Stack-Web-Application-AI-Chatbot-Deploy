#!/usr/bin/env python3
"""Direct test of the signup functionality to identify the error"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.api.auth_routes import signup
from src.schemas import UserCreate
from src.database.db import get_db
from sqlalchemy.orm import Session

def test_signup_directly():
    """Test the signup function directly to see the actual error"""
    print("Testing signup function directly...")

    # Create a test user data
    user_data = UserCreate(
        email="test@example.com",
        password="TestPass123!@#",
        first_name="Test",
        last_name="User"
    )

    # Get a database session
    try:
        with get_db() as db:
            print("Got database session, calling signup function...")

            # Call signup function directly
            result = signup(user_data, None, db)
            print(f"Signup result: {result}")

    except Exception as e:
        print(f"Error during signup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_signup_directly()