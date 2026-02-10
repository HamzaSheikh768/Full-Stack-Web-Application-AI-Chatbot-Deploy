---
name: dapr-jobs-reminders
description: Dapr Jobs API for scheduled tasks, recurring jobs, and due-date reminders in cloud-native applications. Use when implementing scheduled background jobs, task reminders, recurring tasks, cron-like scheduling, or time-based automation with Dapr. Covers Dapr Jobs API configuration, reminder patterns, scheduling workflows, and integration with event-driven architectures for Todo applications.
---

# Dapr Jobs & Reminders

Implement scheduled tasks and reminders using Dapr Jobs API.

## Overview

Dapr Jobs API provides reliable scheduling for:
- **One-time jobs** - Execute once at a specific time
- **Recurring jobs** - Repeat on a schedule (cron-like)
- **Reminders** - Due date notifications and alerts
- **Background tasks** - Scheduled data processing

## Core Pattern – Due Date Reminder

1. When task with due date is created/updated → schedule Job
2. Dapr fires HTTP callback at due time
3. Callback publishes "reminder" event via Dapr Pub/Sub

## Prerequisites

Dapr runtime installed on Kubernetes cluster. See `oci-oke-deployment` or other cluster deployment skills.

## Core Workflows

### 1. Schedule One-Time Job

Schedule a task reminder to trigger once:

```python
from dapr.clients import DaprClient
from datetime import datetime, timedelta

# Schedule reminder 1 day before due date
due_date = datetime(2026, 2, 18, 9, 0, 0)
reminder_time = due_date - timedelta(days=1)

with DaprClient() as client:
    client.schedule_job(
        job_name=f"task-reminder-{task_id}",
        schedule=reminder_time.isoformat(),
        data={
            "task_id": task_id,
            "reminder_type": "due_date",
            "message": "Task due tomorrow"
        }
    )
```

### 2. Schedule Recurring Job

Create recurring task (e.g., daily standup reminder):

```python
# Every day at 9 AM
client.schedule_job(
    job_name="daily-standup-reminder",
    schedule="0 9 * * *",  # Cron expression
    repeats=True,
    data={
        "reminder_type": "recurring",
        "message": "Daily standup in 15 minutes"
    }
)
```

### 3. Handle Job Execution

Implement job handler in your service:

```python
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

app = FastAPI()
dapr_app = DaprApp(app)

@app.post('/job/task-reminder')
async def handle_task_reminder(job_data: dict):
    task_id = job_data['task_id']
    message = job_data['message']
    
    # Send notification
    await send_notification(task_id, message)
    
    # Publish event
    with DaprClient() as client:
        client.publish_event(
            pubsub_name='kafka-pubsub',
            topic_name='todo-events',
            data={
                'event_type': 'task.reminder_triggered',
                'task_id': task_id
            }
        )
    
    return {'status': 'completed'}
```

### 4. Cancel Scheduled Job

Remove a scheduled reminder:

```python
client.delete_job(job_name=f"task-reminder-{task_id}")
```

## Todo App Reminder Patterns

### Pattern 1: Due Date Reminder

Remind user 24 hours before task due date:

```python
async def create_task_with_reminder(task_data):
    # Create task
    task = await save_task(task_data)
    
    # Schedule reminder if due date exists
    if task.due_date:
        reminder_time = task.due_date - timedelta(days=1)
        
        with DaprClient() as client:
            client.schedule_job(
                job_name=f"due-date-{task.id}",
                schedule=reminder_time.isoformat(),
                data={
                    "task_id": task.id,
                    "type": "due_date",
                    "message": f"Task '{task.title}' due tomorrow"
                }
            )
    
    return task
```

### Pattern 2: Recurring Task Reminder

Daily reminder for recurring tasks:

```python
async def create_recurring_task(task_data):
    task = await save_task(task_data)
    
    # Schedule daily reminder at 9 AM
    with DaprClient() as client:
        client.schedule_job(
            job_name=f"recurring-{task.id}",
            schedule="0 9 * * *",
            repeats=True,
            data={
                "task_id": task.id,
                "type": "recurring",
                "message": f"Recurring: {task.title}"
            }
        )
    
    return task
```

### Pattern 3: Overdue Task Check

Daily job to check for overdue tasks:

```python
# Schedule daily at midnight
client.schedule_job(
    job_name="check-overdue-tasks",
    schedule="0 0 * * *",
    repeats=True,
    data={"job_type": "overdue_check"}
)

# Handler
@app.post('/job/check-overdue-tasks')
async def check_overdue_tasks(job_data: dict):
    overdue_tasks = await get_overdue_tasks()
    
    for task in overdue_tasks:
        await send_overdue_notification(task)
        
        # Publish event
        publish_event('task.overdue', {'task_id': task.id})
    
    return {'processed': len(overdue_tasks)}
```

## Cron Schedule Examples

Common cron expressions for reminders:

```python
# Every day at 9 AM
"0 9 * * *"

# Every Monday at 10 AM
"0 10 * * 1"

# Every hour
"0 * * * *"

# Every 15 minutes
"*/15 * * * *"

# First day of month at 8 AM
"0 8 1 * *"

# Weekdays at 5 PM
"0 17 * * 1-5"
```

## Integration with Events

Combine jobs with event-driven architecture:

```python
# When task created → schedule reminder
@dapr_app.subscribe(pubsub_name='kafka-pubsub', topic='todo-events')
async def handle_task_created(event):
    if event['event_type'] == 'task.created':
        task_data = event['data']
        
        if task_data.get('due_date'):
            # Schedule reminder
            await schedule_due_date_reminder(task_data)

# When task completed → cancel reminder
@dapr_app.subscribe(pubsub_name='kafka-pubsub', topic='todo-events')
async def handle_task_completed(event):
    if event['event_type'] == 'task.completed':
        task_id = event['data']['task_id']
        
        # Cancel reminder
        with DaprClient() as client:
            client.delete_job(job_name=f"due-date-{task_id}")
```

## Configuration

Dapr Jobs uses a state store for persistence:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: jobs-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis:6379
  - name: actorStateStore
    value: "true"
```

## Error Handling

Handle job execution failures:

```python
@app.post('/job/task-reminder')
async def handle_task_reminder(job_data: dict):
    try:
        await send_notification(job_data)
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Job failed: {e}")
        
        # Retry logic (Dapr handles automatic retries)
        raise  # Will be retried by Dapr
```

## Monitoring

Track job execution:

```python
from prometheus_client import Counter, Histogram

jobs_executed = Counter('dapr_jobs_executed_total', 'Jobs executed', ['job_type'])
job_duration = Histogram('dapr_job_duration_seconds', 'Job duration', ['job_type'])

@app.post('/job/task-reminder')
async def handle_task_reminder(job_data: dict):
    with job_duration.labels(job_type='task_reminder').time():
        await process_reminder(job_data)
        jobs_executed.labels(job_type='task_reminder').inc()
```

## Reference Files

- `jobs-api-patterns.md` - Complete Jobs API patterns and examples

## Best Practices

1. **Use unique job names** - Include task ID or timestamp
2. **Handle idempotency** - Jobs may execute multiple times
3. **Set appropriate TTL** - Clean up old jobs
4. **Monitor execution** - Track success/failure rates
5. **Cancel when not needed** - Delete jobs when tasks completed
6. **Use cron for recurring** - Reliable scheduling
7. **Handle time zones** - Store times in UTC
8. **Validate schedules** - Ensure cron expressions are valid
9. **Combine with events** - Trigger jobs from events
10. **Test thoroughly** - Verify job execution timing

## Integration with Other Skills

- Use `cloud-native-blueprints` for event schemas
- Use `kafka-redpanda-dapr` for event streaming
- Use `oci-oke-deployment` for OKE deployment