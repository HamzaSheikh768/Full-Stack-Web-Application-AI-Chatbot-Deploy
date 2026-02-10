"""
Neon Database Connection and Task Management Example
This script demonstrates how to connect to the Neon database and manage tasks
"""
import os
from sqlalchemy import create_engine, text
from datetime import datetime
import uuid

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Create a sync engine to connect to Neon database
engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"))

def connect_to_neon_database():
    """
    Connect to the Neon database and verify the connection
    """
    try:
        with engine.connect() as conn:
            # Test the connection with a simple query
            result = conn.execute(text("SELECT version();"))
            version_info = result.fetchone()
            print("[SUCCESS] Successfully connected to Neon database!")
            print(f"Database version: {version_info[0][:50]}...")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Neon database: {e}")
        return False

def create_task_in_neon(user_id, title, description, priority="MEDIUM"):
    """
    Create a task in the Neon database using raw SQL
    """
    task_id = str(uuid.uuid4())
    
    # Insert task with all required fields to match the actual database schema
    sql = text("""
        INSERT INTO task (
            id, user_id, title, description, is_completed, priority, 
            order_index, created_at, updated_at
        )
        VALUES (
            :id, :user_id, :title, :description, :is_completed, 
            :priority, :order_index, :created_at, :updated_at
        )
        RETURNING id, title, user_id, created_at
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
                "order_index": "0",  # Required field in the actual schema
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            conn.commit()
            
            row = result.fetchone()
            print(f"[SUCCESS] Task created successfully!")
            print(f"   ID: {row[0]}")
            print(f"   Title: {row[1]}")
            print(f"   User ID: {row[2]}")
            print(f"   Created: {row[3]}")
            
            return row[0]
    except Exception as e:
        print(f"[ERROR] Error creating task: {e}")
        return None

def get_tasks_from_neon(user_id):
    """
    Retrieve tasks for a specific user from the Neon database
    """
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
            
            print(f"[INFO] Found {len(rows)} tasks for user {user_id}:")
            for i, row in enumerate(rows, 1):
                print(f"  {i}. {row[1]} (ID: {row[0]}, Priority: {row[4]}, Completed: {row[3]})")
            
            return rows
    except Exception as e:
        print(f"[ERROR] Error retrieving tasks: {e}")
        return []

def update_task_in_neon(task_id, title=None, description=None, is_completed=None):
    """
    Update a task in the Neon database
    """
    # Build dynamic update query
    updates = []
    params = {"task_id": task_id}
    
    if title is not None:
        updates.append("title = :title")
        params["title"] = title
        
    if description is not None:
        updates.append("description = :description")
        params["description"] = description
        
    if is_completed is not None:
        updates.append("is_completed = :is_completed")
        params["is_completed"] = is_completed
    
    if not updates:
        print("[WARNING] No updates provided")
        return False
    
    updates.append("updated_at = :updated_at")
    params["updated_at"] = datetime.utcnow()
    
    sql = text(f"UPDATE task SET {', '.join(updates)} WHERE id = :task_id RETURNING id, title, is_completed")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, params)
            conn.commit()
            
            row = result.fetchone()
            if row:
                print(f"[SUCCESS] Task updated successfully!")
                print(f"   ID: {row[0]}")
                print(f"   Title: {row[1]}")
                print(f"   Completed: {row[2]}")
                return True
            else:
                print("[ERROR] Task not found")
                return False
    except Exception as e:
        print(f"[ERROR] Error updating task: {e}")
        return False

def delete_task_from_neon(task_id):
    """
    Delete a task from the Neon database
    """
    sql = text("DELETE FROM task WHERE id = :task_id RETURNING id")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(sql, {"task_id": task_id})
            conn.commit()
            
            row = result.fetchone()
            if row:
                print(f"[SUCCESS] Task {row[0]} deleted successfully!")
                return True
            else:
                print("[ERROR] Task not found")
                return False
    except Exception as e:
        print(f"[ERROR] Error deleting task: {e}")
        return False

def main():
    """
    Main function demonstrating Neon database operations
    """
    print("Neon Database Connection and Task Management Demo")
    print("="*60)
    
    # 1. Connect to Neon database
    if not connect_to_neon_database():
        return
    
    print()
    
    # 2. Create a sample task
    user_id = "sample_user_123"
    task_id = create_task_in_neon(
        user_id=user_id,
        title="Sample Task from Neon Connection Demo",
        description="This task was created using direct Neon database connection",
        priority="HIGH"
    )
    
    if not task_id:
        print("Failed to create task, exiting...")
        return
    
    print()
    
    # 3. Retrieve tasks for the user
    get_tasks_from_neon(user_id)
    
    print()
    
    # 4. Update the task
    update_task_in_neon(
        task_id=task_id,
        title="Updated Sample Task from Neon Connection Demo",
        is_completed=True
    )
    
    print()
    
    # 5. Retrieve tasks again to see the update
    get_tasks_from_neon(user_id)
    
    print()
    
    # 6. Show how to use environment variables for connection
    print("Environment Variables Setup:")
    print("For production use, set these environment variables:")
    print(f"export DATABASE_URL='{DATABASE_URL}'")
    print("export BETTER_AUTH_SECRET='your-secret-key'")
    print()
    
    print("Tips for Neon Database:")
    print("- Neon provides serverless PostgreSQL with smart branching")
    print("- Connections are pooled and managed automatically")
    print("- Use connection pooling in production applications")
    print("- Always handle connection errors gracefully")
    print("- Monitor your connection usage in the Neon dashboard")
    
    print()
    print("Neon database operations completed successfully!")

if __name__ == "__main__":
    main()