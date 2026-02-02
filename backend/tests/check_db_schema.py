"""
Check database schema to see if tables are properly created
"""
import sqlite3
import os

def check_db_schema():
    db_path = "taskapp_dev.db"

    if not os.path.exists(db_path):
        print("Database file does not exist!")
        return

    print("Database file exists. Checking schema...")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")

        # Check user table structure if it exists
        if ('user',) in tables:
            cursor.execute("PRAGMA table_info(user)")
            user_columns = cursor.fetchall()
            print("User table columns:")
            for col in user_columns:
                print(f"  - {col[1]} ({col[2]}) - {'' if col[5] == 0 else 'PRIMARY KEY'}")

        # Check task table structure if it exists
        if ('task',) in tables:
            cursor.execute("PRAGMA table_info(task)")
            task_columns = cursor.fetchall()
            print("Task table columns:")
            for col in task_columns:
                print(f"  - {col[1]} ({col[2]}) - {'' if col[5] == 0 else 'PRIMARY KEY'}")

        conn.close()
        print("Database schema check completed.")

    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_db_schema()