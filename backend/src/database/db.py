from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, NullPool
from sqlmodel import SQLModel
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")

print(f"DEBUG: DATABASE_URL = {DATABASE_URL}")

# For async engine with asyncpg for async operations
# Remove channel_binding parameter as it's not supported by asyncpg
if "channel_binding=" in DATABASE_URL:
    import re
    DATABASE_URL = re.sub(r'[&?]?channel_binding=[^&]*', '', DATABASE_URL)
    # Ensure proper query separator
    if "?" not in DATABASE_URL and "&" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("&", "?", 1)

# Remove any problematic parameters that might cause DNS resolution issues
if "?sslmode=require" in DATABASE_URL:
    # For Neon, we might need to adjust SSL parameters
    pass

# Additional fix for Neon connection issues - remove channel_binding if present
if "channel_binding=" in DATABASE_URL:
    import re
    # Remove channel_binding parameter entirely as it's causing SSL issues
    DATABASE_URL = re.sub(r'[&?]channel_binding=[^&]*', '', DATABASE_URL)
    # Clean up any double ?? or ?& that might have been created
    DATABASE_URL = DATABASE_URL.replace('?&', '?').replace('??', '?')
    # Ensure proper query separator if we removed the first parameter
    if '?' not in DATABASE_URL and '&' in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace('&', '?', 1)

# Additional fix for Neon - remove unsupported parameters
if "?options=" in DATABASE_URL:
    import re
    DATABASE_URL = re.sub(r'[&?]?options=[^&]*', '', DATABASE_URL)

# Replace postgresql:// with postgresql+asyncpg:// for async compatibility
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1) if DATABASE_URL.startswith("postgresql://") else DATABASE_URL
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1) if ASYNC_DATABASE_URL.startswith("postgres://") else ASYNC_DATABASE_URL

# Sync engine for create_db_and_tables (using psycopg2)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1) if DATABASE_URL.startswith("postgresql://") else DATABASE_URL
SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1) if SYNC_DATABASE_URL.startswith("postgres://") else SYNC_DATABASE_URL

# For Neon, we may need to add specific parameters for better compatibility
if "neon.tech" in ASYNC_DATABASE_URL and "pooler" in ASYNC_DATABASE_URL:
    # Add Neon-specific parameters if not already present
    if "sslmode=" not in ASYNC_DATABASE_URL:
        ASYNC_DATABASE_URL += "&sslmode=require"
    if "connect_timeout=" not in ASYNC_DATABASE_URL:
        ASYNC_DATABASE_URL += "&connect_timeout=10"

if "neon.tech" in SYNC_DATABASE_URL and "pooler" in SYNC_DATABASE_URL:
    # Add Neon-specific parameters if not already present
    if "sslmode=" not in SYNC_DATABASE_URL:
        SYNC_DATABASE_URL += "&sslmode=require"
    if "connect_timeout=" not in SYNC_DATABASE_URL:
        SYNC_DATABASE_URL += "&connect_timeout=10"

# Create async engine for async operations
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    # Neon Serverless optimized settings
    poolclass=NullPool,   # Use NullPool for async engines
    pool_pre_ping=True,   # Verify connections before use (critical for serverless)
    pool_recycle=300,     # Recycle connections to prevent serverless timeout issues
    echo=False            # Set to True for SQL query logging during development
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create sync engine for sync operations like table creation
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    # Neon Serverless optimized settings
    poolclass=QueuePool,
    pool_size=2,          # Small pool for serverless
    max_overflow=5,       # Limited overflow
    pool_pre_ping=True,   # Verify connections before use (critical for serverless)
    pool_recycle=300,     # Recycle connections to prevent serverless timeout issues
    echo=False            # Set to True for SQL query logging during development
)

# Create sync session maker
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

def get_db():
    """Get a sync database session for FastAPI dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_session():
    """Get an async database session for FastAPI dependency injection"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def create_db_and_tables():
    """Create database tables"""
    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(bind=sync_engine)