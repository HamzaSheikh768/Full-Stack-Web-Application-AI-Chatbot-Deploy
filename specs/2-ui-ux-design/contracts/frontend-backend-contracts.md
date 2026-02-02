# Frontend-Backend API Contracts for Todo App

## Authentication Endpoints

### Login
- **Endpoint**: `POST /api/auth/login`
- **Request**:
  ```
  Headers: Content-Type: application/json
  Body: {
    "email": "string (valid email)",
    "password": "string (min 8 characters)"
  }
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "token": "string (JWT token)",
    "user": {
      "id": "string",
      "name": "string",
      "email": "string",
      "themePreference": "'dark'|'light'"
    }
  }
  ```
- **Error Responses**:
  - 401: Invalid credentials
  - 400: Invalid request format

### Register
- **Endpoint**: `POST /api/auth/register`
- **Request**:
  ```
  Headers: Content-Type: application/json
  Body: {
    "name": "string (2-50 characters)",
    "email": "string (valid email)",
    "password": "string (min 8 characters)"
  }
  ```
- **Success Response**:
  ```
  Status: 201 Created
  Body: {
    "token": "string (JWT token)",
    "user": {
      "id": "string",
      "name": "string",
      "email": "string",
      "themePreference": "'dark'|'light'"
    }
  }
  ```
- **Error Responses**:
  - 409: Email already registered
  - 400: Invalid request format

### Get Current User
- **Endpoint**: `GET /api/auth/me`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "user": {
      "id": "string",
      "name": "string",
      "email": "string",
      "themePreference": "'dark'|'light'",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

## Task Management Endpoints

### Get All User Tasks
- **Endpoint**: `GET /api/tasks`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  Query Parameters:
    - status: "'all'|'pending'|'completed'" (optional, default: 'all')
    - priority: "'high'|'medium'|'low'|'all'" (optional)
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "description": "string (nullable)",
        "completed": "boolean",
        "priority": "'high'|'medium'|'low'",
        "dueDate": "timestamp (nullable)",
        "createdAt": "timestamp",
        "updatedAt": "timestamp"
      }
    ]
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

### Create Task
- **Endpoint**: `POST /api/tasks`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  Body: {
    "title": "string (1-200 characters)",
    "description": "string (0-1000 characters, optional)",
    "priority": "'high'|'medium'|'low' (optional, default: 'medium')",
    "dueDate": "timestamp (optional)"
  }
  ```
- **Success Response**:
  ```
  Status: 201 Created
  Body: {
    "task": {
      "id": "string",
      "title": "string",
      "description": "string (nullable)",
      "completed": "boolean (default: false)",
      "priority": "'high'|'medium'|'low'",
      "dueDate": "timestamp (nullable)",
      "userId": "string",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token
  - 400: Invalid request format

### Update Task
- **Endpoint**: `PUT /api/tasks/{id}`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  Body: {
    "title": "string (1-200 characters, optional)",
    "description": "string (0-1000 characters, optional)",
    "completed": "boolean (optional)",
    "priority": "'high'|'medium'|'low' (optional)",
    "dueDate": "timestamp (optional)"
  }
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "task": {
      "id": "string",
      "title": "string",
      "description": "string (nullable)",
      "completed": "boolean",
      "priority": "'high'|'medium'|'low'",
      "dueDate": "timestamp (nullable)",
      "userId": "string",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 400: Invalid request format

### Delete Task
- **Endpoint**: `DELETE /api/tasks/{id}`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "success": true,
    "message": "Task deleted successfully"
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token
  - 403: Task does not belong to user
  - 404: Task not found

## Dashboard Endpoints

### Get User Stats
- **Endpoint**: `GET /api/dashboard/stats`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "stats": {
      "total": "number",
      "completed": "number",
      "pending": "number",
      "highPriority": "number",
      "mediumPriority": "number",
      "lowPriority": "number"
    }
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

## Chat Endpoints

### Send Message & Get AI Response
- **Endpoint**: `POST /api/chat/{user_id}`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  Body: {
    "conversation_id": "integer (optional, creates new if not provided)",
    "message": "string (non-empty)"
  }
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "conversation_id": "integer",
    "response": "string (AI-generated response)",
    "tool_calls": "array (list of MCP tools invoked)"
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token
  - 400: Invalid request format

### Get Conversation History
- **Endpoint**: `GET /api/chat/{user_id}/conversations`
- **Request**:
  ```
  Headers: Authorization: Bearer {token}
  ```
- **Success Response**:
  ```
  Status: 200 OK
  Body: {
    "conversations": [
      {
        "id": "integer",
        "title": "string",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    ]
  }
  ```
- **Error Responses**:
  - 401: Invalid or expired token

## Error Response Format
All error responses follow this format:
```
{
  "error": {
    "message": "string (human-readable error message)",
    "code": "string (error code)",
    "details": "object (optional, additional error details)"
  }
}
```