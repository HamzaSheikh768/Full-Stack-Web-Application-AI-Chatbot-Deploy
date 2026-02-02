"""Add conversation and message tables

Revision ID: 001_add_conversation_message_tables
Revises:
Create Date: 2026-01-23 15:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = '001_add_conversation_message_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_user_id'), 'conversation', ['user_id'], unique=False)

    # Create message table
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.String(length=5000), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'], unique=False)


def downgrade() -> None:
    # Drop message table first (due to foreign key)
    op.drop_index(op.f('ix_message_conversation_id'), table_name='message')
    op.drop_table('message')

    # Drop conversation table
    op.drop_index(op.f('ix_conversation_user_id'), table_name='conversation')
    op.drop_table('conversation')