from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "007"
down_revision: str | None = "006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS memex")

    op.create_table(
        "memory_collections",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_shared", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("metadata", sa.JSON, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "memory_collection_items",
        sa.Column("collection_id", sa.String(255), nullable=False),
        sa.Column("memory_id", sa.String(255), nullable=False),
        sa.Column("added_by", sa.String(255), nullable=False),
        sa.Column("added_at", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("collection_id", "memory_id"),
        schema="memex",
    )

    op.create_table(
        "memory_comments",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("memory_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("parent_id", sa.String(255), nullable=True, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "memory_permissions",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("memory_id", sa.String(255), nullable=True, index=True),
        sa.Column("collection_id", sa.String(255), nullable=True, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("granted_by", sa.String(255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "share_links",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("memory_id", sa.String(255), nullable=True, index=True),
        sa.Column("collection_id", sa.String(255), nullable=True, index=True),
        sa.Column("token", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("permission", sa.String(50), nullable=False, server_default="viewer"),
        sa.Column("expires_at", sa.String(50), nullable=True),
        sa.Column("max_uses", sa.Integer, nullable=True),
        sa.Column("use_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "invitations",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("workspace_id", sa.String(255), nullable=False, index=True),
        sa.Column("invited_by", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("token", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("role", sa.String(50), nullable=False, server_default="viewer"),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("expires_at", sa.String(50), nullable=True),
        sa.Column("accepted_at", sa.String(50), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(255), nullable=True, index=True),
        sa.Column("details", sa.JSON, nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False,
        ),
        schema="memex",
    )

    op.create_index("ix_audit_logs_action", "audit_logs", ["action"], schema="memex")


def downgrade() -> None:
    op.drop_table("audit_logs", schema="memex")
    op.drop_table("invitations", schema="memex")
    op.drop_table("share_links", schema="memex")
    op.drop_table("memory_permissions", schema="memex")
    op.drop_table("memory_comments", schema="memex")
    op.drop_table("memory_collection_items", schema="memex")
    op.drop_table("memory_collections", schema="memex")
