from pydantic import BaseModel
from pydantic.functional_validators import field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .models.task import RecurrenceEnum, TaskPriority


class TaskBase(BaseModel):
    """Base schema for task data"""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # Use lowercase string values (API representation)
    tags: List[str] = []
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[RecurrenceEnum] = RecurrenceEnum.none

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 100:
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 5000:
            raise ValueError('Description cannot exceed 5000 characters')
        return v


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    title: str  # Required field
    # Other fields inherited from TaskBase

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is None:
            return "MEDIUM"
        # Convert API representation (lowercase) to database representation (uppercase)
        priority_map = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH'
        }
        if v.lower() in priority_map:
            return priority_map[v.lower()]
        else:
            # If it's already in uppercase format, return as is
            if v.upper() in ['LOW', 'MEDIUM', 'HIGH']:
                return v.upper()
            else:
                raise ValueError('Priority must be one of: low, medium, high')


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional for partial updates)"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[RecurrenceEnum] = None

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is None:
            return None
        # Convert API representation (lowercase) to database representation (uppercase)
        priority_map = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH'
        }
        if v.lower() in priority_map:
            return priority_map[v.lower()]
        else:
            # If it's already in uppercase format, return as is
            if v.upper() in ['LOW', 'MEDIUM', 'HIGH']:
                return v.upper()
            else:
                raise ValueError('Priority must be one of: low, medium, high')

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 100):
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 5000:
            raise ValueError('Description cannot exceed 5000 characters')
        return v


class TaskToggleComplete(BaseModel):
    """Schema for toggling task completion status"""
    completed: Optional[bool] = None


from pydantic import ConfigDict


class TaskResponse(TaskBase):
    """Schema for task response with additional fields"""
    id: str  # Changed from int to str to match the Task model
    user_id: str
    completed: bool  # This is computed from status field
    created_at: datetime
    updated_at: datetime
    status: str  # Added to match the Task model
    recurrence_pattern: RecurrenceEnum  # Added to match the Task model

    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode for Pydantic v2


class ApiResponse(BaseModel):
    """Generic response wrapper"""
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool
    error: dict


class TaskListResponse(BaseModel):
    """Response for task list with pagination info"""
    success: bool
    data: dict


# --- User-related schemas ---
class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    """
    Schema for user login credentials.
    """
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user information.
    """
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for token data payload.
    """
    user_id: str
    email: str