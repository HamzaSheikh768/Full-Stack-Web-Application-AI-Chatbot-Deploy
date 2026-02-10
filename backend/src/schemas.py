from pydantic import BaseModel
from pydantic.functional_validators import field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from .models.task import TaskPriority, RecurrenceEnum


class TaskBase(BaseModel):
    """Base schema for task data with advanced features"""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"  # Use lowercase string values (API representation)
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[Dict[str, Any]] = None
    next_due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('Title is required and cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must not exceed 200 characters')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is None:
            return "medium"
        valid_priorities = {'low', 'medium', 'high', 'LOW', 'MEDIUM', 'HIGH'}
        if v.lower() not in {'low', 'medium', 'high'}:
            raise ValueError('Priority must be one of: low, medium, high')
        return v.lower()

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v is None:
            return []
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed per task')
        # Validate each tag
        for tag in v:
            if not tag or len(tag.strip()) == 0:
                raise ValueError('Tags cannot be empty')
            if len(tag) > 50:
                raise ValueError('Each tag must not exceed 50 characters')
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in v:
            tag_lower = tag.lower().strip()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag.strip())
        return unique_tags

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return v

    @field_validator('remind_at')
    @classmethod
    def validate_remind_at(cls, v, info):
        # Validate that remind_at is before due_date if both are set
        if v and info.data.get('due_date') and v > info.data['due_date']:
            raise ValueError('Reminder time must be before due date')
        if v and v < datetime.now():
            raise ValueError('Reminder time cannot be in the past')
        return v

    @field_validator('recurrence_pattern')
    @classmethod
    def validate_recurrence_pattern(cls, v):
        if v is None:
            return v
            
        # Validate recurrence pattern structure
        required_fields = {'type'}
        if not all(field in v for field in required_fields):
            raise ValueError('Recurrence pattern must include a type field')
            
        recurrence_type = v.get('type')
        valid_types = {'daily', 'weekly', 'monthly', 'yearly'}
        if recurrence_type not in valid_types:
            raise ValueError(f'Recurrence type must be one of: {", ".join(valid_types)}')
            
        # Validate interval if provided
        if 'interval' in v:
            interval = v['interval']
            if not isinstance(interval, int) or interval < 1:
                raise ValueError('Recurrence interval must be a positive integer')
                
        # Validate days_of_week if provided
        if 'days_of_week' in v and recurrence_type in {'weekly'}:
            valid_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
            for day in v['days_of_week']:
                if day.lower() not in valid_days:
                    raise ValueError(f'Invalid day of week: {day}')
                    
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
    remind_at: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    next_due_date: Optional[datetime] = None

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

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v

    @field_validator('remind_at')
    @classmethod
    def validate_remind_at(cls, v, info):
        if v and info.data.get('due_date') and v > info.data['due_date']:
            raise ValueError('Reminder time must be before due date')
        return v


class TaskToggleComplete(BaseModel):
    """Schema for toggling task completion status"""
    completed: Optional[bool] = None


from pydantic import ConfigDict


class TaskResponse(TaskBase):
    """Schema for task response with additional fields"""
    id: str
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]] = []
    remind_at: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[Dict[str, Any]] = None
    next_due_date: Optional[datetime] = None

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