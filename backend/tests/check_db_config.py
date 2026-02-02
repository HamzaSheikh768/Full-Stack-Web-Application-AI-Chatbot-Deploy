"""
Script to check the database configuration being used by the backend
"""
import os
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskapp_dev.db")  # Use SQLite for development by default

print("Database Configuration Check:")
print(f"Environment DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"Effective DATABASE_URL: {DATABASE_URL}")
print(f"Using SQLite: {'Yes' if 'sqlite' in DATABASE_URL else 'No'}")
print(f"Using PostgreSQL: {'Yes' if 'postgresql' in DATABASE_URL else 'No'}")

if 'neon.tech' in DATABASE_URL:
    print("\n⚠️  WARNING: The backend is configured to use Neon database!")
    print("This may cause connection issues during development.")
    print("The backend will try to connect to Neon instead of local SQLite.")

print("\nFor development, it's recommended to use SQLite.")
print("Make sure the backend server can connect to the database before processing requests.")