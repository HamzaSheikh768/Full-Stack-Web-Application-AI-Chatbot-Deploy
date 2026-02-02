from sqlmodel import select
from typing import List, Dict, Any
from datetime import datetime

from ..database.db import SessionLocal
from ..models.conversation import Conversation, Message


def get_conversation_history(conversation_id: int, user_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve conversation history from the database.
    Ensures user isolation by filtering by user_id.
    """
    with SessionLocal() as session:
        # First verify that the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            # Return empty history if conversation doesn't exist or doesn't belong to user
            return []

        # Get all messages in the conversation
        msgs_query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        result = session.execute(msgs_query)
        messages = result.all()

        # Convert Row objects to proper Message model instances
        # The result.all() returns Row objects where the first element is the Message
        message_objects = [row[0] for row in messages]

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in message_objects
        ]


def create_conversation(user_id: str, title: str = None) -> int:
    """
    Create a new conversation in the database.
    """
    with SessionLocal() as session:
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation.id


def add_message_to_conversation(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str
) -> None:
    """
    Add a message to a conversation in the database.
    Ensures user isolation by verifying conversation ownership.
    """
    with SessionLocal() as session:
        # Verify that the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found or doesn't belong to user")

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()


def get_user_conversations(user_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve all conversations for a specific user.
    Ensures user isolation by filtering by user_id.
    """
    with SessionLocal() as session:
        # Get all conversations for the user
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
        result = session.execute(stmt)
        conversations = result.scalars().all()

        # Convert to dictionary format
        conversation_list = []
        for conv in conversations:
            # Get the last message to show preview
            last_message_stmt = (
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at.desc())
                .limit(1)
            )
            last_message_result = session.execute(last_message_stmt)
            last_message = last_message_result.scalar_one_or_none()

            conv_dict = {
                "id": conv.id,
                "title": conv.title or f"Conversation {conv.id}",
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "last_message": last_message.content[:50] + "..." if last_message and len(last_message.content) > 50 else (last_message.content if last_message else "No messages yet"),
                "last_message_at": last_message.created_at.isoformat() if last_message else None
            }
            conversation_list.append(conv_dict)

        return conversation_list


def get_or_create_conversation(
    conversation_id: int = None,
    user_id: str = None,
    title: str = None
) -> int:
    """
    Get existing conversation (if valid for user) or create a new one.
    """
    if conversation_id:
        # Check if conversation exists and belongs to user
        with SessionLocal() as session:
            conversation = session.get(Conversation, conversation_id)
            if conversation and conversation.user_id == user_id:
                return conversation_id

    # Create new conversation
    return create_conversation(user_id, title)