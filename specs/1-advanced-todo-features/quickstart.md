# Quickstart Guide: Advanced Todo Features

**Date**: 2026-02-08
**Feature**: Advanced Todo Features
**Spec**: [spec.md](./spec.md)

## Overview

This quickstart guide provides a rapid introduction to implementing the advanced todo features including priorities, tags, search/filter, sort, recurring tasks, and due dates & reminders. The guide follows the AGENTS.md constitution for Phase V, emphasizing Dapr abstractions, event-driven architecture, and cloud-native deployment patterns.

## Prerequisites

- Python 3.13+ installed
- Next.js 16+ with App Router
- Neon Serverless PostgreSQL account
- Better Auth configured
- Dapr runtime installed (for local development)
- Cohere API key
- Docker (for containerization)

## Setup Instructions

### 1. Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL="your_neon_postgres_connection_string"

# Authentication
BETTER_AUTH_SECRET="your_jwt_secret_here"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"

# Cohere API
COHERE_API_KEY="your_cohere_api_key"

# Dapr Configuration
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001

# Application
NEXTAUTH_URL="http://localhost:3000"
NODE_ENV="development"
```

### 2. Database Schema Extension

Extend your existing Task model with the new fields:

```python
# backend/models.py
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import enum

class PriorityLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Advanced features
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    tags: Optional[List[str]] = Field(default=None)
    due_at: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[dict] = Field(default=None)
    next_due_date: Optional[datetime] = None
```

### 3. Run Database Migration

Apply the schema changes to your database:

```bash
# Run this command to update your database schema
alembic revision --autogenerate -m "Add advanced todo features"
alembic upgrade head
```

### 4. Extend MCP Tools

Update your MCP tools to support the new features:

```python
# backend/mcp/tools.py
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class AddTaskParams(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = []
    due_at: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[dict] = None

class ListTasksParams(BaseModel):
    user_id: str
    status: Optional[str] = "all"
    priority: Optional[str] = None
    tags: Optional[List[str]] = []
    search: Optional[str] = None
    sort_by: Optional[str] = "due_at"
    sort_order: Optional[str] = "asc"
```

### 5. Dapr Configuration

Create Dapr component configurations for pub/sub:

```yaml
# dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

## Implementation Steps

### Step 1: Implement Extended MCP Tools

```python
# backend/mcp/task_tools.py
from dapr.ext.grpc import App
from dapr.clients import DaprClient
import json

app = App()

@app.method(name='add_task')
def add_task(request):
    """Add a new task with advanced features"""
    params = request['params']

    # Validate input
    if not params.get('title'):
        raise ValueError("Title is required")

    # Create task with advanced features
    task = {
        'user_id': params['user_id'],
        'title': params['title'],
        'description': params.get('description', ''),
        'priority': params.get('priority', 'medium'),
        'tags': params.get('tags', []),
        'due_at': params.get('due_at'),
        'remind_at': params.get('remind_at'),
        'is_recurring': params.get('is_recurring', False),
        'recurrence_pattern': params.get('recurrence_pattern'),
        'completed': False
    }

    # Save to database
    # ... database save logic

    # Publish event if recurring
    if task['is_recurring']:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name='todo-pubsub',
                topic_name='task-created',
                data=json.dumps(task)
            )

    return {'task_id': task['id'], 'status': 'created', 'title': task['title']}

@app.method(name='list_tasks')
def list_tasks(request):
    """List tasks with advanced filtering and sorting"""
    params = request['params']
    user_id = params['user_id']

    # Build query with filters
    query_filters = {'user_id': user_id}

    if params.get('status') and params['status'] != 'all':
        query_filters['completed'] = params['status'] == 'completed'

    if params.get('priority'):
        query_filters['priority'] = params['priority']

    if params.get('tags'):
        # Filter by tags (implementation depends on your DB structure)
        pass

    if params.get('search'):
        # Full-text search implementation
        pass

    # Apply sorting
    sort_field = params.get('sort_by', 'due_at')
    sort_order = params.get('sort_order', 'asc')

    # Execute query and return results
    # ... database query logic

    return {'tasks': tasks, 'total': len(tasks)}

# Implement other tools similarly...
```

### Step 2: Update Cohere Integration

Configure your Cohere agent to use the extended tools:

```python
# backend/services/cohere_service.py
import cohere
from typing import Dict, Any

class CohereService:
    def __init__(self, api_key: str):
        self.client = cohere.Client(api_key)

    def process_message(self, message: str, user_id: str, tools: list) -> Dict[str, Any]:
        """Process user message with Cohere and return tool calls"""

        response = self.client.chat(
            model='command-r-plus',
            message=message,
            tools=tools,
            temperature=0.3
        )

        return {
            'response': response.text,
            'tool_calls': response.tool_calls if hasattr(response, 'tool_calls') else []
        }

# Define your tools for Cohere
COHERE_TOOLS = [
    {
        "name": "add_task",
        "description": "Create a new task with advanced features",
        "parameter_definitions": {
            "user_id": {"type": "str", "required": True},
            "title": {"type": "str", "required": True},
            "description": {"type": "str", "required": False},
            "priority": {"type": "str", "required": False, "default": "medium"},
            "tags": {"type": "list", "required": False},
            "due_at": {"type": "str", "required": False},
            "remind_at": {"type": "str", "required": False},
            "is_recurring": {"type": "bool", "required": False}
        }
    },
    # Add other tools...
]
```

### Step 3: Implement Event-Driven Architecture

Set up consumers for task events:

```python
# backend/services/event_consumer.py
import asyncio
import json
from datetime import datetime
from dapr.ext.grpc import App

app = App()

@app.subscribe(pubsub_name='todo-pubsub', topic='task-completed')
async def handle_task_completed(event_data: bytes):
    """Handle task completion events"""
    data = json.loads(event_data.decode('utf-8'))

    if data.get('is_recurring'):
        # Generate next occurrence
        await generate_next_occurrence(data)

@app.subscribe(pubsub_name='todo-pubsub', topic='reminder-due')
async def handle_reminder_due(event_data: bytes):
    """Handle reminder due events"""
    data = json.loads(event_data.decode('utf-8'))

    # Trigger notification
    await send_notification(data['user_id'], f"Reminder: {data['title']}")

async def generate_next_occurrence(task_data: dict):
    """Generate the next occurrence of a recurring task"""
    # Calculate next due date based on recurrence pattern
    next_date = calculate_next_occurrence(
        task_data['recurrence_pattern'],
        task_data['next_due_date']
    )

    if next_date and not recurrence_ended(task_data['recurrence_pattern']):
        # Create new task instance
        new_task = {
            **task_data,
            'id': None,  # New ID
            'completed': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'due_at': next_date,
            'next_due_date': calculate_next_occurrence(task_data['recurrence_pattern'], next_date)
        }

        # Save to database
        # ... save logic
```

### Step 4: Update Frontend Components

Update your Next.js components to support new features:

```tsx
// frontend/components/TaskForm.tsx
'use client';

import { useState } from 'react';
import { PriorityLevel } from '@/types/task';

interface TaskFormData {
  title: string;
  description?: string;
  priority: PriorityLevel;
  tags: string[];
  dueAt?: string;
  remindAt?: string;
  isRecurring: boolean;
  recurrencePattern?: any;
}

export default function TaskForm() {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    priority: 'medium',
    tags: [],
    isRecurring: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const response = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      // Handle success
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Task title"
        value={formData.title}
        onChange={(e) => setFormData({...formData, title: e.target.value})}
        required
      />

      {/* Priority selector */}
      <select
        value={formData.priority}
        onChange={(e) => setFormData({...formData, priority: e.target.value as PriorityLevel})}
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      {/* Tags input */}
      <div>
        <input
          type="text"
          placeholder="Add tag"
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              const tag = (e.target as HTMLInputElement).value.trim();
              if (tag && !formData.tags.includes(tag)) {
                setFormData({
                  ...formData,
                  tags: [...formData.tags, tag]
                });
                (e.target as HTMLInputElement).value = '';
              }
            }
          }}
        />
        <div className="tags">
          {formData.tags.map((tag, index) => (
            <span key={index} onClick={() => {
              setFormData({
                ...formData,
                tags: formData.tags.filter((_, i) => i !== index)
              });
            }}>
              {tag} ×
            </span>
          ))}
        </div>
      </div>

      {/* Due date picker */}
      <input
        type="datetime-local"
        value={formData.dueAt || ''}
        onChange={(e) => setFormData({...formData, dueAt: e.target.value})}
      />

      {/* Recurring task toggle */}
      <label>
        <input
          type="checkbox"
          checked={formData.isRecurring}
          onChange={(e) => setFormData({...formData, isRecurring: e.target.checked})}
        />
        Recurring task
      </label>

      <button type="submit">Add Task</button>
    </form>
  );
}
```

## Running the Application

### Local Development

1. Start Dapr:
```bash
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python backend/main.py
```

2. Run the backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Run the frontend:
```bash
cd frontend
npm install
npm run dev
```

### Testing the Features

Try these sample commands with the chatbot:
- "Add a high priority task to buy groceries with tags shopping and food"
- "Show me all pending tasks with high priority"
- "List tasks due this week sorted by priority"
- "Create a recurring task to water plants every Tuesday"

## Deployment to OKE

1. Build Docker images:
```bash
# Use Gordon AI agent for Dockerfile generation
gordon generate dockerfile --context ./backend --output ./backend/Dockerfile
gordon generate dockerfile --context ./frontend --output ./frontend/Dockerfile
```

2. Create Helm charts using kubectl-ai:
```bash
kubectl-ai "generate helm chart for todo application"
```

3. Deploy to OKE:
```bash
helm install todo-app ./charts/todo-app --namespace todo-app --create-namespace
```

## Troubleshooting

### Common Issues

1. **Dapr not starting**: Ensure Dapr runtime is installed with `dapr init`
2. **Cohere API errors**: Verify your API key and check rate limits
3. **Database connection**: Confirm your Neon PostgreSQL connection string is correct
4. **Authentication failures**: Check that Better Auth is properly configured

### Useful Commands

```bash
# Check Dapr status
dapr status -k

# View logs
dapr logs todo-backend

# Check service invocation
dapr invoke --app-id todo-backend --method healthz

# Test MCP tools directly
curl -d '{"user_id":"test", "title":"Test task"}' \
  -H "Content-Type: application/json" \
  -X POST http://localhost:3500/v1.0/invoke/todo-backend/method/tasks
```

## Next Steps

1. Implement the complete event-driven architecture for recurring tasks
2. Add comprehensive error handling and validation
3. Set up monitoring and observability with Dapr
4. Optimize database queries for search and filter operations
5. Add proper testing for all new features