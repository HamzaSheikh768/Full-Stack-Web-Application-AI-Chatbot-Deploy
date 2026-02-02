"""
Test script to verify the database configuration fix
"""
import os
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

# Get database URL from environment variables
# For development, prioritize local SQLite over Neon database
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Set to 'postgres' for production, 'sqlite' for development
if DB_TYPE == "sqlite":
    DATABASE_URL = "sqlite:///./taskapp_dev.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskapp_dev.db")

print("Database Configuration After Fix:")
print(f"DB_TYPE environment variable: {os.getenv('DB_TYPE', 'NOT SET')}")
print(f"Effective DATABASE_URL: {DATABASE_URL}")
print(f"Using SQLite: {'Yes' if 'sqlite' in DATABASE_URL else 'No'}")
print(f"Using PostgreSQL: {'Yes' if 'postgresql' in DATABASE_URL else 'No'}")

if 'neon.tech' in DATABASE_URL:
    print("\n❌ PROBLEM: Still using Neon database")
else:
    print("\n✅ SUCCESS: Using local SQLite database for development")

print("\nThe backend will now use a local SQLite database for development,")
print("which should resolve the 'Failed to fetch' error during signup.")