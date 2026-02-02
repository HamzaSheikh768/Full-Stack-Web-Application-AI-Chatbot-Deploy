#!/usr/bin/env python3
"""
Simple script to recreate database tables to match the current model
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

async def update_database_schema():
    """Update database schema to match current models"""
    try:
        print("Updating database schema to match current models...")

        # Import the database setup
        from backend.src.database.db import async_engine
        from sqlmodel import SQLModel

        # Import models to register them with SQLModel metadata
        from backend.src.models.user import User
        from backend.src.models.task import Task

        # Create tables
        async with async_engine.begin() as conn:
            # Drop all tables first (be careful!)
            await conn.run_sync(SQLModel.metadata.drop_all)
            # Create all tables according to current models
            await conn.run_sync(SQLModel.metadata.create_all)

        print("Database tables recreated successfully!")

        # Test connection
        async with async_engine.begin() as conn:
            # Try to count users
            from sqlalchemy import text
            result = await conn.execute(text("SELECT COUNT(*) FROM user"))
            count = result.scalar()
            print(f"Connected to database, users table exists with {count} users")

            # Check if name column exists
            try:
                result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='name'"))
                columns = result.fetchall()
                if columns:
                    print("'name' column exists in user table")
                else:
                    print("'name' column missing from user table")
            except Exception as e:
                print(f"Could not check columns: {e}")

        return True

    except Exception as e:
        print(f"Error updating database schema: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Recreating database tables to match current models...")

    success = asyncio.run(update_database_schema())

    if success:
        print("\nDatabase schema updated successfully!")
        print("Now the signup functionality should work correctly.")
    else:
        print("\nFailed to update database schema.")
        sys.exit(1)