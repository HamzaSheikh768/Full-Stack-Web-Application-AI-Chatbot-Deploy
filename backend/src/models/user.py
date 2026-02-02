from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid
import sqlalchemy as sa
from sqlalchemy import String
from enum import Enum

def get_utc_now():
    """Helper function to get current UTC time"""
    return datetime.now(timezone.utc)


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(SQLModel, table=True):
    """
    User entity representing a registered user in the system
    """
    id: str = Field(
        sa_column=sa.Column(
            String,
            primary_key=True,
            default=lambda: str(uuid.uuid4())
        )
    )
    email: str = Field(sa_column=sa.Column(sa.String, unique=True, nullable=False, index=True))
    first_name: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))
    last_name: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))
    password_hash: str = Field(sa_column=sa.Column('hashed_password', sa.String, nullable=False))
    is_active: bool = Field(default=True, sa_column=sa.Column(sa.Boolean, nullable=False))
    created_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))