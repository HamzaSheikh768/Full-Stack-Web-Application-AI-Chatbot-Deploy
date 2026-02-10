# Data Model: Kubernetes Deployment for Oracle Cloud OKE

## Overview

This document defines the extended data model for the Kubernetes deployment of the Todo Chatbot application, including new entities and relationships required for the event-driven architecture, Dapr integration, and cloud deployment patterns.

## Entity Definitions

### Task Entity (Extended)
**Purpose**: Represents a user's task item with advanced features for the cloud deployment

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key, Auto-generated | Unique identifier for the task |
| user_id | String | Foreign Key, Not Null | Owner of the task (for user isolation) |
| title | String(200) | Not Null, Length: 1-200 | Task title |
| description | String(1000) | Nullable, Length: 0-1000 | Task description |
| completed | Boolean | Not Null, Default: False | Completion status |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when task was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when task was last updated |
| priority | String(Enum) | Not Null, Default: "medium", Values: "high", "medium", "low" | Task priority level |
| tags | Array(String) | Nullable, Max: 10 elements | Array of tags/categories for the task |
| due_at | DateTime | Nullable | Optional due date and time for the task |
| remind_at | DateTime | Nullable | Optional reminder time (can be before due_at) |
| is_recurring | Boolean | Not Null, Default: False | Flag indicating if task recurs |
| recurrence_pattern | JSONB | Nullable | JSON object defining recurrence pattern |
| next_due_date | DateTime | Nullable | Date of next occurrence for recurring tasks |
| dapr_metadata | JSONB | Nullable | Dapr-specific metadata for event processing |

#### Relationships
- **User**: Many tasks belong to one user (user_id foreign key)

#### Validation Rules
- priority must be one of: "high", "medium", "low"
- tags array must not exceed 10 elements
- remind_at must be before due_at if both are set
- recurrence_pattern follows RFC 5545-inspired structure when is_recurring is true
- next_due_date must be set when is_recurring is true

### User Entity (Existing)
**Purpose**: Represents a registered user in the system

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique identifier for the user |
| email | String | Not Null, Unique | User's email address |
| name | String | Nullable | User's name |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when user was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when user was last updated |

### Conversation Entity (Extended)
**Purpose**: Represents a chat conversation with the AI assistant

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique identifier for the conversation |
| user_id | String | Foreign Key, Not Null | Owner of the conversation |
| title | String(200) | Not Null | Title of the conversation |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when conversation was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when conversation was last updated |
| dapr_metadata | JSONB | Nullable | Dapr-specific metadata for event processing |

### Message Entity (Extended)
**Purpose**: Represents a message in a conversation

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique identifier for the message |
| conversation_id | String | Foreign Key, Not Null | Conversation this message belongs to |
| role | String(Enum) | Not Null, Values: "user", "assistant" | Role of the message sender |
| content | Text | Not Null | Content of the message |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when message was created |
| dapr_metadata | JSONB | Nullable | Dapr-specific metadata for event processing |

### Reminder Entity (New)
**Purpose**: Represents a scheduled reminder for a task

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique identifier for the reminder |
| task_id | String | Foreign Key, Not Null | Associated task |
| user_id | String | Foreign Key, Not Null | Owner of the reminder |
| scheduled_at | DateTime | Not Null | When the reminder should be triggered |
| status | String(Enum) | Not Null, Default: "pending", Values: "pending", "sent", "cancelled" | Status of the reminder |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when reminder was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when reminder was last updated |

### RecurringTaskSchedule Entity (New)
**Purpose**: Represents the schedule for recurring tasks

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique identifier for the schedule |
| original_task_id | String | Foreign Key, Not Null | Original task that is recurring |
| user_id | String | Foreign Key, Not Null | Owner of the schedule |
| recurrence_pattern | JSONB | Not Null | Pattern for recurrence |
| next_occurrence | DateTime | Not Null | When the next occurrence should be created |
| status | String(Enum) | Not Null, Default: "active", Values: "active", "paused", "cancelled" | Status of the schedule |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when schedule was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when schedule was last updated |

## State Transitions

### Task States
1. **Created**: New task with default values
2. **Pending**: Task exists but not completed
3. **Completed**: Task marked as done
4. **Recurring**: Task that generates future occurrences
5. **Overdue**: Task past its due date

### Reminder States
1. **Scheduled**: Reminder created but not yet sent
2. **Sent**: Reminder notification delivered
3. **Cancelled**: Reminder cancelled before sending

### RecurringTaskSchedule States
1. **Active**: Schedule is generating occurrences
2. **Paused**: Schedule temporarily inactive
3. **Cancelled**: Schedule permanently stopped

## SQLModel Class Definitions

```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
import enum
from sqlalchemy import JSON
from enum import Enum

class PriorityLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ReminderStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"

class RecurringTaskScheduleStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class Task(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Advanced features
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    tags: Optional[List[str]] = Field(sa_column=Column("tags", sa.ARRAY(sa.String)))
    due_at: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column("recurrence_pattern", JSON))
    next_due_date: Optional[datetime] = None
    dapr_metadata: Optional[dict] = Field(default=None, sa_column=Column("dapr_metadata", JSON))

    # Validation constraints handled at application level
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate remind_at is not after due_at
        if self.remind_at and self.due_at and self.remind_at > self.due_at:
            raise ValueError("Remind time cannot be after due time")

        # Update updated_at on any change
        self.updated_at = datetime.utcnow()

class Reminder(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    task_id: str = Field(foreign_key="task.id")
    user_id: str = Field(foreign_key="user.id")
    scheduled_at: datetime
    status: ReminderStatus = Field(default=ReminderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RecurringTaskSchedule(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    original_task_id: str = Field(foreign_key="task.id")
    user_id: str = Field(foreign_key="user.id")
    recurrence_pattern: dict = Field(sa_column=Column("recurrence_pattern", JSON))
    next_occurrence: datetime
    status: RecurringTaskScheduleStatus = Field(default=RecurringTaskScheduleStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Indexing Strategy

### Primary Indexes
- `idx_tasks_user_id`: For user isolation queries
- `idx_tasks_priority`: For priority-based filtering
- `idx_tasks_completed`: For status-based filtering

### Performance Indexes
- `idx_tasks_due_at`: For due date queries
- `idx_tasks_next_due_date`: For recurring task scheduling
- `idx_tasks_created_at`: For chronological ordering
- `idx_tasks_tags`: GIN index for tag-based filtering

### Full-Text Search Indexes
- `idx_tasks_title_tsv`: For title search
- `idx_tasks_description_tsv`: For description search

## Data Access Patterns

### Common Queries

1. **Get user's pending tasks with filters**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = $1
     AND completed = false
     AND (priority = ANY($2) OR $2 IS NULL)
     AND (tag = ANY(tags) OR $3 IS NULL)
   ORDER BY due_at ASC NULLS LAST, priority DESC;
   ```

2. **Search tasks by keyword**:
   ```sql
   SELECT * FROM tasks
   WHERE user_id = $1
     AND (to_tsvector('english', title || ' ' || COALESCE(description, '')) @@ plainto_tsquery('english', $2));
   ```

3. **Get recurring tasks due for generation**:
   ```sql
   SELECT * FROM recurring_task_schedules
   WHERE next_occurrence <= NOW()
     AND status = 'active';
   ```

4. **Get reminders due for processing**:
   ```sql
   SELECT * FROM reminders
   WHERE scheduled_at <= NOW()
     AND status = 'pending';
   ```

## Migration Strategy

### From Basic to Advanced Schema
1. **Backup existing data**
2. **Add new columns to tasks table**
3. **Create new tables for reminders and recurring schedules**
4. **Create indexes**
5. **Update application code to handle new fields**
6. **Validate data integrity**

### Backward Compatibility
- New fields have sensible defaults
- Existing functionality remains unchanged
- Old data will have default values for new fields

## Security Considerations

### User Isolation
- All queries must filter by user_id
- Foreign key constraints enforce referential integrity
- Application layer must validate user ownership

### Data Validation
- Input validation at API layer
- Database constraints for data integrity
- Business rule validation in application logic

## Performance Considerations

### Query Optimization
- Use indexes for common filter operations
- Implement pagination for large result sets
- Consider caching for frequently accessed data

### Index Maintenance
- Regular monitoring of index usage
- Periodic vacuuming and analyzing of tables
- Review and optimize indexes based on query patterns

## Future Extensibility

### Potential Additions
- Custom fields for tasks
- Nested task relationships
- Time tracking for tasks
- Attachment support

### Schema Evolution
- Use JSONB for flexible data storage
- Maintain backward compatibility
- Document breaking changes in migration notes