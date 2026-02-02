import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
from src.models import User, Task, Session  # Import your models

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

# Add the parent directory to the path so we can import from db module
sys.path.append(str(Path(__file__).parent.parent))

# Get database URL from environment variables (similar to what's in db.py)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

# Convert async URL to sync for Alembic since it doesn't support async engines directly
# Replace async drivers with sync equivalents
import re
sync_database_url = re.sub(r'\+asyncpg', '+psycopg2', DATABASE_URL)
sync_database_url = re.sub(r'\+aiomysql', '+pymysql', sync_database_url)
sync_database_url = re.sub(r'\+aiosqlite', '+sqlite', sync_database_url)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL from environment variables
config.set_main_option('sqlalchemy.url', sync_database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_sync_migrations():
    from sqlalchemy import create_engine
    import re

    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise ValueError("sqlalchemy.url configuration is not set")

    # Convert async URL to sync for Alembic since it doesn't support async engines directly
    # Replace async drivers with sync equivalents
    sync_url = re.sub(r'\+asyncpg', '+psycopg2', url)
    sync_url = re.sub(r'\+aiomysql', '+pymysql', sync_url)
    sync_url = re.sub(r'\+aiosqlite', '+sqlite', sync_url)

    connectable = create_engine(sync_url)

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    run_sync_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()