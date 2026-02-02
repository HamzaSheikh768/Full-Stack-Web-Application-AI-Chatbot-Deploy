#!/usr/bin/env python3
"""
Direct script to add 3 test users to the SQLite database
This bypasses the import issues with the async database setup
"""
import sqlite3
import uuid
import hashlib
import time
from datetime import datetime


def hash_password_sync(password):
    """Synchronous password hashing function"""
    # Using a simple hash for the test - in production, use bcrypt
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def add_test_users_to_db():
    """Add 3 test users directly to the SQLite database"""
    print("Adding test users directly to SQLite database...")

    # Connect to the existing database
    conn = sqlite3.connect('taskapp_dev.db')
    cursor = conn.cursor()

    # Define test users
    test_users = [
        {
            "email": "user1@example.com",
            "password": "SecurePass123!",
            "first_name": "Admin",
            "last_name": "User"
        },
        {
            "email": "user2@example.com",
            "password": "SecurePass123!",
            "first_name": "Regular",
            "last_name": "User"
        },
        {
            "email": "user3@example.com",
            "password": "SecurePass123!",
            "first_name": "Guest",
            "last_name": "User"
        }
    ]

    # Import bcrypt here to make sure it's available
    import bcrypt

    for user_data in test_users:
        # Check if user already exists
        cursor.execute("SELECT id FROM user WHERE email = ?", (user_data["email"],))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"User {user_data['email']} already exists, skipping...")
            continue

        # Hash the password
        password_hash = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user record with actual table structure
        user_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        updated_at = created_at

        cursor.execute("""
            INSERT INTO user (id, email, first_name, last_name, password_hash, created_at, updated_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            user_data["email"],
            user_data["first_name"],
            user_data["last_name"],
            password_hash,
            created_at,
            updated_at,
            1  # is_active = True
        ))

        print(f"Added user: {user_data['email']} ({user_data['first_name']} {user_data['last_name']})")

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Test users added successfully!")


if __name__ == "__main__":
    add_test_users_to_db()