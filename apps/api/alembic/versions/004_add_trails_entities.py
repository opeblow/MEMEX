"""Add memory_trails, entities, relationships tables

Revision ID: 004
Revises: 003
Create Date: 2026-06-27 12:00:00.000000
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "004"
down_revision: str | None = "003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS memex")

    op.create_table(
        "memory_trails",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("answer", sa.Text, nullable=True),
        sa.Column("trail_steps", sa.JSON, nullable=True),
        sa.Column("memory_ids", sa.JSON, nullable=True),
        sa.Column("confidence_score", sa.Float, nullable=True),
        sa.Column("processing_time_ms", sa.Integer, nullable=True),
        sa.Column("model_used", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="completed"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "entities",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "relationships",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("source_entity_id", sa.String(255), nullable=False, index=True),
        sa.Column("target_entity_id", sa.String(255), nullable=False, index=True),
        sa.Column("relationship_type", sa.String(100), nullable=False),
        sa.Column("strength", sa.Float, nullable=False, server_default="0.5"),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        schema="memex",
    )

    op.create_index("ix_relationships_source_entity", "relationships", ["source_entity_id"], schema="memex")
    op.create_index("ix_relationships_target_entity", "relationships", ["target_entity_id"], schema="memex")
    op.create_index("ix_entities_name", "entities", ["name"], schema="memex")


def downgrade() -> None:
    op.drop_table("relationships", schema="memex")
    op.drop_table("entities", schema="memex")
    op.drop_table("memory_trails", schema="memex")
