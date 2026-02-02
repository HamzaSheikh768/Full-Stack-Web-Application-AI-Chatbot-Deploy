# Data Model: Chat API, Voice Input & UI Navigation

**Feature**: Chat API, Voice Input & UI Navigation
**Source**: `spec.md` -> Functional Requirements

## 1. Database Entities (SQLModel)

### Conversation
New model to store chat conversations.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique conversation identifier |
| user_id | String | Yes | Index | Owner of the conversation (from Auth) |
| title | String | No | Max 200 chars | Optional summary of the conversation |
| created_at | DateTime | Yes | Default: Now | Timestamp of creation |
| updated_at | DateTime | Yes | Default: Now | Timestamp of last update |

### Message
New model to store individual chat messages.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| id | Integer | Yes | PK, Auto-inc | Unique message identifier |
| conversation_id | Integer | Yes | FK -> Conversation, Index | Associated conversation |
| role | String | Yes | Enum: "user", "assistant" | Who sent the message |
| content | String | Yes | Max 5000 chars | The message text |
| created_at | DateTime | Yes | Default: Now | Timestamp of creation |

## 2. API Contracts (OpenAPI/JSON Schema)

These schemas define the API endpoints for the chat functionality.

### Chat API Endpoint: `POST /api/{user_id}/chat`

**Request Body Schema**:
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "The user's message to the AI assistant",
      "minLength": 1,
      "maxLength": 5000
    },
    "conversation_id": {
      "type": "integer",
      "description": "Optional existing conversation ID (creates new if not provided)",
      "minimum": 1
    }
  },
  "required": ["message"]
}
```

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": "integer",
      "description": "The conversation ID (newly created or existing)"
    },
    "response": {
      "type": "string",
      "description": "The AI assistant's response to the user"
    },
    "tool_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "arguments": {"type": "object"},
          "result": {}
        }
      },
      "description": "List of MCP tools invoked during processing"
    }
  },
  "required": ["conversation_id", "response", "tool_calls"]
}
```

### Web Speech API Integration

The frontend will use the browser's native Web Speech API:
- `webkitSpeechRecognition` for Chrome/Edge
- Standard `SpeechRecognition` where available
- Graceful fallback to text input for unsupported browsers

**Supported Languages**:
- en-US (English - US)
- ur-PK (Urdu - Pakistan)

## 3. UI/Navigation Contracts

### Navbar Component Update
The existing Navbar component will be updated to include:
- "AI Chat" button visible on all authenticated pages
- Navigates to `/chat` route when clicked

### Sidebar Component Update
The existing Sidebar component will be updated to include:
- "AI Chat" option in the navigation list alongside Dashboard and Tasks
- Active state highlighting when on the chat page

### AI Chat Page Component
New page component at `/chat` that includes:
- ChatKit UI for conversation display
- Text input field for typing messages
- Microphone button for voice input
- Real-time display of tool execution confirmations
- Conversation history display

## 4. Real-Time Update Contracts

### Task Updates Propagation
When the AI assistant creates, updates, or deletes tasks:
1. Changes are persisted to the database via MCP tools
2. The Tasks page component should reflect changes without page refresh
3. Dashboard metrics should update to reflect new task status

**Implementation Approach**:
- Use React state management to propagate changes between components
- Potentially implement polling or WebSocket connection for real-time updates (if needed)

## 5. Key Relationships

- **Conversation** (1) ←→ (Many) **Message**: A conversation contains multiple messages
- **User** (1) ←→ (Many) **Conversation**: A user has multiple conversations
- **Message** (1) ←→ (1) **Conversation**: Each message belongs to one conversation