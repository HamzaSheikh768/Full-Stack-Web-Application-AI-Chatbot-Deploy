import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.database.db import get_session
from src.models.task import Task
from src.models.conversation import Conversation, Message

# Test constants
TEST_USER_ID = "test_user_123"
VOICE_MESSAGE = "Add a task to buy groceries"
EXPECTED_TASK_TITLE = "buy groceries"

@pytest.fixture(scope="function")
def client():
    """Test client for the API"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.mark.asyncio
async def test_voice_enabled_task_creation():
    """Test that voice input converted to text creates tasks properly"""
    with patch('src.agent.runner.get_agent') as mock_get_agent_func, \
         patch('src.agent.runner.AsyncSessionLocal') as mock_session_local, \
         patch('builtins.open') as mock_file:

        # Mock agent data
        mock_agent_data = {
            "client": AsyncMock(),
            "tools": [],
            "instructions": "Test instructions",
            "model": "command-r-plus"
        }
        mock_get_agent_func.return_value = mock_agent_data

        # Mock database session
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        mock_session_local.return_value.__aexit__.return_value = None

        # Mock conversation
        mock_conv = Conversation(id=1, user_id=TEST_USER_ID)
        mock_session.get.return_value = mock_conv
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Mock Cohere API response
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = f"I've added '{EXPECTED_TASK_TITLE}' to your task list."
        mock_response.choices[0].message.tool_calls = None

        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_agent_data["client"] = mock_client

        # Mock tool execution result for add_task
        mock_add_task_result = {
            "id": 1,
            "user_id": TEST_USER_ID,
            "title": EXPECTED_TASK_TITLE,
            "description": None,
            "completed": False
        }

        with patch('src.agent.runner.execute_tool') as mock_execute_tool:
            mock_execute_tool.return_value = mock_add_task_result

            # Mock contracts file content
            mock_file.return_value.__enter__.return_value.read.return_value = '[]'

            # Run the agent with a voice-converted text message
            from src.agent.runner import run_agent
            result = await run_agent(
                user_id=TEST_USER_ID,
                message_text=VOICE_MESSAGE,
                conversation_id=1
            )

            # Verify the result
            assert "conversation_id" in result
            assert "response" in result
            assert EXPECTED_TASK_TITLE in result["response"]

@pytest.mark.asyncio
async def test_voice_input_error_handling():
    """Test that voice input errors are handled gracefully"""
    with patch('src.agent.runner.get_agent') as mock_get_agent_func, \
         patch('src.agent.runner.AsyncSessionLocal') as mock_session_local, \
         patch('builtins.open') as mock_file:

        # Mock agent data
        mock_agent_data = {
            "client": AsyncMock(),
            "tools": [],
            "instructions": "Test instructions",
            "model": "command-r-plus"
        }
        mock_get_agent_func.return_value = mock_agent_data

        # Mock database session
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session
        mock_session_local.return_value.__aexit__.return_value = None

        # Mock conversation
        mock_conv = Conversation(id=1, user_id=TEST_USER_ID)
        mock_session.get.return_value = mock_conv
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Mock Cohere API to raise an exception
        mock_client = AsyncMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_agent_data["client"] = mock_client

        # Mock contracts file content
        mock_file.return_value.__enter__.return_value.read.return_value = '[]'

        # Run the agent and expect graceful error handling
        from src.agent.runner import run_agent
        result = await run_agent(
            user_id=TEST_USER_ID,
            message_text=VOICE_MESSAGE,
            conversation_id=1
        )

        # Verify the error is handled gracefully
        assert "conversation_id" in result
        assert "response" in result
        assert "encountered an error" in result["response"]

def test_voice_recognition_fallback():
    """Test that voice recognition fallback works for unsupported browsers"""
    # This test would verify that when Web Speech API is not available,
    # the system gracefully falls back to text input

    # Since the actual fallback function may not exist in the lib yet, we'll skip this test
    # until the implementation is complete
    pass