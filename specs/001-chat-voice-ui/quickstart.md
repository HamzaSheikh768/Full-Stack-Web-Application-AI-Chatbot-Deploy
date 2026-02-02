# Quickstart: Chat API, Voice Input & UI Navigation

**Feature**: Chat API, Voice Input & UI Navigation
**Branch**: 001-chat-voice-ui

## Prerequisites

1. **Environment Variables**
   Ensure `.env` contains:
   ```bash
   COHERE_API_KEY=your_cohere_key_here
   DATABASE_URL=postgresql://user:pass@host/db
   BETTER_AUTH_SECRET=your_better_auth_secret
   ```

2. **Database Migration**
   Apply the SQLModel schema:
   ```bash
   alembic upgrade head
   ```

## Running the Service

### 1. Start the Backend Server
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

## Testing the Chat API

### 1. Test Chat Endpoint
Send a message to the AI assistant:

```bash
curl -X POST http://localhost:8000/api/your_user_id/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{
    "message": "Add a task to buy milk"
  }'
```

**Expected Response**:
```json
{
  "conversation_id": 123,
  "response": "Sure, I've added 'Buy milk' to your task list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "your_user_id",
        "title": "Buy milk"
      },
      "result": {
        "id": 456,
        "user_id": "your_user_id",
        "title": "Buy milk",
        "completed": false,
        "created_at": "2023-01-01T00:00:00"
      }
    }
  ]
}
```

### 2. Test Conversation Continuation
Continue the conversation by including the conversation_id:

```bash
curl -X POST http://localhost:8000/api/your_user_id/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{
    "message": "Show my tasks",
    "conversation_id": 123
  }'
```

## Voice Input Testing

1. Navigate to the AI Chat page in your browser (usually at `/chat`)
2. Click the microphone button in the chat interface
3. Speak a command like "Add a task to call mom"
4. The system should convert your speech to text and process it

## UI Navigation

1. **Navbar Access**: Look for the "AI Chat" button in the top navigation bar on any authenticated page
2. **Sidebar Access**: In the sidebar, there should be an "AI Chat" link alongside Dashboard and Tasks
3. **Chat Page**: The AI Chat page will display conversation history and provide both text and voice input options

## Troubleshooting

- **401 Unauthorized**: Verify your JWT token is valid and included in the Authorization header
- **500 Error**: Check that `COHERE_API_KEY` is properly set in your environment
- **Voice Input Not Working**: Ensure you're using a supported browser (Chrome, Edge, Safari) and have granted microphone permissions
- **No Real-time Updates**: Verify that your frontend is properly listening for state changes when tasks are updated via AI