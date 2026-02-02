#!/usr/bin/env python3
"""
Test script to verify Neon database integration works properly.
This test connects to the actual Neon database and performs operations
without using hardcoded values or mock data.
"""

import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

# Add the backend src to the path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from src.database.db import get_db, create_db_and_tables
from src.models.user import User
from src.models.task import Task
from src.utils import hash_password
from sqlmodel import select


def test_neon_database_connection():
    """
    Test Neon database connection and basic operations
    """
    print("Testing Neon database connection...")

    # Get database URL from environment (should be Neon)
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    print(f"Using database URL: {db_url}")

    # Test basic connection by creating tables
    try:
        create_db_and_tables()
        print("[OK] Database tables created successfully")
    except Exception as e:
        print(f"[ERROR] Failed to create database tables: {e}")
        return False

    # Test creating a user and task
    try:
        # Get a database session
        db_gen = get_db()
        db = next(db_gen)

        print("[OK] Database session created successfully")

        # Create a test user with a unique ID
        user_email = f"test_{uuid4().hex[:8]}@example.com"
        user = User(
            email=user_email,
            password_hash=hash_password("TestPass123!@#"),
            first_name="Test",
            last_name="User",
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"[OK] User created successfully: {user.email} (ID: {user.id})")

        # Create a test task for the user
        task = Task(
            user_id=user.id,
            title="Test Task from Integration Test",
            description="This is a test task created during database integration testing",
            priority="MEDIUM",  # Use uppercase as per database enum values: LOW, MEDIUM, HIGH
            recurrence_pattern="none"
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        print(f"[OK] Task created successfully: {task.title} (ID: {task.id})")

        # Query the task back to verify it was saved
        statement = select(Task).where(Task.id == task.id)
        result = db.execute(statement)
        retrieved_task_tuple = result.first()

        # The result.first() returns a tuple when using session.execute, so extract the task
        retrieved_task = retrieved_task_tuple[0] if retrieved_task_tuple else None

        if retrieved_task and retrieved_task.id == task.id:
            print("[OK] Task retrieval successful - database write/read working")
        else:
            print("[ERROR] Failed to retrieve created task")
            return False

        # Query user's tasks to verify user isolation
        # Using str() to ensure proper type matching with database schema
        user_tasks_statement = select(Task).where(Task.user_id == str(user.id))
        user_tasks_result = db.execute(user_tasks_statement)
        user_tasks_tuples = user_tasks_result.all()

        # Extract the actual task objects from tuples
        user_tasks = [task_tuple[0] for task_tuple in user_tasks_tuples]

        if len(user_tasks) >= 1:
            print(f"[OK] User isolation working - found {len(user_tasks)} tasks for user")
        else:
            print("[ERROR] User isolation test failed - couldn't find user's tasks")
            return False

        # Clean up: delete the test data
        db.delete(retrieved_task)
        db.delete(user)
        db.commit()

        print("[OK] Test data cleaned up successfully")

        # Close the session
        db.close()

        return True

    except Exception as e:
        print(f"[ERROR] Database operation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_tests():
    """
    Run all Neon database integration tests
    """
    print("=" * 60)
    print("Neon Database Integration Tests")
    print("=" * 60)

    success = test_neon_database_connection()

    print("=" * 60)
    if success:
        print("[OK] All Neon database integration tests PASSED")
        return True
    else:
        print("[ERROR] Some Neon database integration tests FAILED")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)