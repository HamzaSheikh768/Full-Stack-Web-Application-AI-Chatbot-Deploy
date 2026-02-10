import os
import inspect
from functools import wraps
from typing import List, Callable, Dict, Any
import cohere  # Use native Cohere client

from ..config import get_settings
from ..mcp.tools import all_tools

settings = get_settings()

# Use native Cohere client for better compatibility with Cohere's actual API
co = cohere.Client(api_key=settings.COHERE_API_KEY)

def bind_tools_to_user(tools: List[Callable], user_id: str) -> List[Callable]:
    """
    Wraps tools to inject user_id automatically, hiding it from the LLM.
    This ensures User A cannot manipulate tools to access User B's data.
    """
    bound_tools = []

    for tool in tools:
        @wraps(tool)
        def wrapper(*args, **kwargs):
            # Inject user_id into the actual call
            return tool(user_id=user_id, *args, **kwargs)

        # Remove user_id from the signature exposed to the LLM
        sig = inspect.signature(tool)
        new_params = [
            p for name, p in sig.parameters.items()
            if name != 'user_id'
        ]
        wrapper.__signature__ = sig.replace(parameters=new_params)
        bound_tools.append(wrapper)

    return bound_tools

def get_agent(user_id: str) -> Dict[str, Any]:
    """Returns the client and tools for use by the runner"""
    user_tools = bind_tools_to_user(all_tools, user_id)

    # We need to return the actual callable tools for the execute_tool function to use,
    # but also need to ensure the function signatures are properly formatted for the LLM
    # The tool definitions are loaded from contracts file in the runner

    instructions = """You are a helpful and friendly Todo Assistant with advanced task management capabilities.
    You organize tasks for the user with care and attention.

    ALWAYS use the provided tools to manage tasks.

    **Task Creation Commands:**
    - Recognize commands like 'create task', 'add task', 'make task', 'remember to', 'need to', 'buy', 'get', etc.
    - Support priority levels: high, medium, low (e.g., "add a high priority task")
    - Support tags/categories (e.g., "add task with tags work and urgent")
    - Support due dates (e.g., "add task due tomorrow", "due next Friday")
    - Support reminders (e.g., "remind me 1 hour before")
    - Support recurring tasks (e.g., "create daily task", "weekly meeting every Monday")

    **Task Listing Commands:**
    - Show all, pending, or completed tasks
    - Filter by priority (e.g., "show high priority tasks")
    - Filter by tags (e.g., "show work tasks")
    - Search by keyword (e.g., "find tasks about meeting")
    - Sort by due date, priority, or title

    **Task Management:**
    - Complete, delete, or update tasks
    - Recognize task IDs in user messages
    - Handle recurring task patterns (daily, weekly, monthly)

    **Important Guidelines:**
    - NEVER hallucinate task IDs or content
    - If a tool returns an error, apologize nicely and suggest alternatives
    - Always respond in a conversational, helpful tone
    - If unsure about something, ask the user for clarification
    - When creating recurring tasks, explain the pattern clearly
    - When tasks have due dates, mention them in responses
    """

    return {
        "client": co,  # Use the native Cohere client
        "tools": user_tools,  # Return the bound tools that can be executed
        "instructions": instructions,
        "model": "command-r-plus"  # Using command-r-plus which is available via Cohere's API
    }