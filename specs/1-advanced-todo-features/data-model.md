# Data Model: Advanced Todo Features

**Date**: 2026-02-08
**Feature**: Advanced Todo Features
**Spec**: [spec.md](./spec.md)

## Overview

This document defines the extended data model for the advanced todo features, including new fields and relationships to support priorities, tags, search/filter, sort, recurring tasks, and due dates & reminders.

## Entity Definitions

### Task Entity (Extended)

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for the task |
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

#### Relationships
- **User**: Many tasks belong to one user (user_id foreign key)

#### Validation Rules
- priority must be one of: "high", "medium", "low"
- tags array must not exceed 10 elements
- remind_at must be before due_at if both are set
- recurrence_pattern follows RFC 5545-inspired structure when is_recurring is true
- next_due_date must be set when is_recurring is true

### Recurrence Pattern Structure
```json
{
  "type": "daily|weekly|monthly|yearly",
  "interval": 1,
  "days_of_week": ["monday", "wednesday", "friday"],
  "day_of_month": 15,
  "month_of_year": 1,
  "end_date": "2026-12-31",
  "occurrence_count": 10,
  "exceptions": ["2026-11-25"]
}
```

### User Entity (Existing)
*Note: This entity is already defined but referenced here for completeness*

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String | Primary Key | Unique identifier for the user |
| email | String | Not Null, Unique | User's email address |
| name | String | Nullable | User's name |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when user was created |

## Database Schema

### Tasks Table Extension
```sql
-- Extending existing tasks table
ALTER TABLE tasks
ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'medium',
ADD COLUMN tags TEXT[], -- PostgreSQL array type
ADD COLUMN due_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN remind_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN recurrence_pattern JSONB,
ADD COLUMN next_due_date TIMESTAMP WITH TIME ZONE;

-- Add enum constraint for priority
CREATE TYPE priority_level AS ENUM ('high', 'medium', 'low');
ALTER TABLE tasks ALTER COLUMN priority TYPE priority_level USING priority::priority_level;

-- Add check constraint for remind_at vs due_at
ALTER TABLE tasks ADD CONSTRAINT check_remind_before_due
CHECK (remind_at IS NULL OR due_at IS NULL OR remind_at <= due_at);

-- Create indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_at ON tasks(due_at);
CREATE INDEX idx_tasks_next_due_date ON tasks(next_due_date);
CREATE INDEX idx_tasks_is_recurring ON tasks(is_recurring);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE GIN INDEX idx_tasks_tags ON tasks USING GIN(tags);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at);

-- Full-text search indexes
CREATE INDEX idx_tasks_title_tsv ON tasks USING GIN(to_tsvector('english', title));
CREATE INDEX idx_tasks_description_tsv ON tasks USING GIN(to_tsvector('english', COALESCE(description, '')));
```

## State Transitions

### Task States
1. **Created**: New task with default values
2. **Pending**: Task exists but not completed
3. **Completed**: Task marked as done
4. **Recurring**: Task that generates future occurrences
5. **Overdue**: Task past its due date

### Transition Rules
- Created → Pending: Automatic upon creation
- Pending → Completed: When user marks as complete
- Completed → Pending: When user reopens task
- Pending → Recurring: When recurrence is enabled
- Pending → Overdue: When due_at passes and not completed
- Recurring → Completed: When recurring task is completed (generates next occurrence)

## SQLModel Class Definition

```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
import enum

class PriorityLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # New fields for advanced features
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    tags: Optional[List[str]] = Field(sa_column=Column("tags", sa.ARRAY(sa.String)))
    due_at: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[dict] = Field(default=None, sa_column=Column("recurrence_pattern", sa.JSON))
    next_due_date: Optional[datetime] = None

    # Validation constraints handled at application level
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate remind_at is not after due_at
        if self.remind_at and self.due_at and self.remind_at > self.due_at:
            raise ValueError("Remind time cannot be after due time")

        # Update updated_at on any change
        self.updated_at = datetime.utcnow()
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
   SELECT * FROM tasks
   WHERE is_recurring = true
     AND next_due_date <= NOW()
     AND completed = false;
   ```

4. **Get tasks for reminder processing**:
   ```sql
   SELECT * FROM tasks
   WHERE remind_at IS NOT NULL
     AND remind_at <= NOW()
     AND completed = false;
   ```

## Migration Strategy

### From Basic to Advanced Schema
1. **Backup existing data**
2. **Add new columns to tasks table**
3. **Create indexes**
4. **Update application code to handle new fields**
5. **Validate data integrity**

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