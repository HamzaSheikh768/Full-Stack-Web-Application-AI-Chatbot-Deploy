"""
Script to verify the task exists in the database
"""
import asyncio
from datetime import datetime
from sqlalchemy import create_engine, text
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Create a sync engine to execute raw SQL
engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"))

def verify_task_exists():
    """Verify the task exists in the database"""
    # Query the task we just created
    sql = text("""
        SELECT id, user_id, title, description, is_completed, priority, created_at, updated_at
        FROM task
        WHERE title = 'New Task Created via Raw SQL'
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql)
            row = result.fetchone()
            
            if row:
                print("Task found in database:")
                print(f"  ID: {row[0]}")
                print(f"  User ID: {row[1]}")
                print(f"  Title: {row[2]}")
                print(f"  Description: {row[3]}")
                print(f"  Completed: {row[4]}")
                print(f"  Priority: {row[5]}")
                print(f"  Created At: {row[6]}")
                print(f"  Updated At: {row[7]}")
                
                return True
            else:
                print("Task not found in database")
                return False
    except Exception as e:
        print(f"Error querying task: {e}")
        return False

if __name__ == "__main__":
    success = verify_task_exists()
    if success:
        print("\nTask verification successful!")
    else:
        print("\nTask verification failed!")