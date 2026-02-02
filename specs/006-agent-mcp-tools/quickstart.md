# Quickstart: Agent & MCP Tools

**Feature**: Agent & MCP Tools for Todo AI Chatbot
**Branch**: 006-agent-mcp-tools

## Prerequisites

1. **Environment Variables**
   Ensure `.env` contains:
   ```bash
   COHERE_API_KEY=your_cohere_key_here
   DATABASE_URL=postgresql://user:pass@host/db
   ```

2. **Database Migration**
   Apply the SQLModel schema:
   ```bash
   alembic upgrade head
   ```

## Testing the Agent

Since the agent is stateless, you can test it via the API directly.

### 1. Start the Server
```bash
uvicorn src.main:app --reload
```

### 2. Test Tool Execution (Integration Test)
Send a request that triggers `add_task`:

```bash
curl -X POST http://localhost:8000/api/your_user_id_123/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy milk"
  }'
```

**Expected Response:**
```json
{
  "response": "Sure, I've added 'Buy milk' to your task list.",
  "tool_calls": [
    { "name": "add_task", "arguments": { "title": "Buy milk" } }
  ]
}
```

## Troubleshooting

- **500 Error**: Check `COHERE_API_KEY` validity.
- **Agent hallucinates tools**: Ensure the tool schemas in `mcp-tools.json` are correctly loaded into the Agent definition.
- **DB Permission Error**: Check if `user_id` is propagated to the DB query filters.
