# Dapr Jobs API Patterns

Advanced patterns for scheduled tasks and reminders.

## Pattern 1: Reminder System

```python
class ReminderService:
    def __init__(self):
        self.dapr_client = DaprClient()
    
    async def schedule_reminder(self, task_id, reminder_time, message):
        job_name = f"reminder-{task_id}-{int(reminder_time.timestamp())}"
        
        self.dapr_client.schedule_job(
            job_name=job_name,
            schedule=reminder_time.isoformat(),
            data={
                "task_id": task_id,
                "message": message,
                "scheduled_at": datetime.utcnow().isoformat()
            }
        )
        
        return job_name
    
    async def cancel_reminder(self, job_name):
        self.dapr_client.delete_job(job_name=job_name)
```

## Pattern 2: Recurring Task System

```python
class RecurringTaskService:
    async def create_recurring_task(self, task_data):
        # Save task
        task = await db.tasks.create(task_data)
        
        # Schedule recurring job
        with DaprClient() as client:
            client.schedule_job(
                job_name=f"recurring-{task.id}",
                schedule=task.recurrence_pattern,  # Cron expression
                repeats=True,
                data={
                    "task_id": task.id,
                    "recurrence": task.recurrence_pattern
                }
            )
        
        return task
```

## Pattern 3: Batch Processing

```python
# Daily batch job for analytics
@app.post('/job/daily-analytics')
async def process_daily_analytics(job_data: dict):
    # Process yesterday's data
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    tasks = await get_tasks_for_date(yesterday)
    analytics = await compute_analytics(tasks)
    
    await save_analytics(analytics)
    
    # Publish event
    publish_event('analytics.computed', analytics)
```

See SKILL.md for more patterns.