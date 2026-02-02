#!/usr/bin/env python3
"""Test script to debug user registration issues"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.database.db import get_async_session, AsyncSessionLocal, create_db_and_tables
from src.models.user import User
from src.auth import get_password_hash
from sqlmodel import select
import uuid

async def test_user_creation():
    print("Testing user creation...")

    # Create database tables
    await create_db_and_tables()

    async with AsyncSessionLocal() as session:
        try:
            # Check if test user already exists
            existing_user_result = await session.execute(select(User).where(User.email == "test@example.com"))
            existing_user = existing_user_result.first()

            if existing_user:
                print(f"User already exists: {existing_user}")
                # Let's try to delete the existing user first
                await session.delete(existing_user[0])  # Unpack the tuple
                await session.commit()
                print("Deleted existing user")

            # Create new user
            user_id = str(uuid.uuid4())
            hashed_password = get_password_hash("testpassword123")
            db_user = User(
                id=user_id,
                email="test@example.com",
                name="Test User",
                password_hash=hashed_password
            )

            print(f"About to add user: {db_user}")
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            print(f"User created successfully: {db_user}")

            # Verify the user was created
            verify_result = await session.execute(select(User).where(User.email == "test@example.com"))
            verify_user = verify_result.first()
            print(f"Verified user exists: {verify_user}")

        except Exception as e:
            print(f"Error occurred: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_user_creation())