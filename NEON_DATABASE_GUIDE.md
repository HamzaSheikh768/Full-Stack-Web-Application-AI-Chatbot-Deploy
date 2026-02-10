# Neon Database Connection and Task Management Guide

## Overview
This document explains how to connect to the Neon database and manage tasks in the Todo application. The application uses Neon PostgreSQL as its database backend, which provides serverless PostgreSQL with smart branching capabilities.

## Database Connection Information

### Connection String
```python
DATABASE_URL = "postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

### Connection Method
The application connects to Neon using SQLAlchemy with the psycopg2 driver:
```python
from sqlalchemy import create_engine

# Convert the connection string to use psycopg2
DATABASE_URL_PS = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
engine = create_engine(DATABASE_URL_PS)
```

## Task Schema in Neon Database

Based on our analysis, the task table has the following schema:

```sql
CREATE TABLE task (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    parent_id VARCHAR,  -- Nullable
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR NOT NULL,  -- Values: 'LOW', 'MEDIUM', 'HIGH'
    tags TEXT[],  -- Array of text tags
    due_date TIMESTAMP,
    remind_at TIMESTAMP,
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
    recurrence_pattern JSONB,  -- Flexible JSON structure for recurrence
    next_due_date TIMESTAMP,
    order_index VARCHAR NOT NULL DEFAULT '0',  -- Required field
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

## Common Issues and Solutions

### Issue 1: Schema Mismatch
**Problem**: The application model expects certain columns that may not exist in the database.
**Solution**: Ensure migrations are properly applied using Alembic:
```bash
cd backend
python -m alembic upgrade head
```

### Issue 2: Required Fields
**Problem**: The `order_index` field is required but may not be included in model definitions.
**Solution**: Always include required fields when inserting records.

## Code Examples

### Connecting to Neon Database
```python
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "your-default-url")

# Create engine with psycopg2 driver
engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"))

def connect_to_neon_database():
    try:
        with engine.connect() as conn:
            # Test the connection
            result = conn.execute(text("SELECT version();"))
            version_info = result.fetchone()
            print(f"Connected to: {version_info[0][:50]}...")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

### Creating a Task
```python
from datetime import datetime
import uuid

def create_task_in_neon(user_id, title, description, priority="MEDIUM"):
    task_id = str(uuid.uuid4())
    
    sql = text("""
        INSERT INTO task (
            id, user_id, title, description, is_completed, priority, 
            order_index, created_at, updated_at
        )
        VALUES (
            :id, :user_id, :title, :description, :is_completed, 
            :priority, :order_index, :created_at, :updated_at
        )
        RETURNING id, title, user_id
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, {
                "id": task_id,
                "user_id": user_id,
                "title": title,
                "description": description,
                "is_completed": False,
                "priority": priority,
                "order_index": "0",  # Required field
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            conn.commit()
            row = result.fetchone()
            
            print(f"Task created: {row[0]} - {row[1]}")
            return row[0]
    except Exception as e:
        print(f"Error creating task: {e}")
        return None
```

### Retrieving Tasks
```python
def get_tasks_from_neon(user_id):
    sql = text("""
        SELECT id, title, description, is_completed, priority, created_at
        FROM task
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT 10
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, {"user_id": user_id})
            rows = result.fetchall()
            
            tasks = []
            for row in rows:
                task = {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "is_completed": row[3],
                    "priority": row[4],
                    "created_at": row[5]
                }
                tasks.append(task)
            
            return tasks
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return []
```

### Updating a Task
```python
def update_task_in_neon(task_id, **updates):
    # Build dynamic update query
    set_clauses = []
    params = {"task_id": task_id}
    
    for field, value in updates.items():
        if value is not None:
            set_clauses.append(f"{field} = :{field}")
            params[field] = value
    
    if not set_clauses:
        print("No updates provided")
        return False
    
    # Always update the timestamp
    set_clauses.append("updated_at = :updated_at")
    params["updated_at"] = datetime.utcnow()
    
    sql = text(f"UPDATE task SET {', '.join(set_clauses)} WHERE id = :task_id")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, params)
            conn.commit()
            
            if result.rowcount > 0:
                print(f"Task {task_id} updated successfully")
                return True
            else:
                print("Task not found")
                return False
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
```

## Best Practices for Neon Database Usage

1. **Connection Management**:
   - Use connection pooling in production
   - Handle connection errors gracefully
   - Close connections properly

2. **Environment Variables**:
   - Store the database URL in environment variables
   - Never hardcode credentials in source code

3. **Migration Management**:
   - Always run migrations when deploying
   - Test migrations in a development branch first
   - Use Neon's branching feature for testing

4. **Error Handling**:
   - Implement retry logic for transient failures
   - Log database errors for debugging
   - Provide user-friendly error messages

## Environment Setup

For local development, set these environment variables:

```bash
export DATABASE_URL="postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
export BETTER_AUTH_SECRET="your-secret-key"
```

## Troubleshooting

### Common Connection Issues
- **SSL Mode Problems**: Ensure SSL parameters are correctly set in the connection string
- **Rate Limiting**: Neon has connection limits; implement proper connection pooling
- **Branch Switching**: Make sure you're connecting to the correct branch

### Schema Issues
- Run `python -m alembic upgrade head` to apply pending migrations
- Check that your model definitions match the actual database schema
- Use raw SQL for complex operations that bypass ORM limitations

## Conclusion

The Neon database provides a robust, serverless PostgreSQL solution for the Todo application. By following the patterns outlined in this document, you can effectively manage tasks and other data in your application while taking advantage of Neon's scaling and branching capabilities.