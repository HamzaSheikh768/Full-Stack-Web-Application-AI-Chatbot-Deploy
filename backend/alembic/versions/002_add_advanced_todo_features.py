"""Add advanced todo features

Revision ID: 002_adv_features
Revises: 001_conv_msg_tables
Create Date: 2026-02-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_adv_features'
down_revision = '001_conv_msg_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add new columns for advanced todo features"""

    # Add tags column (PostgreSQL array)
    op.add_column('task', sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True))

    # Add remind_at column
    op.add_column('task', sa.Column('remind_at', sa.DateTime(), nullable=True))

    # Add is_recurring column
    op.add_column('task', sa.Column('is_recurring', sa.Boolean(), nullable=False, server_default='false'))

    # Add recurrence_pattern column (JSONB for flexible structure)
    op.add_column('task', sa.Column('recurrence_pattern', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Add next_due_date column
    op.add_column('task', sa.Column('next_due_date', sa.DateTime(), nullable=True))

    # Create indexes for performance
    op.create_index('idx_task_tags', 'task', ['tags'], postgresql_using='gin')
    op.create_index('idx_task_remind_at', 'task', ['remind_at'])
    op.create_index('idx_task_is_recurring', 'task', ['is_recurring'])
    op.create_index('idx_task_next_due_date', 'task', ['next_due_date'])
    op.create_index('idx_task_due_date', 'task', ['due_date'])

    # Create full-text search indexes for title and description
    op.execute("""
        CREATE INDEX idx_task_title_tsv ON task USING GIN(to_tsvector('english', title));
    """)
    op.execute("""
        CREATE INDEX idx_task_description_tsv ON task USING GIN(to_tsvector('english', COALESCE(description, '')));
    """)


def downgrade() -> None:
    """Remove advanced todo features columns"""

    # Drop indexes
    op.execute("DROP INDEX IF EXISTS idx_task_description_tsv;")
    op.execute("DROP INDEX IF EXISTS idx_task_title_tsv;")
    op.drop_index('idx_task_next_due_date', table_name='task')
    op.drop_index('idx_task_is_recurring', table_name='task')
    op.drop_index('idx_task_remind_at', table_name='task')
    op.drop_index('idx_task_due_date', table_name='task')
    op.drop_index('idx_task_tags', table_name='task', postgresql_using='gin')

    # Drop columns
    op.drop_column('task', 'next_due_date')
    op.drop_column('task', 'recurrence_pattern')
    op.drop_column('task', 'is_recurring')
    op.drop_column('task', 'remind_at')
    op.drop_column('task', 'tags')
