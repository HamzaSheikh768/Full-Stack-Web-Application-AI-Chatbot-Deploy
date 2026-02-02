#!/usr/bin/env python3
"""
Test script to verify database connection and test users exist
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import sys
import pathlib

# Add the src directory to the path
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

from models.user import User


async def test_db_connection():
    """Test the database connection and verify test users exist"""
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./taskapp_dev.db")
    print(f"Using database URL: {database_url}")

    # Create engine
    engine = create_async_engine(database_url)

    async with AsyncSession(engine) as session:
        # Query all users
        result = await session.execute(select(User))
        users = result.all()

        print(f"Connected to database successfully. Found {len(users)} users in total.")

        # Find test users specifically
        test_emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
        test_users = [u for u in users if u.email in test_emails]

        print(f"Found {len(test_users)} test users:")
        for user in test_users:
            print(f"  - {user.email} (ID: {user.id[:8]}...)")

        # Verify all 3 test users exist
        found_emails = [u.email for u in test_users]
        missing_users = [email for email in test_emails if email not in found_emails]

        if missing_users:
            print(f"Missing test users: {missing_users}")
            return False
        else:
            print("✓ All 3 test users found in database!")
            return True


if __name__ == "__main__":
    success = asyncio.run(test_db_connection())
    if success:
        print("\n✓ Database connection and test users verification: PASSED")
    else:
        print("\n✗ Database connection or test users verification: FAILED")
        sys.exit(1)