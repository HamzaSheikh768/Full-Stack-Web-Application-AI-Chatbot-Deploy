from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import uuid
import sqlalchemy as sa
from sqlalchemy import String, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum
from sqlalchemy.sql.schema import ForeignKey
import json

def get_utc_now():
    """Helper function to get current UTC time"""
    return datetime.now(timezone.utc)


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RecurrenceEnum(str, Enum):
    """Recurrence patterns for tasks"""
    none = "none"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class Task(SQLModel, table=True):
    """
    Task entity representing a user's task item in the todo system
    Extended with advanced features: tags, reminders, recurring tasks
    """
    id: str = Field(
        sa_column=sa.Column(
            String,
            primary_key=True,
            default=lambda: str(uuid.uuid4())
        )
    )
    user_id: str = Field(sa_column=sa.Column(sa.String, sa.ForeignKey("user.id"), nullable=False, index=True))
    parent_id: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, sa.ForeignKey("task.id"), nullable=True))
    title: str = Field(sa_column=sa.Column(sa.String(256), nullable=False))
    description: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))
    completed: bool = Field(default=False, sa_column=sa.Column('is_completed', sa.Boolean, nullable=False))
    priority: str = Field(default="MEDIUM", sa_column=sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='priorityenum', create_type=False), nullable=False))

    # Advanced features - new fields
    tags: Optional[List[str]] = Field(default=None, sa_column=sa.Column(ARRAY(sa.String), nullable=True))
    due_date: Optional[datetime] = Field(sa_column=sa.Column(sa.DateTime, nullable=True))
    remind_at: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime, nullable=True))
    is_recurring: bool = Field(default=False, sa_column=sa.Column(sa.Boolean, nullable=False, server_default='false'))
    recurrence_pattern: Optional[Dict[str, Any]] = Field(default=None, sa_column=sa.Column(JSONB, nullable=True))
    next_due_date: Optional[datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime, nullable=True))

    order_index: Optional[str] = Field(default="0", sa_column=sa.Column(sa.String, nullable=True))
    created_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
