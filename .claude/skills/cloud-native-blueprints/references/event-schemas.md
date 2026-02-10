# Event Schemas Reference

Versioned event schema definitions for cloud-native applications with Todo app examples.

## Schema Versioning

All events follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible with previous version)
- **MINOR**: New fields added (backward compatible)
- **PATCH**: Bug fixes, documentation

## Base Event Structure

All events share this base structure:

```yaml
event_id: string (uuid)           # Unique event identifier
event_type: string                # Event type (e.g., "task.created")
schema_version: string            # Schema version (e.g., "1.0.0")
timestamp: string (ISO 8601)      # Event timestamp in UTC
correlation_id: string (uuid)     # For tracing related events
causation_id: string (uuid)       # Event that caused this event
source: string                    # Service that produced the event
data: object                      # Event-specific payload
metadata: object                  # Optional metadata
```

## Todo App Event Schemas

### task.created (v1.0.0)

Task creation event.

```yaml
event_type: "task.created"
schema_version: "1.0.0"
data:
  task_id: string (uuid, required)
  title: string (max 200 chars, required)
  description: string (optional)
  status: enum ["pending", "in_progress", "completed"]
  priority: enum ["low", "medium", "high"]
  tags: array of strings (optional)
  due_date: string (ISO 8601 date, optional)
  created_by: string (user_id, required)
  created_at: string (ISO 8601, required)
```

**Example**:
```json
{
  "event_id": "evt_001",
  "event_type": "task.created",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T10:00:00Z",
  "correlation_id": "corr_abc",
  "causation_id": null,
  "source": "todo-api",
  "data": {
    "task_id": "task_123",
    "title": "Complete Phase V deployment",
    "description": "Deploy Todo app to OKE with Dapr and Redpanda",
    "status": "pending",
    "priority": "high",
    "tags": ["hackathon", "phase5", "cloud"],
    "due_date": "2026-02-18",
    "created_by": "user_456",
    "created_at": "2026-02-07T10:00:00Z"
  },
  "metadata": {
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### task.updated (v1.0.0)

Task update event with change tracking.

```yaml
event_type: "task.updated"
schema_version: "1.0.0"
data:
  task_id: string (uuid, required)
  changes: object (required)
    field: string
    old_value: any
    new_value: any
  updated_by: string (user_id, required)
  updated_at: string (ISO 8601, required)
```

**Example**:
```json
{
  "event_id": "evt_002",
  "event_type": "task.updated",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T11:30:00Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_001",
  "source": "todo-api",
  "data": {
    "task_id": "task_123",
    "changes": [
      {
        "field": "status",
        "old_value": "pending",
        "new_value": "in_progress"
      },
      {
        "field": "priority",
        "old_value": "high",
        "new_value": "medium"
      }
    ],
    "updated_by": "user_456",
    "updated_at": "2026-02-07T11:30:00Z"
  }
}
```

### task.completed (v1.0.0)

Task completion event.

```yaml
event_type: "task.completed"
schema_version: "1.0.0"
data:
  task_id: string (uuid, required)
  completed_by: string (user_id, required)
  completed_at: string (ISO 8601, required)
  duration_seconds: integer (optional)
```

**Example**:
```json
{
  "event_id": "evt_003",
  "event_type": "task.completed",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T15:00:00Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_002",
  "source": "todo-api",
  "data": {
    "task_id": "task_123",
    "completed_by": "user_456",
    "completed_at": "2026-02-07T15:00:00Z",
    "duration_seconds": 18000
  }
}
```

### task.deleted (v1.0.0)

Task deletion event (soft delete).

```yaml
event_type: "task.deleted"
schema_version: "1.0.0"
data:
  task_id: string (uuid, required)
  deleted_by: string (user_id, required)
  deleted_at: string (ISO 8601, required)
  reason: string (optional)
```

**Example**:
```json
{
  "event_id": "evt_004",
  "event_type": "task.deleted",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-08T09:00:00Z",
  "correlation_id": "corr_xyz",
  "source": "todo-api",
  "data": {
    "task_id": "task_456",
    "deleted_by": "user_789",
    "deleted_at": "2026-02-08T09:00:00Z",
    "reason": "Duplicate task"
  }
}
```

### task.assigned (v1.1.0)

Task assignment event (added in v1.1.0).

```yaml
event_type: "task.assigned"
schema_version: "1.1.0"
data:
  task_id: string (uuid, required)
  assigned_to: string (user_id, required)
  assigned_by: string (user_id, required)
  assigned_at: string (ISO 8601, required)
  previous_assignee: string (user_id, optional)  # New in 1.1.0
  message: string (optional)                     # New in 1.1.0
```

**Example**:
```json
{
  "event_id": "evt_005",
  "event_type": "task.assigned",
  "schema_version": "1.1.0",
  "timestamp": "2026-02-07T10:15:00Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_001",
  "source": "todo-api",
  "data": {
    "task_id": "task_123",
    "assigned_to": "user_789",
    "assigned_by": "user_456",
    "assigned_at": "2026-02-07T10:15:00Z",
    "previous_assignee": null,
    "message": "You have the expertise for this"
  }
}
```

### notification.sent (v1.0.0)

Notification delivery event.

```yaml
event_type: "notification.sent"
schema_version: "1.0.0"
data:
  notification_id: string (uuid, required)
  user_id: string (uuid, required)
  channel: enum ["email", "sms", "push", "in_app"]
  template: string (required)
  context: object (template variables)
  sent_at: string (ISO 8601, required)
  status: enum ["sent", "failed"]
```

**Example**:
```json
{
  "event_id": "evt_006",
  "event_type": "notification.sent",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T10:00:15Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_001",
  "source": "notification-service",
  "data": {
    "notification_id": "notif_001",
    "user_id": "user_456",
    "channel": "email",
    "template": "task_created",
    "context": {
      "task_title": "Complete Phase V deployment",
      "task_link": "https://todo.app/tasks/task_123"
    },
    "sent_at": "2026-02-07T10:00:15Z",
    "status": "sent"
  }
}
```

### task.reminder_scheduled (v1.0.0)

Reminder scheduling event (used with Dapr Jobs API).

```yaml
event_type: "task.reminder_scheduled"
schema_version: "1.0.0"
data:
  task_id: string (uuid, required)
  reminder_id: string (uuid, required)
  user_id: string (uuid, required)
  scheduled_for: string (ISO 8601, required)
  reminder_type: enum ["due_date", "custom", "recurring"]
  recurrence: object (optional)
    pattern: string (cron expression)
    end_date: string (ISO 8601, optional)
  created_at: string (ISO 8601, required)
```

**Example**:
```json
{
  "event_id": "evt_007",
  "event_type": "task.reminder_scheduled",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T10:01:00Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_001",
  "source": "todo-api",
  "data": {
    "task_id": "task_123",
    "reminder_id": "rem_001",
    "user_id": "user_456",
    "scheduled_for": "2026-02-17T09:00:00Z",
    "reminder_type": "due_date",
    "recurrence": null,
    "created_at": "2026-02-07T10:01:00Z"
  }
}
```

### task.reminder_triggered (v1.0.0)

Reminder execution event.

```yaml
event_type: "task.reminder_triggered"
schema_version: "1.0.0"
data:
  reminder_id: string (uuid, required)
  task_id: string (uuid, required)
  user_id: string (uuid, required)
  triggered_at: string (ISO 8601, required)
  next_occurrence: string (ISO 8601, optional)
```

**Example**:
```json
{
  "event_id": "evt_008",
  "event_type": "task.reminder_triggered",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-17T09:00:00Z",
  "correlation_id": "corr_abc",
  "causation_id": "evt_007",
  "source": "reminder-service",
  "data": {
    "reminder_id": "rem_001",
    "task_id": "task_123",
    "user_id": "user_456",
    "triggered_at": "2026-02-17T09:00:00Z",
    "next_occurrence": null
  }
}
```

## Analytics Events

### task.analytics_recorded (v1.0.0)

Analytics aggregation event.

```yaml
event_type: "task.analytics_recorded"
schema_version: "1.0.0"
data:
  metric_type: enum ["created", "completed", "overdue", "reassigned"]
  task_id: string (uuid, required)
  user_id: string (uuid, required)
  timestamp: string (ISO 8601, required)
  aggregation_period: enum ["hourly", "daily", "weekly", "monthly"]
  dimensions: object
```

**Example**:
```json
{
  "event_id": "evt_009",
  "event_type": "task.analytics_recorded",
  "schema_version": "1.0.0",
  "timestamp": "2026-02-07T15:00:00Z",
  "source": "analytics-service",
  "data": {
    "metric_type": "completed",
    "task_id": "task_123",
    "user_id": "user_456",
    "timestamp": "2026-02-07T15:00:00Z",
    "aggregation_period": "hourly",
    "dimensions": {
      "priority": "high",
      "tags": ["hackathon", "phase5"],
      "duration_seconds": 18000
    }
  }
}
```

## Schema Evolution

### Version 1.0.0 → 1.1.0 Example

Added `previous_assignee` and `message` to `task.assigned`:

**Consumer handling both versions**:

```python
def handle_task_assigned(event):
    version = event.get('schema_version', '1.0.0')
    data = event['data']
    
    # Always present
    task_id = data['task_id']
    assigned_to = data['assigned_to']
    
    # New in 1.1.0
    if version >= '1.1.0':
        previous_assignee = data.get('previous_assignee')
        message = data.get('message')
    else:
        previous_assignee = None
        message = None
    
    process_assignment(task_id, assigned_to, previous_assignee, message)
```

## Validation Schemas

### JSON Schema for task.created

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TaskCreatedEvent",
  "type": "object",
  "required": ["event_id", "event_type", "schema_version", "timestamp", "source", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    },
    "event_type": {
      "type": "string",
      "const": "task.created"
    },
    "schema_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "source": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "required": ["task_id", "title", "status", "priority", "created_by", "created_at"],
      "properties": {
        "task_id": {
          "type": "string",
          "pattern": "^task_[a-zA-Z0-9]+$"
        },
        "title": {
          "type": "string",
          "maxLength": 200,
          "minLength": 1
        },
        "description": {
          "type": "string"
        },
        "status": {
          "type": "string",
          "enum": ["pending", "in_progress", "completed"]
        },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high"]
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "due_date": {
          "type": "string",
          "format": "date"
        },
        "created_by": {
          "type": "string"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    }
  }
}
```

## Event Publishing (Dapr)

### Python Example

```python
from dapr.clients import DaprClient
import uuid
from datetime import datetime

def publish_task_created(task_data):
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "task.created",
        "schema_version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "correlation_id": str(uuid.uuid4()),
        "causation_id": None,
        "source": "todo-api",
        "data": task_data,
        "metadata": {}
    }
    
    with DaprClient() as client:
        client.publish_event(
            pubsub_name='kafka-pubsub',
            topic_name='todo-events',
            data=event,
            data_content_type='application/json'
        )
```

## Event Consuming (Dapr)

### Python Example

```python
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub_name='kafka-pubsub', topic='todo-events')
async def handle_todo_event(event):
    event_type = event.get('event_type')
    schema_version = event.get('schema_version')
    
    # Route to appropriate handler
    if event_type == 'task.created':
        if schema_version >= '1.0.0':
            await handle_task_created_v1(event)
    elif event_type == 'task.updated':
        await handle_task_updated(event)
    elif event_type == 'task.completed':
        await handle_task_completed(event)
    
    return {'success': True}
```

## Best Practices

1. **Always include schema_version** - Enables safe evolution
2. **Use correlation_id** - Track related events
3. **Use causation_id** - Build event chains
4. **Validate at boundaries** - Validate on publish and consume
5. **Version carefully** - Follow semantic versioning
6. **Document changes** - Maintain changelog
7. **Support multiple versions** - Consumers handle old and new
8. **Keep schemas backward compatible** - Don't break consumers
9. **Use enums for fixed values** - Prevent typos
10. **Include timestamps** - Always use ISO 8601 UTC

## Event Schema Registry

Consider using a schema registry for production:
- **Confluent Schema Registry** (with Kafka/Redpanda)
- **Azure Schema Registry**
- **AWS Glue Schema Registry**

Benefits:
- Centralized schema management
- Version control
- Compatibility checking
- Schema evolution tracking