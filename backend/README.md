# Todo AI Chatbot Backend

Backend service for the Todo AI Chatbot application using FastAPI, SQLModel, and Cohere AI integration.

## Architecture

The backend consists of:
- **FastAPI** endpoints for API communication
- **SQLModel** for database models and ORM operations
- **Cohere AI Agent** for natural language processing
- **MCP (Model Context Protocol)** tools for task management
- **Neon Serverless PostgreSQL** for data persistence

## API Endpoints

### Chat API

#### POST `/api/{user_id}/chat`
Process user messages through the AI assistant.

**Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "message": "string",
  "conversation_id": "number (optional)"
}
```

**Response**:
```json
{
  "conversation_id": "number",
  "response": "string",
  "tool_calls": "array"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/user_123/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": 1
  }'
```

## MCP Tools

The backend exposes the following tools for the AI agent:

### Task Management Tools

- `add_task`: Create a new task
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark a task as completed
- `delete_task`: Permanently remove a task
- `update_task`: Modify task title or description

## Environment Variables

Create a `.env` file in the backend root with the following variables:

```bash
# Cohere API Key (required for AI functionality)
COHERE_API_KEY=your_cohere_api_key_here

# Database URL for Neon PostgreSQL
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

```

## Database Models

### Task
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique task identifier |
| user_id | String | Owner of the task |
| title | String | Task summary (max 200 chars) |
| description | String | Optional details (max 1000 chars) |
| completed | Boolean | Completion status |
| created_at | DateTime | Timestamp of creation |
| updated_at | DateTime | Timestamp of last update |

### Conversation
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique conversation identifier |
| user_id | String | Owner of the conversation |
| title | String | Optional conversation summary |
| created_at | DateTime | Timestamp of creation |
| updated_at | DateTime | Timestamp of last update |

### Message
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique message identifier |
| conversation_id | Integer | Associated conversation |
| user_id | String | Sender of the message |
| role | String | "user" or "assistant" |
| content | String | Message text content |
| created_at | DateTime | Timestamp of creation |

## Running the Backend

### Prerequisites
- Python 3.11+
- pip

### Installation
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file

5. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## Testing

Run the backend tests with pytest:
```bash
cd backend
pytest tests/
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── models/              # SQLModel database models
│   │   ├── task.py          # Task model
│   │   ├── conversation.py  # Conversation/Message models
│   │   └── user.py          # User model
│   ├── api/                 # API route definitions
│   │   └── chat_routes.py   # Chat endpoint
│   ├── mcp/                 # MCP tools implementation
│   │   ├── tools.py         # Tool definitions
│   │   ├── handlers.py      # Tool implementations
│   │   └── server.py        # MCP server configuration
│   ├── agent/               # AI Agent integration
│   │   ├── core.py          # Agent configuration
│   │   └── runner.py        # Agent execution logic
│   ├── database/            # Database connection setup
│   │   └── db.py            # Database engine and session
│   └── services/            # Business logic
│       └── chat_service.py  # Chat-specific services
├── tests/                   # Backend tests
│   └── test_chat_api.py     # Chat API integration tests
├── requirements.txt         # Python dependencies
├── alembic.ini              # Database migration config
└── README.md               # This file
```