#!/usr/bin/env python3
"""
Script to create 3 test users in the database for authentication testing
"""
import asyncio
import uuid
import sys
import os
from datetime import datetime

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import after adding to path
from sqlmodel import SQLModel, select
from sqlalchemy import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# Import modules from the src directory
from src.models.user import User, UserRole
from src.utils import hash_password

# Import database engine directly from db module
from src.database.db import AsyncSessionLocal


async def create_test_users():
    """
    Create 3 test users in the database with specified credentials
    """
    print("Creating test users...")

    # Define test users
    test_users = [
        {
            "email": "user1@example.com",
            "password": "SecurePass123!",
            "role": UserRole.admin
        },
        {
            "email": "user2@example.com",
            "password": "SecurePass123!",
            "role": UserRole.user
        },
        {
            "email": "user3@example.com",
            "password": "SecurePass123!",
            "role": UserRole.guest
        }
    ]

    async with AsyncSessionLocal() as session:
        for user_data in test_users:
            # Check if user already exists
            existing_user = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = existing_user.first()

            if existing_user:
                print(f"User {user_data['email']} already exists, skipping...")
                continue

            # Create new user
            user = User(
                id=str(uuid.uuid4()),
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                role=user_data["role"],
                is_verified=True,  # Set to verified for immediate access
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                last_login_at=None,
                failed_login_attempts=0,
                locked_until=None
            )

            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"Created user: {user.email} with role {user.role.value}")

        print("Test users created successfully!")


if __name__ == "__main__":
    asyncio.run(create_test_users())