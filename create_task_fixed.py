"""
Script to create a task directly in the database with correct schema
"""
import asyncio
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select
from backend.src.database.db import get_db
from backend.src.models.task import Task
import json


def create_task_directly():
    # First, let's inspect the actual database schema
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Try to create a task with minimal required fields
        new_task = Task(
            id=str(uuid.uuid4()),
            user_id="test_user_123",
            title="New Task Created Directly",
            description="This is a new task created directly in the database",
            completed=False,
            priority="MEDIUM",  # Using uppercase as per schema
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        print(f"Task created successfully with ID: {new_task.id}")
        print(f"Title: {new_task.title}")
        print(f"Description: {new_task.description}")
        print(f"User ID: {new_task.user_id}")
        print(f"Completed: {new_task.completed}")
        print(f"Priority: {new_task.priority}")
        return new_task
    except Exception as e:
        print(f"Error creating task: {e}")
        print("Attempting to create task with adjusted schema...")
        
        # If the above fails, let's try to create a raw SQL task
        try:
            from sqlalchemy import text
            
            task_id = str(uuid.uuid4())
            user_id = "test_user_123"
            title = "New Task Created via Raw SQL"
            description = "This is a new task created via raw SQL query"
            
            sql = text("""
                INSERT INTO task (id, user_id, title, description, is_completed, priority, created_at, updated_at)
                VALUES (:id, :user_id, :title, :description, :is_completed, :priority, :created_at, :updated_at)
            """)
            
            db.execute(sql, {
                "id": task_id,
                "user_id": user_id,
                "title": title,
                "description": description,
                "is_completed": False,
                "priority": "MEDIUM",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            db.commit()
            print(f"Task created successfully with ID: {task_id}")
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"User ID: {user_id}")
            
        except Exception as e2:
            print(f"Also failed with raw SQL: {e2}")
            db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_task_directly()