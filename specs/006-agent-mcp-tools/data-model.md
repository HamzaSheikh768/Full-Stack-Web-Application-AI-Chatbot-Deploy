# Data Model: Agent & MCP Tools

**Feature**: Agent & MCP Tools for Todo AI Chatbot
**Source**: `spec.md` -> Functional Requirements

## 1. Database Entities (SQLModel)

### Task
Existing model update/verification.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique task identifier |
| user_id | String | Yes | Index | Owner of the task (from Auth) |
| title | String | Yes | Max 200 chars | Task summary |
| description | String | No | Max 1000 chars | detailed info |
| completed | Boolean | Yes | Default: False | Status flag |
| created_at | DateTime | Yes | Default: Now | updates on creation |
| updated_at | DateTime | Yes | Default: Now | updates on change |

### Conversation
Persists chat history for stateless agent reload.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Conversation ID |
| user_id | String | Yes | Index | Owner |
| title | String | No | | Optional summary |
| created_at | DateTime | Yes | | |
| updated_at | DateTime | Yes | | |

### Message
Individual chat turns.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | |
| conversation_id | Integer | Yes | FK -> Conversation | |
| role | String | Yes | "user" or "assistant" | origin |
| content | String | Yes | Text | The message body |
| created_at | DateTime | Yes | | |

## 2. MCP Tool Schemas (JSON)

These schemas define the inputs for the MCP tools exposed to the Agent.

### `add_task`
```json
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user (system injected)" },
      "title": { "type": "string", "description": "The title of the task" },
      "description": { "type": "string", "description": "Optional details about the task" }
    },
    "required": ["user_id", "title"]
  }
}
```

### `list_tasks`
```json
{
  "name": "list_tasks",
  "description": "Retrieve a list of tasks, optionally filtered by status",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user (system injected)" },
      "status": {
        "type": "string",
        "enum": ["all", "pending", "completed"],
        "description": "Filter tasks by status"
      }
    },
    "required": ["user_id"]
  }
}
```

### `complete_task`
```json
{
  "name": "complete_task",
  "description": "Mark a specific task as completed",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user (system injected)" },
      "task_id": { "type": "integer", "description": "The ID of the task to complete" }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### `delete_task`
```json
{
  "name": "delete_task",
  "description": "Permanently remove a task",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user (system injected)" },
      "task_id": { "type": "integer", "description": "The ID of the task to delete" }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### `update_task`
```json
{
  "name": "update_task",
  "description": "Modify the title or description of an existing task",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": { "type": "string", "description": "The ID of the user (system injected)" },
      "task_id": { "type": "integer", "description": "The ID of the task to update" },
      "title": { "type": "string", "description": "New title" },
      "description": { "type": "string", "description": "New description" }
    },
    "required": ["user_id", "task_id"]
  }
}
```
