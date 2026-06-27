"""Add auth tables (organizations, verification_tokens, password_reset_tokens)

Revision ID: 002
Revises: 001
Create Date: 2026-06-27
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email_verified", sa.Boolean(), server_default="false", nullable=False), schema="memex")
    op.add_column("users", sa.Column("is_onboarded", sa.Boolean(), server_default="false", nullable=False), schema="memex")

    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), unique=True, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("avatar_url", sa.String(1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        schema="memex",
    )

    op.create_table(
        "organization_members",
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="member"),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("organization_id", "user_id"),
        schema="memex",
    )

    op.create_table(
        "verification_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("token", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("type", sa.String(50), nullable=False, server_default="email_verification"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_used", sa.Boolean(), server_default="false", nullable=False),
        schema="memex",
    )


def downgrade() -> None:
    op.drop_table("verification_tokens", schema="memex")
    op.drop_table("organization_members", schema="memex")
    op.drop_table("organizations", schema="memex")
