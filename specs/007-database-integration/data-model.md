# Data Model: Database Integration for Todo AI Chatbot

**Feature**: Database Integration for Todo AI Chatbot
**Source**: `spec.md` → Functional Requirements

## 1. Database Entities (SQLModel)

### Task
Represents a user's to-do item with title, description, completion status, and timestamps.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique task identifier |
| user_id | String | Yes | Index | Owner of the task (from Auth) |
| title | String | Yes | Max 200 chars | Task summary |
| description | String | No | Max 1000 chars | Detailed information |
| completed | Boolean | Yes | Default: False | Completion status |
| created_at | DateTime | Yes | Default: Now | Timestamp of creation |
| updated_at | DateTime | Yes | Default: Now | Timestamp of last update |

### Conversation
Represents a chat session between user and AI assistant, containing metadata and linking to associated messages.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique conversation identifier |
| user_id | String | Yes | Index | Owner of the conversation |
| title | String | No | Max 200 chars | Optional conversation summary |
| created_at | DateTime | Yes | Default: Now | Timestamp of creation |
| updated_at | DateTime | Yes | Default: Now | Timestamp of last update |

### Message
Represents an individual message in a conversation, including the sender (user/assistant), content, and timestamp.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique message identifier |
| conversation_id | Integer | Yes | FK → Conversation, Index | Associated conversation |
| user_id | String | Yes | Index | Sender of the message |
| role | String | Yes | Enum: "user", "assistant", "tool" | Origin of the message |
| content | String | Yes | Max 5000 chars | Message text content |
| created_at | DateTime | Yes | Default: Now | Timestamp of creation |

## 2. Entity Relationships

```
User (1) ←→ (Many) Task
User (1) ←→ (Many) Conversation
Conversation (1) ←→ (Many) Message
```

## 3. Validation Rules

### Task Validation
- Title: 1-200 characters, required
- Description: 0-1000 characters, optional
- Completed: Boolean, defaults to False

### Conversation Validation
- Title: 0-200 characters, optional
- User_id: Required, indexed for performance

### Message Validation
- Role: Must be one of "user", "assistant", or "tool"
- Content: 1-5000 characters, required
- User_id: Required, indexed for isolation

## 4. Indexing Strategy

### Required Indexes
- Task.user_id (for user isolation)
- Message.conversation_id (for conversation history queries)
- Message.user_id (for user isolation)
- Conversation.user_id (for user isolation)
- Message.created_at (for chronological ordering)
- Task.created_at (for task listing)

### Composite Indexes
- Message (conversation_id, created_at) - for conversation history retrieval
- Task (user_id, completed) - for filtered task queries

## 5. State Transitions

### Task State Transitions
- Created → Pending (default upon creation)
- Pending → Completed (via complete_task tool)
- Completed → Pending (via update_task tool)

### Message State Transitions
- None (immutable once created)

### Conversation State Transitions
- None (immutable once created, only metadata updates)

## 6. Referential Integrity

- Message.conversation_id references Conversation.id (CASCADE delete)
- Task.user_id and Message.user_id and Conversation.user_id all tied to user authentication system
- Foreign key constraints enforced at database level