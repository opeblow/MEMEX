"""Add sources, import_jobs, memory_versions tables

Revision ID: 005
Revises: 004
Create Date: 2026-06-27 14:00:00.000000
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "005"
down_revision: str | None = "004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS memex")

    op.create_table(
        "sources",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("source_type", sa.String(100), nullable=False),
        sa.Column("display_name", sa.String(500), nullable=True),
        sa.Column("url", sa.Text, nullable=True),
        sa.Column("file_path", sa.Text, nullable=True),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("size_bytes", sa.BigInteger, nullable=True),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column("memory_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_import_at", sa.String(50), nullable=True),
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
        "import_jobs",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("source_id", sa.String(255), nullable=True),
        sa.Column("source_type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="queued"),
        sa.Column("progress_pct", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_step", sa.String(100), nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("total_items", sa.Integer, nullable=False, server_default="0"),
        sa.Column("processed_items", sa.Integer, nullable=False, server_default="0"),
        sa.Column("memory_ids", sa.JSON, nullable=True),
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

    op.create_index("ix_import_jobs_status", "import_jobs", ["status"], schema="memex")

    op.create_table(
        "memory_versions",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("memory_id", sa.String(255), nullable=False, index=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("version_type", sa.String(50), nullable=False),
        sa.Column("content_preview", sa.Text, nullable=True),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("tags", sa.JSON, nullable=True),
        sa.Column("importance", sa.Float, nullable=False, server_default="0.5"),
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


def downgrade() -> None:
    op.drop_table("memory_versions", schema="memex")
    op.drop_table("import_jobs", schema="memex")
    op.drop_table("sources", schema="memex")
