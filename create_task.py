"""
Script to create a task directly in the database
"""
import asyncio
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from backend.src.database.db import get_db
from backend.src.models.task import Task


def create_task_directly():
    # Create a new task directly in the database
    new_task = Task(
        id=str(uuid.uuid4()),
        user_id="test_user_123",
        title="New Task Created Directly",
        description="This is a new task created directly in the database",
        completed=False,
        priority="medium",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Get database session and add the task
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        print(f"Task created successfully with ID: {new_task.id}")
        print(f"Title: {new_task.title}")
        print(f"Description: {new_task.description}")
        print(f"User ID: {new_task.user_id}")
        return new_task
    except Exception as e:
        print(f"Error creating task: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_task_directly()