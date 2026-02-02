# Data Model: JWT Authentication

**Feature**: 005-jwt-auth
**Date**: 2026-01-22
**Status**: Complete

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           USER                                   │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ email: VARCHAR(254) UNIQUE NOT NULL                             │
│ name: VARCHAR(100) NULL                                         │
│ password_hash: VARCHAR(255) NOT NULL                            │
│ is_active: BOOLEAN DEFAULT TRUE                                 │
│ created_at: TIMESTAMP NOT NULL                                  │
│ updated_at: TIMESTAMP NOT NULL                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           TASK                                   │
├─────────────────────────────────────────────────────────────────┤
│ id: UUID (PK)                                                   │
│ user_id: UUID (FK → user.id) NOT NULL                           │
│ parent_id: UUID (FK → task.id) NULL                             │
│ title: VARCHAR(200) NOT NULL                                    │
│ description: VARCHAR(1000) NULL                                 │
│ is_completed: BOOLEAN DEFAULT FALSE                             │
│ priority: ENUM('low', 'medium', 'high') DEFAULT 'medium'        │
│ due_date: TIMESTAMP NULL                                        │
│ recurrence_pattern: ENUM('daily', 'weekly', 'monthly') NULL     │
│ order_index: VARCHAR DEFAULT '0'                                │
│ created_at: TIMESTAMP NOT NULL                                  │
│ updated_at: TIMESTAMP NOT NULL                                  │
├─────────────────────────────────────────────────────────────────┤
│ INDEX: idx_task_user_id ON user_id                              │
└─────────────────────────────────────────────────────────────────┘
```

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user who can authenticate and own tasks.

**Status**: ✅ Already implemented in `backend/src/models/user.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL | Login credential, unique per user |
| `name` | VARCHAR(100) | NULL | Display name (optional) |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active status |
| `created_at` | TIMESTAMP | NOT NULL, auto | Account creation time |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Last update time |

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique (case-insensitive comparison recommended)
- Password must be minimum 8 characters before hashing
- Password is stored as bcrypt hash (never plain text)

### Task Entity

**Purpose**: Represents a todo item owned by a specific user.

**Status**: ✅ Already implemented in `backend/src/models/task.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `user_id` | UUID | FK → user.id, NOT NULL | Owner of the task |
| `parent_id` | UUID | FK → task.id, NULL | For hierarchical tasks |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | VARCHAR(1000) | NULL | Task details |
| `is_completed` | BOOLEAN | DEFAULT FALSE | Completion status |
| `priority` | ENUM | DEFAULT 'medium' | Priority level |
| `due_date` | TIMESTAMP | NULL | Due date/time |
| `recurrence_pattern` | ENUM | NULL | Recurring pattern |
| `order_index` | VARCHAR | DEFAULT '0' | Display order |
| `created_at` | TIMESTAMP | NOT NULL, auto | Creation time |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Last update time |

**Indexes**:
- `idx_task_user_id` on `user_id` for efficient user-scoped queries

**Relationships**:
- `user_id` → `user.id` (Many-to-One): Each task belongs to exactly one user
- `parent_id` → `task.id` (Self-referential): For subtask support

---

## JWT Token Structure

**Note**: Not stored in database - stateless tokens

### Access Token Claims

```json
{
  "sub": "user@example.com",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1706000000,
  "iat": 1705999000
}
```

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | string | Subject - user's email address |
| `user_id` | string (UUID) | User's unique identifier |
| `exp` | integer | Expiration timestamp (Unix) |
| `iat` | integer | Issued at timestamp (Unix) |

**Token Configuration**:
- Algorithm: HS256
- Expiration: 7 days (604800 seconds) - aligned with Better Auth session
- Secret: `BETTER_AUTH_SECRET` environment variable

---

## Data Access Patterns

### User Queries

```sql
-- Find user by email (login)
SELECT * FROM user WHERE email = :email LIMIT 1;

-- Find user by ID (token verification)
SELECT * FROM user WHERE id = :user_id LIMIT 1;

-- Check email existence (registration)
SELECT COUNT(*) FROM user WHERE email = :email;
```

### Task Queries (User-Scoped)

```sql
-- Get all tasks for user
SELECT * FROM task WHERE user_id = :user_id ORDER BY created_at DESC;

-- Get task by ID with ownership check
SELECT * FROM task WHERE id = :task_id AND user_id = :user_id;

-- Filter tasks by status
SELECT * FROM task WHERE user_id = :user_id AND is_completed = :status;

-- Search tasks
SELECT * FROM task
WHERE user_id = :user_id
AND (title ILIKE :search OR description ILIKE :search);
```

---

## State Transitions

### User Account States

```
┌─────────────┐     register      ┌─────────────┐
│   (none)    │ ─────────────────▶│   Active    │
└─────────────┘                   └─────────────┘
                                        │
                                        │ deactivate
                                        ▼
                                  ┌─────────────┐
                                  │  Inactive   │
                                  └─────────────┘
```

### Task States

```
┌─────────────┐     create        ┌─────────────┐
│   (none)    │ ─────────────────▶│   Pending   │
└─────────────┘                   └─────────────┘
                                        │
                                        │ complete
                                        ▼
                                  ┌─────────────┐
                                  │  Completed  │
                                  └─────────────┘
                                        │
                                        │ uncomplete
                                        │
                                  ┌─────────────┐
                                  │   Pending   │◀──────┘
                                  └─────────────┘
```

---

## Migration Notes

### Existing Schema Status

The database schema for authentication is **already in place**:

1. **User table**: Exists with all required fields
2. **Task table**: Exists with `user_id` foreign key
3. **Indexes**: `idx_task_user_id` already created

### Data Migration

For existing tasks created in "public access" mode:

```sql
-- Identify orphaned tasks (no valid user_id)
SELECT COUNT(*) FROM task WHERE user_id = 'public-user' OR user_id IS NULL;

-- Options:
-- 1. Delete orphaned tasks (clean slate)
-- 2. Assign to admin user (preserve data)
-- 3. Leave as-is (public tasks become inaccessible)
```

**Recommendation**: Create migration script to handle orphaned tasks based on business decision.

---

## SQLModel Implementation Reference

### User Model (Existing)

```python
# backend/src/models/user.py
class User(SQLModel, table=True):
    id: str = Field(sa_column=sa.Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4))
    email: str = Field(sa_column=sa.Column(sa.String, unique=True, nullable=False))
    name: Optional[str] = Field(sa_column=sa.Column(sa.String(100)))
    password_hash: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
```

### Task Model (Existing)

```python
# backend/src/models/task.py
class Task(SQLModel, table=True):
    id: str = Field(sa_column=sa.Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4))
    user_id: str = Field(sa_column=sa.Column(sa.Text, sa.ForeignKey("user.id"), nullable=False))
    title: str = Field(sa_column=sa.Column(sa.String(200), nullable=False))
    # ... other fields
```

---

## Validation Rules Summary

| Entity | Field | Rule |
|--------|-------|------|
| User | email | Valid email format, unique, max 254 chars |
| User | password | Min 8 chars, bcrypt hashed |
| User | name | Optional, max 100 chars |
| Task | title | Required, max 200 chars |
| Task | description | Optional, max 1000 chars |
| Task | user_id | Required, must reference existing user |
| Task | priority | Must be 'low', 'medium', or 'high' |
