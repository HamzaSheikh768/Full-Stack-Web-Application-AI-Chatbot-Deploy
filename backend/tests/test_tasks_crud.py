"""
Unit tests for task CRUD operations
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlmodel import Session, SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from datetime import datetime
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crud.tasks import (
    get_tasks_by_user_id,
    get_task_by_id_and_user,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from src.models.task import Task
from src.schemas import TaskCreate, TaskUpdate


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
        session.rollback()
    SQLModel.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_create_task(db_session):
    """Test creating a task"""
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        priority="medium"
    )
    user_id = "test_user_123"
    
    created_task = await create_task(db_session, task_data, user_id)
    
    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.user_id == user_id
    assert created_task.status == "pending"  # Default status
    assert created_task.priority == "medium"


@pytest.mark.asyncio
async def test_get_task_by_id_and_user(db_session):
    """Test retrieving a specific task"""
    # First create a task
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        priority="medium"
    )
    user_id = "test_user_123"
    
    created_task = await create_task(db_session, task_data, user_id)
    task_id = created_task.id
    
    # Now retrieve the task
    retrieved_task = await get_task_by_id_and_user(db_session, task_id, user_id)
    
    assert retrieved_task.id == task_id
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.user_id == user_id


@pytest.mark.asyncio
async def test_get_tasks_by_user_id(db_session):
    """Test retrieving all tasks for a user"""
    user_id = "test_user_123"
    
    # Create multiple tasks for the user
    task_data1 = TaskCreate(title="Task 1", description="First task", priority="high")
    task_data2 = TaskCreate(title="Task 2", description="Second task", priority="low")
    
    await create_task(db_session, task_data1, user_id)
    await create_task(db_session, task_data2, user_id)
    
    # Also create a task for a different user
    other_user_id = "other_user_456"
    task_data3 = TaskCreate(title="Other User Task", description="Task for other user", priority="medium")
    await create_task(db_session, task_data3, other_user_id)
    
    # Retrieve tasks for the first user
    user_tasks = await get_tasks_by_user_id(db_session, user_id)
    
    assert len(user_tasks) == 2
    assert all(task.user_id == user_id for task in user_tasks)
    assert any(task.title == "Task 1" for task in user_tasks)
    assert any(task.title == "Task 2" for task in user_tasks)
    
    # Verify the other user's task is not included
    assert all(task.title != "Other User Task" for task in user_tasks)


@pytest.mark.asyncio
async def test_update_task(db_session):
    """Test updating a task"""
    # First create a task
    task_data = TaskCreate(title="Original Task", description="Original description", priority="low")
    user_id = "test_user_123"
    
    created_task = await create_task(db_session, task_data, user_id)
    task_id = created_task.id
    
    # Update the task
    update_data = TaskUpdate(title="Updated Task", priority="high", description="Updated description")
    updated_task = await update_task(db_session, task_id, user_id, update_data)
    
    assert updated_task.id == task_id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated description"
    assert updated_task.priority == "high"


@pytest.mark.asyncio
async def test_delete_task(db_session):
    """Test deleting a task"""
    # First create a task
    task_data = TaskCreate(title="Task to Delete", description="This task will be deleted", priority="medium")
    user_id = "test_user_123"
    
    created_task = await create_task(db_session, task_data, user_id)
    task_id = created_task.id
    
    # Verify the task exists
    retrieved_task = await get_task_by_id_and_user(db_session, task_id, user_id)
    assert retrieved_task is not None
    
    # Delete the task
    result = await delete_task(db_session, task_id, user_id)
    assert result is True
    
    # Verify the task no longer exists
    with pytest.raises(Exception):  # Assuming TaskNotFoundException is raised
        await get_task_by_id_and_user(db_session, task_id, user_id)


@pytest.mark.asyncio
async def test_toggle_task_completion(db_session):
    """Test toggling task completion status"""
    # First create a task
    task_data = TaskCreate(title="Task to Toggle", description="This task will be toggled", priority="medium")
    user_id = "test_user_123"
    
    created_task = await create_task(db_session, task_data, user_id)
    task_id = created_task.id
    
    # Verify initial status is pending
    retrieved_task = await get_task_by_id_and_user(db_session, task_id, user_id)
    assert retrieved_task.status == "pending"
    
    # Toggle to completed
    toggled_task, new_task_instance = await toggle_task_completion(db_session, task_id, user_id, "completed")
    assert toggled_task.status == "completed"
    
    # Toggle back to pending
    toggled_task, new_task_instance = await toggle_task_completion(db_session, task_id, user_id, "pending")
    assert toggled_task.status == "pending"