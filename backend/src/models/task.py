from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid
import sqlalchemy as sa
from sqlalchemy import String
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
    title: str = Field(sa_column=sa.Column(sa.String(256), nullable=False))  # Updated to match db
    description: Optional[str] = Field(sa_column=sa.Column(sa.String, nullable=True))  # Updated to match db
    completed: bool = Field(default=False, sa_column=sa.Column('is_completed', sa.Boolean, nullable=False))
    priority: str = Field(default="MEDIUM", sa_column=sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='priorityenum', create_type=False), nullable=False))  # Updated to match db enum values
    due_date: Optional[datetime] = Field(sa_column=sa.Column(sa.DateTime, nullable=True))
    recurrence_pattern: str = Field(default="none", sa_column=sa.Column(sa.String, nullable=False))  # Updated to match db
    order_index: Optional[str] = Field(default="0", sa_column=sa.Column(sa.String, nullable=True))  # Added from db
    created_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
