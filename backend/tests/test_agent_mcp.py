import pytest
from unittest.mock import AsyncMock, patch
from src.agent.runner import run_agent, execute_tool
from src.models.task import Task

@pytest.mark.asyncio
async def test_run_agent_with_valid_input():
    """Test that the agent can process valid input and return a response"""
    with patch('src.agent.runner.client') as mock_client:
        # Mock the API response
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "I've added the task for you."
        mock_response.choices[0].message.tool_calls = None

        mock_client.chat.completions.create.return_value = mock_response

        result = await run_agent(
            user_id="test_user_123",
            message_text="Add a task to buy groceries"
        )

        assert "response" in result
        assert "conversation_id" in result
        assert "tool_calls" in result


@pytest.mark.asyncio
async def test_execute_add_task_tool():
    """Test that the add_task tool works correctly"""
    with patch('src.mcp.handlers.AsyncSessionLocal') as mock_session:
        mock_session_instance = AsyncMock()
        mock_task_instance = AsyncMock()
        mock_task_instance.model_dump.return_value = {
            "id": 1,
            "user_id": "test_user_123",
            "title": "buy groceries",
            "description": None,
            "completed": False,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }

        mock_session_instance.__aenter__.return_value = mock_session_instance
        mock_session_instance.add = AsyncMock()
        mock_session_instance.commit = AsyncMock()
        mock_session_instance.refresh = AsyncMock()

        with patch('src.mcp.handlers.select') as mock_select:
            result = await execute_tool("add_task", {
                "user_id": "test_user_123",
                "title": "buy groceries"
            })

            assert result is not None
            assert result["title"] == "buy groceries"


@pytest.mark.asyncio
async def test_execute_unknown_tool():
    """Test that unknown tools return an error"""
    result = await execute_tool("unknown_tool", {})

    assert "error" in result
    assert "Unknown function: unknown_tool" in result["error"]


@pytest.mark.asyncio
async def test_execute_tool_with_invalid_args():
    """Test error handling when tool is called with invalid arguments"""
    # Test with a task that doesn't exist
    with patch('src.mcp.handlers.AsyncSessionLocal') as mock_session:
        mock_session_instance = AsyncMock()
        mock_session_instance.__aenter__.return_value = mock_session_instance
        mock_session_instance.exec = AsyncMock()
        mock_session_instance.exec.return_value.first.return_value = None  # No task found

        result = await execute_tool("complete_task", {
            "user_id": "test_user_123",
            "task_id": 999
        })

        assert "error" in result
        assert "not found" in result["error"].lower()