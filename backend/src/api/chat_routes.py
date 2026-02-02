from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any, List, Optional
import json
from pydantic import BaseModel

from ..agent.runner import run_agent_sync
from ..services.chat_service import get_conversation_history
from ..auth import get_current_user
from ..database.db import SessionLocal
from sqlmodel import Session

router = APIRouter(prefix="", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]

class ConversationHistoryResponse(BaseModel):
    conversation_id: int
    messages: List[Dict[str, Any]]

@router.post("/{user_id}/chat")
def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Chat endpoint that processes user messages through the AI agent.
    The agent uses MCP tools to manage tasks.
    """
    # Verify that the user_id in the path matches the authenticated user
    # Convert both to string to ensure type consistency
    authenticated_user_id = str(current_user["user_id"])
    path_user_id = str(user_id)

    if authenticated_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Token user_id '{authenticated_user_id}' does not match path user_id '{path_user_id}'"
        )

    # Use the authenticated user's ID from the token for internal operations
    actual_authenticated_user_id = current_user["user_id"]

    try:
        # Run the agent with the user message (using sync version)
        result = run_agent_sync(
            user_id=actual_authenticated_user_id,
            message_text=request.message,
            conversation_id=request.conversation_id
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result["tool_calls"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")


@router.get("/{user_id}/conversations")
def get_user_conversations_endpoint(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Retrieve a list of all conversations for the user.
    User isolation is maintained through authentication.
    """
    # Verify that the user_id in the path matches the authenticated user
    # Convert both to string to ensure type consistency
    authenticated_user_id = str(current_user["user_id"])
    path_user_id = str(user_id)

    if authenticated_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Token user_id '{authenticated_user_id}' does not match path user_id '{path_user_id}'"
        )

    # Use the authenticated user's ID from the token for internal operations
    actual_authenticated_user_id = current_user["user_id"]

    try:
        # Get all conversations for the user from service
        from ..services.chat_service import get_user_conversations
        conversations = get_user_conversations(actual_authenticated_user_id)

        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load conversations: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}/history")
def get_conversation_history_endpoint(
    user_id: str,
    conversation_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Retrieve conversation history for a specific conversation.
    User isolation is maintained through authentication.
    """
    # Verify that the user_id in the path matches the authenticated user
    # Convert both to string to ensure type consistency
    authenticated_user_id = str(current_user["user_id"])
    path_user_id = str(user_id)

    if authenticated_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Token user_id '{authenticated_user_id}' does not match path user_id '{path_user_id}'"
        )

    # Use the authenticated user's ID from the token for internal operations
    actual_authenticated_user_id = current_user["user_id"]

    try:
        # Get conversation history from service (using sync version)
        messages = get_conversation_history(conversation_id, actual_authenticated_user_id)

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=messages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load conversation history: {str(e)}")
