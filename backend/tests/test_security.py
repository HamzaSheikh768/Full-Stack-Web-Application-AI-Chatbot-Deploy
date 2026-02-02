import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, select
from unittest.mock import patch, AsyncMock

from src.main import app
from src.database.db import get_session
from src.models.task import Task
from src.models.conversation import Conversation, Message

# Create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def client(test_db):
    def get_test_session():
        yield test_db

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

async def mock_get_current_user_from_better_auth():
    """Mock authenticated user for testing"""
    from src.models.user import User

    return User(
        id="test_user_123",
        email="test@example.com",
        name="Test User"
    )

def test_user_isolation_in_task_operations(client, test_db):
    """Test that User A cannot access User B's tasks"""
    from src.mcp.handlers import add_task, list_tasks, complete_task, delete_task, update_task

    # Create tasks for different users in the test database
    user_a_task = Task(
        user_id="user_a_123",
        title="User A's task",
        description="This belongs to User A",
        completed=False
    )
    user_b_task = Task(
        user_id="user_b_456",  # Different user
        title="User B's task",
        description="This belongs to User B",
        completed=False
    )

    test_db.add(user_a_task)
    test_db.add(user_b_task)
    test_db.commit()
    test_db.refresh(user_a_task)
    test_db.refresh(user_b_task)

    # Test that User A cannot access User B's task when trying to complete it
    result = complete_task("user_a_123", user_b_task.id)  # User A trying to complete User B's task

    # The function should return an error since the task doesn't belong to the user
    assert "error" in result
    assert "not found for your account" in result["error"]

    # Test that User A cannot access User B's task when trying to delete it
    result = delete_task("user_a_123", user_b_task.id)  # User A trying to delete User B's task

    # The function should return an error since the task doesn't belong to the user
    assert "error" in result
    assert "not found for your account" in result["error"]

    # Test that User A cannot access User B's task when trying to update it
    result = update_task("user_a_123", user_b_task.id, title="New title")

    # The function should return an error since the task doesn't belong to the user
    assert "error" in result
    assert "not found for your account" in result["error"]

    # Test that User A only sees their own tasks when listing
    user_a_tasks = list_tasks("user_a_123")
    user_a_task_ids = [task["id"] for task in user_a_tasks if "id" in task and isinstance(task, dict)]

    # User A should only see their own task, not User B's task
    assert user_a_task.id in user_a_task_ids
    assert user_b_task.id not in user_a_task_ids

    # Test that User B only sees their own tasks when listing
    user_b_tasks = list_tasks("user_b_456")
    user_b_task_ids = [task["id"] for task in user_b_tasks if "id" in task and isinstance(task, dict)]

    # User B should only see their own task, not User A's task
    assert user_b_task.id in user_b_task_ids
    assert user_a_task.id not in user_b_task_ids

def test_user_isolation_in_conversation_operations(client, test_db):
    """Test that User A cannot access User B's conversations"""
    from src.services.chat_service import get_conversation_history

    # Create conversations for different users in the test database
    user_a_conv = Conversation(
        user_id="user_a_123",
        title="User A's conversation"
    )
    user_b_conv = Conversation(
        user_id="user_b_456",  # Different user
        title="User B's conversation"
    )

    test_db.add(user_a_conv)
    test_db.add(user_b_conv)
    test_db.commit()
    test_db.refresh(user_a_conv)
    test_db.refresh(user_b_conv)

    # Create messages for each conversation
    user_a_msg = Message(
        conversation_id=user_a_conv.id,
        user_id="user_a_123",
        role="user",
        content="User A message"
    )
    user_b_msg = Message(
        conversation_id=user_b_conv.id,
        user_id="user_b_456",
        role="user",
        content="User B message"
    )

    test_db.add(user_a_msg)
    test_db.add(user_b_msg)
    test_db.commit()

    # Test that User A cannot access User B's conversation history
    history_result = get_conversation_history(user_b_conv.id, "user_a_123")  # User A trying to access User B's conversation

    # The function should return an empty history since the conversation doesn't belong to the user
    assert history_result == []

    # Test that User B cannot access User A's conversation history
    history_result = get_conversation_history(user_a_conv.id, "user_b_456")  # User B trying to access User A's conversation

    # The function should return an empty history since the conversation doesn't belong to the user
    assert history_result == []

    # Test that User A can access their own conversation history
    history_result = get_conversation_history(user_a_conv.id, "user_a_123")

    # The function should return the correct history for User A's conversation
    assert len(history_result) > 0
    assert any(msg["content"] == "User A message" for msg in history_result)

    # Test that User B can access their own conversation history
    history_result = get_conversation_history(user_b_conv.id, "user_b_456")

    # The function should return the correct history for User B's conversation
    assert len(history_result) > 0
    assert any(msg["content"] == "User B message" for msg in history_result)

def test_chat_endpoint_user_id_validation(client, test_db):
    """Test that the chat endpoint validates user_id matches authenticated user"""

    # Mock the auth dependency to return a specific user
    with patch('src.api.chat_routes.get_current_user_from_better_auth', return_value=mock_get_current_user_from_better_auth()):
        # Try to access chat endpoint with different user_id than authenticated user
        response = client.post("/api/user_b_456/chat", json={
            "message": "Test message"
        })

        # Should return 403 Forbidden because user_id in URL doesn't match authenticated user
        assert response.status_code == 403
        assert "User ID mismatch" in response.json()["detail"]

        # Try to access chat endpoint with matching user_id
        response = client.post("/api/test_user_123/chat", json={
            "message": "Test message"
        })

        # Should not return 403 (could return 200, 500, etc. depending on other factors)
        assert response.status_code != 403

@pytest.mark.asyncio
async def test_secure_tool_execution_with_mocked_agent():
    """Test that tools properly isolate user data when executed by agent"""
    # This test mocks the agent execution to verify tools work with proper user isolation

    with patch('src.mcp.handlers.AsyncSessionLocal') as mock_session_local:
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        mock_session_local.return_value.__aexit__.return_value = None

        # Mock task retrieval
        mock_task = AsyncMock()
        mock_task.id = 1
        mock_task.user_id = "user_a_123"
        mock_task.title = "Test task"
        mock_task.description = "Test description"
        mock_task.completed = False

        # Configure mock to return task only when user_id matches
        async def mock_exec(query):
            mock_result = AsyncMock()
            if "user_a_123" in str(query) and "1" in str(query):
                mock_result.first.return_value = mock_task
            else:
                mock_result.first.return_value = None
            return mock_result

        mock_session.exec = mock_exec
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        from src.mcp.handlers import complete_task, delete_task, update_task

        # Test successful operation when user_id matches
        result = await complete_task("user_a_123", 1)
        assert "error" not in result  # Should succeed

        # Test failed operation when user_id doesn't match
        # (In a real scenario, this would be caught by the DB query filter)
        result = await complete_task("user_b_456", 1)  # Wrong user trying to access task
        assert "error" in result  # Should fail with error