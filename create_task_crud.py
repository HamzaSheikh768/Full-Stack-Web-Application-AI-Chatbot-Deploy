"""
Script to create a task using the application's CRUD functions
"""
import asyncio
import sys
import os
from datetime import datetime
from sqlmodel import Session

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.database.db import get_async_session
from backend.src.models.task import Task
from backend.src.schemas import TaskCreate
from backend.src.crud.tasks import create_task


async def create_task_via_crud():
    # Create a new task using the CRUD function
    task_data = TaskCreate(
        title="New Task Created via CRUD Function",
        description="This is a new task created using the application's CRUD functions",
        priority="medium"
    )
    user_id = "test_user_123"
    
    # Get async session
    session_gen = get_async_session()
    session = await session_gen.__anext__()
    
    try:
        created_task = await create_task(session, task_data, user_id)
        print(f"Task created successfully with ID: {created_task.id}")
        print(f"Title: {created_task.title}")
        print(f"Description: {created_task.description}")
        print(f"User ID: {created_task.user_id}")
        print(f"Completed: {created_task.completed}")
        print(f"Priority: {created_task.priority}")
        return created_task
    except Exception as e:
        print(f"Error creating task via CRUD: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(create_task_via_crud())