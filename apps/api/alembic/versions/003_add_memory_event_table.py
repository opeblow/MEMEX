"""Add memory_event table for timeline tracking

Revision ID: 003
Revises: 002
Create Date: 2026-06-27
"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "memory_events",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("event_type", sa.String(100), nullable=False, index=True),
        sa.Column("event_data", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        schema="memex",
    )

    op.create_index("ix_memory_events_event_type", "memory_events", ["event_type"], schema="memex")
    op.create_index("ix_memory_events_created_at", "memory_events", ["created_at"], schema="memex")


def downgrade() -> None:
    op.drop_table("memory_events", schema="memex")
