"""
Script to create a task directly in the database by bypassing model issues
"""
import asyncio
from datetime import datetime
import uuid
from sqlalchemy import create_engine, text
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Create a sync engine to execute raw SQL
engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"))

def create_task_raw_sql():
    """Create a task using raw SQL to bypass model issues"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_123"
    title = "New Task Created via Raw SQL"
    description = "This is a new task created directly with raw SQL to bypass model issues"
    
    # Prepare the SQL statement with only the columns that exist in the current schema
    # Based on the error message, we'll try to insert with only the basic columns
    sql = text("""
        INSERT INTO task (id, user_id, title, description, is_completed, priority, created_at, updated_at)
        VALUES (:id, :user_id, :title, :description, :is_completed, :priority, :created_at, :updated_at)
        RETURNING id, title, description, user_id
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, {
                "id": task_id,
                "user_id": user_id,
                "title": title,
                "description": description,
                "is_completed": False,
                "priority": "MEDIUM",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            conn.commit()
            
            row = result.fetchone()
            print(f"Task created successfully with ID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Description: {row[2]}")
            print(f"User ID: {row[3]}")
            
            return row[0]
    except Exception as e:
        print(f"Error creating task with raw SQL: {e}")
        return None

if __name__ == "__main__":
    created_task_id = create_task_raw_sql()
    if created_task_id:
        print(f"\nSuccessfully created task with ID: {created_task_id}")
    else:
        print("\nFailed to create task with raw SQL")