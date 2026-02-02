from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid
import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.sql.schema import ForeignKey

def get_utc_now():
    """Helper function to get current UTC time"""
    return datetime.now(timezone.utc)


class Session(SQLModel, table=True):
    """
    Session entity representing an active user session with JWT token information
    """
    id: str = Field(
        sa_column=sa.Column(
            String,
            primary_key=True,
            default=lambda: str(uuid.uuid4())
        )
    )
    user_id: str = Field(sa_column=sa.Column(sa.String, sa.ForeignKey("user.id"), nullable=False))
    refresh_token: str = Field(sa_column=sa.Column(sa.String, unique=True, nullable=False, index=True))
    expires_at: datetime = Field(sa_column=sa.Column(sa.DateTime, nullable=False))
    created_at: datetime = Field(default_factory=get_utc_now, sa_column=sa.Column(sa.DateTime, nullable=False))
    revoked: bool = Field(default=False, sa_column=sa.Column(sa.Boolean, nullable=False))
    ip_address: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))
    user_agent: Optional[str] = Field(default=None, sa_column=sa.Column(sa.String, nullable=True))