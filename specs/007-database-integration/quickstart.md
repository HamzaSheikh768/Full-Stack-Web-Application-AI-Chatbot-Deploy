# Quickstart Guide: Database Integration for Todo AI Chatbot

**Feature**: Database Integration for Todo AI Chatbot
**Branch**: 007-database-integration

## Prerequisites

1. **Environment Variables**
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `COHERE_API_KEY`: Cohere API key for AI functionality
   - `BETTER_AUTH_SECRET`: Better Auth secret for JWT

2. **Database Setup**
   - Ensure Neon PostgreSQL database is created and accessible
   - Run database migrations before starting the service

## Setup Instructions

### 1. Database Migration
```bash
# Run migrations to create required tables
cd backend
alembic upgrade head
```

### 2. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Verify Database Connection
```bash
# Test database connectivity
cd backend
python -c "from src.database.db import engine; print('Database connection successful')"
```

## API Usage

### Chat Endpoint
```bash
# Send a message to the AI assistant
curl -X POST http://localhost:8000/api/user_123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": 1
  }'
```

### Expected Response
```json
{
  "conversation_id": 1,
  "response": "I've added 'Buy groceries' to your task list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user_123",
        "title": "Buy groceries"
      },
      "result": {
        "id": 42,
        "user_id": "user_123",
        "title": "Buy groceries",
        "description": null,
        "completed": false,
        "created_at": "2026-01-23T12:00:00Z",
        "updated_at": "2026-01-23T12:00:00Z"
      }
    }
  ]
}
```

## Testing Database Integration

### 1. Test Task Operations
```bash
# Add a task
curl -X POST http://localhost:8000/api/user_123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Add a task to call mom"}'

# List tasks
curl -X POST http://localhost:8000/api/user_123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Show my tasks"}'

# Complete a task
curl -X POST http://localhost:8000/api/user_123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message": "Complete task 1"}'
```

### 2. Verify Data Persistence
Check that all operations are properly stored in the database:
```sql
-- Verify tasks are stored
SELECT * FROM task WHERE user_id = 'user_123';

-- Verify conversations are stored
SELECT * FROM conversation WHERE user_id = 'user_123';

-- Verify messages are stored
SELECT * FROM message WHERE user_id = 'user_123';
```

## Troubleshooting

- **Database Connection Issues**: Verify `DATABASE_URL` is correct and database is accessible
- **User Isolation Failures**: Ensure all queries filter by `user_id` to prevent cross-user data access
- **MCP Tool Failures**: Check that tools validate user ownership before executing operations
- **Cohere API Errors**: Verify `COHERE_API_KEY` is valid and has sufficient quota

## Performance Considerations

- Indexes are created on `user_id` fields for efficient querying
- Connection pooling is configured for Neon Serverless PostgreSQL
- Conversation history is loaded efficiently with proper indexing