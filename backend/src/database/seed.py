"""
Database seed data for testing advanced todo features
"""

from datetime import datetime, timedelta, timezone
from typing import List
from sqlmodel import Session, select

from ..models.task import Task
from ..models.user import User
from ..database.db import SessionLocal


def create_test_users(session: Session) -> List[User]:
    """Create test users for development"""
    test_users = [
        User(
            id="test-user-1",
            email="alice@example.com",
            password_hash="$2b$12$dummy_hash_for_testing",
            is_active=True
        ),
        User(
            id="test-user-2",
            email="bob@example.com",
            password_hash="$2b$12$dummy_hash_for_testing",
            is_active=True
        )
    ]

    for user in test_users:
        # Check if user already exists
        existing = session.exec(select(User).where(User.email == user.email)).first()
        if not existing:
            session.add(user)

    session.commit()
    return test_users


def create_test_tasks(session: Session) -> List[Task]:
    """Create test tasks with various configurations"""

    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(days=1)
    next_week = now + timedelta(days=7)

    test_tasks = [
        # Basic tasks with priorities
        Task(
            user_id="test-user-1",
            title="High priority task",
            description="This is an urgent task that needs immediate attention",
            priority="HIGH",
            tags=["urgent", "work"],
            due_date=tomorrow,
            remind_at=now + timedelta(hours=12),
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Medium priority task",
            description="Regular task with medium priority",
            priority="MEDIUM",
            tags=["work", "planning"],
            due_date=next_week,
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Low priority task",
            description="This can wait",
            priority="LOW",
            tags=["personal", "someday"],
            completed=False
        ),

        # Recurring tasks
        Task(
            user_id="test-user-1",
            title="Daily standup meeting",
            description="Daily team sync at 9 AM",
            priority="MEDIUM",
            tags=["work", "meeting", "daily"],
            due_date=tomorrow.replace(hour=9, minute=0, second=0),
            remind_at=tomorrow.replace(hour=8, minute=45, second=0),
            is_recurring=True,
            recurrence_pattern={
                "type": "daily",
                "interval": 1,
                "end_date": (now + timedelta(days=90)).isoformat()
            },
            next_due_date=tomorrow.replace(hour=9, minute=0, second=0) + timedelta(days=1),
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Weekly team meeting",
            description="Every Friday at 2 PM",
            priority="HIGH",
            tags=["work", "meeting", "weekly"],
            due_date=now + timedelta(days=(4 - now.weekday()) % 7),  # Next Friday
            is_recurring=True,
            recurrence_pattern={
                "type": "weekly",
                "interval": 1,
                "days_of_week": ["friday"]
            },
            next_due_date=now + timedelta(days=(4 - now.weekday()) % 7 + 7),
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Monthly report",
            description="Submit monthly progress report",
            priority="HIGH",
            tags=["work", "report", "monthly"],
            due_date=now.replace(day=1) + timedelta(days=32),  # Next month
            is_recurring=True,
            recurrence_pattern={
                "type": "monthly",
                "interval": 1,
                "day_of_month": 1
            },
            completed=False
        ),

        # Tasks with various tag combinations
        Task(
            user_id="test-user-1",
            title="Buy groceries",
            description="Milk, eggs, bread, vegetables",
            priority="MEDIUM",
            tags=["personal", "shopping", "food"],
            due_date=tomorrow,
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Gym workout",
            description="Cardio and strength training",
            priority="LOW",
            tags=["personal", "health", "fitness"],
            completed=False
        ),
        Task(
            user_id="test-user-1",
            title="Code review",
            description="Review pull requests from team",
            priority="HIGH",
            tags=["work", "development", "review"],
            due_date=now + timedelta(hours=4),
            remind_at=now + timedelta(hours=2),
            completed=False
        ),

        # Completed tasks
        Task(
            user_id="test-user-1",
            title="Completed task",
            description="This task is already done",
            priority="MEDIUM",
            tags=["work", "done"],
            completed=True
        ),

        # Tasks for second user
        Task(
            user_id="test-user-2",
            title="Bob's task",
            description="Task for user isolation testing",
            priority="MEDIUM",
            tags=["test"],
            completed=False
        ),
    ]

    for task in test_tasks:
        session.add(task)

    session.commit()
    return test_tasks


def seed_database():
    """Main function to seed the database with test data"""
    print("Starting database seeding...")

    with SessionLocal() as session:
        # Create test users
        print("Creating test users...")
        users = create_test_users(session)
        print(f"Created {len(users)} test users")

        # Create test tasks
        print("Creating test tasks...")
        tasks = create_test_tasks(session)
        print(f"Created {len(tasks)} test tasks")

    print("Database seeding complete!")
    print("\nTest users:")
    print("  - alice@example.com (test-user-1)")
    print("  - bob@example.com (test-user-2)")
    print("\nYou can now test the application with these users and tasks.")


if __name__ == "__main__":
    seed_database()
