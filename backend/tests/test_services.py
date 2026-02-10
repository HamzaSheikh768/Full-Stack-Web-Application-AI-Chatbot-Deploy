import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from typing import List
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy import event

from ..models.task import Task, TaskPriority, RecurrenceEnum
from ..services.task_service import TaskService, TaskCreate, TaskUpdate, TaskResponse
from ..schemas import TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema


@pytest.fixture
def mock_session():
    """Create a mock database session for testing"""
    session = MagicMock(spec=Session)
    return session


@pytest.mark.asyncio
async def test_create_task_success(mock_session):
    """Test successful task creation"""
    # Arrange
    task_data = TaskCreateSchema(
        title="Test Task",
        description="Test Description",
        priority="medium",
        tags=["test", "important"],
        due_date=datetime.now() + timedelta(days=1)
    )
    user_id = "test_user_id"
    
    # Act
    with patch('backend.src.services.task_service.uuid.uuid4', return_value='mocked_uuid'):
        result = await TaskService.create_task(task_data, user_id, mock_session)
    
    # Assert
    assert result.title == "Test Task"
    assert result.description == "Test Description"
    assert result.priority == "medium"
    assert result.user_id == user_id
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_by_id_success(mock_session):
    """Test successful retrieval of a task by ID"""
    # Arrange
    task_id = "test_task_id"
    user_id = "test_user_id"
    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = mock_task
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.get_task_by_id(task_id, user_id, mock_session)
    
    # Assert
    assert result is not None
    assert result.id == task_id
    assert result.title == "Test Task"


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(mock_session):
    """Test retrieval of a non-existent task"""
    # Arrange
    task_id = "nonexistent_task_id"
    user_id = "test_user_id"
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.get_task_by_id(task_id, user_id, mock_session)
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_update_task_success(mock_session):
    """Test successful task update"""
    # Arrange
    task_id = "test_task_id"
    user_id = "test_user_id"
    update_data = TaskUpdateSchema(title="Updated Title", priority="high")
    
    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Original Title"
    mock_task.priority = "medium"
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = mock_task
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.update_task(task_id, update_data, user_id, mock_session)
    
    # Assert
    assert result is not None
    assert result.title == "Updated Title"
    assert result.priority == "high"
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_unauthorized(mock_session):
    """Test updating a task owned by another user (should fail)"""
    # Arrange
    task_id = "test_task_id"
    user_id = "different_user_id"  # Different from task owner
    update_data = TaskUpdateSchema(title="Updated Title")
    
    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.user_id = "original_owner_id"  # Different user
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = mock_task
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.update_task(task_id, update_data, user_id, mock_session)
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_delete_task_success(mock_session):
    """Test successful task deletion"""
    # Arrange
    task_id = "test_task_id"
    user_id = "test_user_id"
    
    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.user_id = user_id
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = mock_task
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.delete_task(task_id, user_id, mock_session)
    
    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_task)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_task_completion(mock_session):
    """Test toggling task completion status"""
    # Arrange
    task_id = "test_task_id"
    user_id = "test_user_id"
    
    mock_task = MagicMock(spec=Task)
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.completed = False  # Initially not completed
    
    mock_execute = AsyncMock()
    mock_execute.scalar_one_or_none.return_value = mock_task
    mock_session.execute.return_value = mock_execute
    
    # Act
    result = await TaskService.toggle_task_completion(task_id, user_id, mock_session)
    
    # Assert
    assert result is not None
    # Note: The actual toggle logic would happen in the service, 
    # but we're testing that the method executes without error
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_filtered_tasks(mock_session):
    """Test retrieving tasks with filters"""
    # Arrange
    user_id = "test_user_id"
    mock_task = MagicMock(spec=Task)
    mock_task.id = "test_task_id"
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    
    mock_execute = AsyncMock()
    mock_execute.scalars().all.return_value = [mock_task]
    mock_session.execute.return_value = mock_execute
    
    # Mock the count query separately
    count_execute = AsyncMock()
    count_execute.scalar_one.return_value = 1
    mock_session.execute = MagicMock(side_effect=[count_execute, mock_execute])
    
    # Act
    results, total_count = await TaskService.get_filtered_tasks(
        mock_session, 
        user_id,
        status="pending",
        priority="medium",
        search="Test"
    )
    
    # Assert
    assert len(results) == 1
    assert total_count == 1
    assert results[0].title == "Test Task"


@pytest.mark.asyncio
async def test_search_tasks(mock_session):
    """Test searching tasks by title or description"""
    # Arrange
    query = "test"
    mock_task = MagicMock(spec=Task)
    mock_task.id = "test_task_id"
    mock_task.title = "Test Task"
    mock_task.description = "This is a test task"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    
    mock_execute = AsyncMock()
    mock_execute.scalars().all.return_value = [mock_task]
    mock_session.execute.return_value = mock_execute
    
    # Act
    results = await TaskService.search_tasks(query, mock_session)
    
    # Assert
    assert len(results) == 1
    assert results[0].title == "Test Task"
    assert query.lower() in results[0].title.lower()