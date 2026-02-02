#!/usr/bin/env python3
"""Debug script to test the registration function directly"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.api.auth_routes import register_user
from src.auth import UserRegister
from src.database.db import AsyncSessionLocal

async def test_direct_registration():
    print("Testing direct registration call...")

    # Create test user data
    user_data = UserRegister(
        email="debug_test@example.com",
        password="testpassword123",
        name="Debug Test User"
    )

    # Create a session manually
    async with AsyncSessionLocal() as session:
        try:
            print("Calling register_user function...")
            result = await register_user(user_data, session)
            print(f"Registration successful: {result}")
        except Exception as e:
            print(f"Error during registration: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_registration())