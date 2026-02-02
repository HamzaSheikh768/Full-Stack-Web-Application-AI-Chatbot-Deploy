from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid

def get_utc_now():
    """Helper function to get current UTC time"""
    return datetime.now(timezone.utc)

class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between user and AI assistant
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # From auth system
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Represents an individual message in a conversation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # "user" or "assistant"
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=get_utc_now)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")