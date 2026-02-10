"""
Script to manually add missing columns to the task table in Neon database
"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_dQxI6bev8yCq@ep-wispy-salad-adnoqxlk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
engine = create_engine(DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"))

def add_missing_columns():
    """Add missing columns to the task table"""
    try:
        with engine.connect() as conn:
            # Add tags column (PostgreSQL array)
            print("Adding tags column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS tags TEXT[]"))
            
            # Add remind_at column
            print("Adding remind_at column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS remind_at TIMESTAMP"))
            
            # Add is_recurring column
            print("Adding is_recurring column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE"))
            
            # Add recurrence_pattern column (JSONB for flexible structure)
            print("Adding recurrence_pattern column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern JSONB"))
            
            # Add next_due_date column
            print("Adding next_due_date column...")
            conn.execute(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS next_due_date TIMESTAMP"))
            
            # Update the status column to is_completed if it exists but with wrong name
            # Check if status column exists (old name) and is_completed doesn't exist
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'task' AND column_name = 'status'
            """))
            status_col_exists = result.fetchone() is not None
            
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'task' AND column_name = 'is_completed'
            """))
            is_completed_col_exists = result.fetchone() is not None
            
            if status_col_exists and not is_completed_col_exists:
                print("Renaming status column to is_completed...")
                conn.execute(text("ALTER TABLE task RENAME COLUMN status TO is_completed"))
            
            # Commit the changes
            conn.commit()
            print("All missing columns added successfully!")
            
            # Verify the columns were added
            print("\nVerifying columns...")
            result = conn.execute(text("""
                SELECT column_name, data_type
                FROM information_schema.columns 
                WHERE table_name = 'task'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            print("Current columns in task table:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
                
    except Exception as e:
        print(f"Error adding columns: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_missing_columns()