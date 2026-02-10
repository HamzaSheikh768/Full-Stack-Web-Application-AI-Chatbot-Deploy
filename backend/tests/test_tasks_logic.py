"""
Simple tests for task functionality without database schema creation
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
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


@pytest.mark.asyncio
async def test_create_task_logic():
    """Test the create_task function logic"""
    # Mock the session and task data
    mock_session = AsyncMock()
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        priority="medium"
    )
    user_id = "test_user_123"
    
    # Mock the task object that gets created
    mock_task = MagicMock()
    mock_task.id = "task_123"
    mock_task.title = "Test Task"
    mock_task.description = "This is a test task"
    mock_task.user_id = user_id
    mock_task.status = "pending"
    mock_task.priority = "medium"
    
    # Patch the Task constructor to return our mock
    with patch('src.crud.tasks.Task') as mock_task_class:
        mock_task_class.return_value = mock_task
        
        # Call the function
        result = await create_task(mock_session, task_data, user_id)
        
        # Assertions
        assert result == mock_task
        mock_session.add.assert_called_once_with(mock_task)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_task)


@pytest.mark.asyncio
async def test_get_task_by_id_and_user_logic():
    """Test the get_task_by_id_and_user function logic"""
    mock_session = AsyncMock()
    task_id = "task_123"
    user_id = "test_user_123"
    
    # Mock the task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    
    # Mock the result scalar
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    
    # Mock the session.execute method to return an awaitable that resolves to mock_result
    mock_execute = AsyncMock(return_value=mock_result)
    mock_session.execute = mock_execute
    
    # Call the function
    result = await get_task_by_id_and_user(mock_session, task_id, user_id)
    
    # Assertions
    assert result == mock_task
    mock_execute.assert_called_once()
    

@pytest.mark.asyncio
async def test_update_task_logic():
    """Test the update_task function logic"""
    mock_session = AsyncMock()
    task_id = "task_123"
    user_id = "test_user_123"
    
    # Mock the task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Original Task"
    mock_task.priority = "medium"
    mock_task.updated_at = datetime.utcnow()
    
    # Mock the result scalar
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    
    # Mock the session.execute method to return an awaitable that resolves to mock_result
    mock_execute = AsyncMock(return_value=mock_result)
    mock_session.execute = mock_execute
    
    # Create update data
    task_update = TaskUpdate(title="Updated Task", priority="high")
    
    # Call the function
    result = await update_task(mock_session, task_id, user_id, task_update)
    
    # Assertions
    assert result == mock_task
    assert mock_task.title == "Updated Task"
    assert mock_task.priority == "HIGH"  # TaskUpdate schema converts to uppercase
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_task)


@pytest.mark.asyncio
async def test_delete_task_logic():
    """Test the delete_task function logic"""
    mock_session = AsyncMock()
    task_id = "task_123"
    user_id = "test_user_123"
    
    # Mock the task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Task to Delete"
    
    # Mock the result scalar
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    
    # Mock the session.execute method to return an awaitable that resolves to mock_result
    mock_execute = AsyncMock(return_value=mock_result)
    mock_session.execute = mock_execute
    
    # Call the function
    result = await delete_task(mock_session, task_id, user_id)
    
    # Assertions
    assert result is True
    mock_session.delete.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_task_completion_logic():
    """Test the toggle_task_completion function logic"""
    mock_session = AsyncMock()
    task_id = "task_123"
    user_id = "test_user_123"
    
    # Mock the task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Task to Toggle"
    mock_task.status = "pending"
    mock_task.recurrence_pattern = "none"  # Prevent recurring task logic
    mock_task.updated_at = datetime.utcnow()
    
    # Mock the result scalar
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_task
    
    # Mock the session.execute method to return an awaitable that resolves to mock_result
    mock_execute = AsyncMock(return_value=mock_result)
    mock_session.execute = mock_execute
    
    # Call the function to toggle to completed
    result, new_task_instance = await toggle_task_completion(mock_session, task_id, user_id, "completed")
    
    # Assertions
    assert result == mock_task
    assert mock_task.status == "completed"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_task)