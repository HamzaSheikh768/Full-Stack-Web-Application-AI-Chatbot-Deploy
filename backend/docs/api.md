# API Documentation: Advanced Todo Features

## Overview

This document describes the API endpoints for the advanced todo features, including priorities, tags, search/filter, sort, recurring tasks, and due dates & reminders.

## Base URL
```
https://api.todo-chatbot.com/v1
```

## Authentication
All API requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## API Endpoints

### Task Management

#### GET /users/{user_id}/tasks
**Description**: Retrieve tasks with advanced filtering and sorting capabilities

**Parameters**:
- `user_id` (path, required): User identifier
- `status` (query, optional): Filter by task status (all, pending, completed) - default: all
- `priority` (query, optional): Filter by priority level (high, medium, low) - comma separated
- `tags` (query, optional): Filter by tags - comma separated
- `search` (query, optional): Search keyword in title or description
- `sort_by` (query, optional): Sort by field (created_at, due_at, priority, title) - default: due_at
- `sort_order` (query, optional): Sort order (asc, desc) - default: asc
- `due_from` (query, optional): Filter tasks with due date from this date
- `due_to` (query, optional): Filter tasks with due date to this date
- `limit` (query, optional): Number of tasks to return - default: 50, max: 100
- `offset` (query, optional): Number of tasks to skip - default: 0

**Response**:
```
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_abc123",
      "title": "Complete project proposal",
      "description": "Finish the proposal for the new project",
      "completed": false,
      "priority": "high",
      "tags": ["work", "urgent"],
      "due_at": "2026-02-15T10:00:00Z",
      "remind_at": "2026-02-14T16:00:00Z",
      "is_recurring": false,
      "recurrence_pattern": null,
      "next_due_date": null,
      "created_at": "2026-02-07T09:00:00Z",
      "updated_at": "2026-02-07T09:00:00Z"
    }
  ],
  "total": 1,
  "page": 1
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden

#### POST /users/{user_id}/tasks
**Description**: Create a new task with advanced features

**Parameters**:
- `user_id` (path, required): User identifier

**Request Body**:
```
{
  "title": "Schedule team meeting",
  "description": "Organize the weekly team sync",
  "priority": "medium",
  "tags": ["work", "meeting"],
  "due_at": "2026-02-12T14:00:00Z",
  "remind_at": "2026-02-12T13:00:00Z",
  "is_recurring": true,
  "recurrence_pattern": {
    "type": "weekly",
    "interval": 1,
    "days_of_week": ["friday"],
    "end_date": "2026-12-31T00:00:00Z"
  }
}
```

**Response**:
```
{
  "id": 2,
  "user_id": "user_abc123",
  "title": "Schedule team meeting",
  "description": "Organize the weekly team sync",
  "completed": false,
  "priority": "medium",
  "tags": ["work", "meeting"],
  "due_at": "2026-02-12T14:00:00Z",
  "remind_at": "2026-02-12T13:00:00Z",
  "is_recurring": true,
  "recurrence_pattern": {
    "type": "weekly",
    "interval": 1,
    "days_of_week": ["friday"],
    "end_date": "2026-12-31T00:00:00Z"
  },
  "next_due_date": "2026-02-13T14:00:00Z",
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z"
}
```

**Status Codes**:
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden

#### GET /users/{user_id}/tasks/{task_id}
**Description**: Retrieve details of a specific task

**Parameters**:
- `user_id` (path, required): User identifier
- `task_id` (path, required): Task identifier

**Response**:
```
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Complete project proposal",
  "description": "Finish the proposal for the new project",
  "completed": false,
  "priority": "high",
  "tags": ["work", "urgent"],
  "due_at": "2026-02-15T10:00:00Z",
  "remind_at": "2026-02-14T16:00:00Z",
  "is_recurring": false,
  "recurrence_pattern": null,
  "next_due_date": null,
  "created_at": "2026-02-07T09:00:00Z",
  "updated_at": "2026-02-07T09:00:00Z"
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

#### PUT /users/{user_id}/tasks/{task_id}
**Description**: Update task details with advanced features

**Parameters**:
- `user_id` (path, required): User identifier
- `task_id` (path, required): Task identifier

**Request Body**:
```
{
  "title": "Updated task title",
  "description": "Updated description",
  "priority": "high",
  "tags": ["work", "important"],
  "due_at": "2026-02-20T15:00:00Z",
  "remind_at": "2026-02-20T14:00:00Z",
  "is_recurring": true,
  "recurrence_pattern": {
    "type": "monthly",
    "interval": 1,
    "day_of_month": 1,
    "end_date": "2026-12-31T00:00:00Z"
  },
  "completed": false
}
```

**Response**:
Same as GET /users/{user_id}/tasks/{task_id}

**Status Codes**:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

#### DELETE /users/{user_id}/tasks/{task_id}
**Description**: Remove a task from the user's list

**Parameters**:
- `user_id` (path, required): User identifier
- `task_id` (path, required): Task identifier

**Status Codes**:
- 204: Deleted
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

#### PATCH /users/{user_id}/tasks/{task_id}/complete
**Description**: Toggle the completion status of a task

**Parameters**:
- `user_id` (path, required): User identifier
- `task_id` (path, required): Task identifier

**Response**:
Same as GET /users/{user_id}/tasks/{task_id}

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

### Cohere AI Chat Integration

#### POST /users/{user_id}/chat
**Description**: Send a message to the Cohere AI chatbot for natural language task management

**Parameters**:
- `user_id` (path, required): User identifier

**Request Body**:
```
{
  "conversation_id": 123,
  "message": "Add a high priority task to buy groceries due tomorrow with tags shopping and food",
  "metadata": {
    "timezone": "America/New_York",
    "language": "en"
  }
}
```

**Response**:
```
{
  "conversation_id": 123,
  "response": "I've added a high-priority task 'Buy groceries' due tomorrow with tags shopping and food.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user_abc123",
        "title": "Buy groceries",
        "description": "",
        "priority": "high",
        "tags": ["shopping", "food"],
        "due_at": "2026-02-09T00:00:00Z"
      }
    }
  ],
  "suggested_actions": [
    "View all tasks",
    "Add another task",
    "Set a reminder"
  ]
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden

## Advanced Features API Details

### Task Priorities
- Available priorities: `high`, `medium`, `low`
- Used for organizing tasks by importance
- Can be filtered and sorted by priority

### Task Tags
- Array of string tags for categorizing tasks
- Support for multiple tags per task (max 10)
- Used for filtering and grouping tasks

### Recurring Tasks
- Support for daily, weekly, monthly, and yearly recurrence patterns
- Flexible configuration with intervals and exceptions
- Automatic generation of next occurrence when completed

### Due Dates and Reminders
- Due date field for task deadlines
- Reminder time field for notifications before due date
- Visual indicators for overdue tasks

## Error Responses

All error responses follow this format:
```
{
  "error": {
    "type": "string",
    "message": "string",
    "details": "object"
  }
}
```

Common error types:
- `invalid_request_error`: Request parameters are invalid
- `authentication_error`: Authentication failed
- `permission_error`: User lacks permission
- `resource_not_found`: Requested resource doesn't exist
- `cohere_api_error`: Error communicating with Cohere API

## Rate Limiting

The API implements rate limiting:
- Per-user: 1000 requests per hour
- Per-IP: 5000 requests per hour
- Cohere API: Limited by Cohere's rate limits