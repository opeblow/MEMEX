from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "006"
down_revision: str | None = "005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS memex")

    op.create_table(
        "agents",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("agent_type", sa.String(100), nullable=False, server_default="custom"),
        sa.Column("model_config", sa.JSON, nullable=True),
        sa.Column("capabilities", sa.JSON, nullable=True),
        sa.Column("memory_scope", sa.String(50), nullable=False, server_default="workspace"),
        sa.Column("permissions", sa.JSON, nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
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
        "agent_workflows",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("agent_id", sa.String(255), nullable=False, index=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="queued"),
        sa.Column("workflow_type", sa.String(100), nullable=False, server_default="manual"),
        sa.Column("input_data", sa.JSON, nullable=True),
        sa.Column("output_data", sa.JSON, nullable=True),
        sa.Column("progress_pct", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_step", sa.String(200), nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("started_at", sa.String(50), nullable=True),
        sa.Column("completed_at", sa.String(50), nullable=True),
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

    op.create_index("ix_agent_workflows_status", "agent_workflows", ["status"], schema="memex")

    op.create_table(
        "task_executions",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("workflow_id", sa.String(255), nullable=True, index=True),
        sa.Column("agent_id", sa.String(255), nullable=False, index=True),
        sa.Column("parent_task_id", sa.String(255), nullable=True, index=True),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("input_data", sa.JSON, nullable=True),
        sa.Column("output_data", sa.JSON, nullable=True),
        sa.Column("started_at", sa.String(50), nullable=True),
        sa.Column("completed_at", sa.String(50), nullable=True),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
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
        "agent_decisions",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("agent_id", sa.String(255), nullable=False, index=True),
        sa.Column("workflow_id", sa.String(255), nullable=True, index=True),
        sa.Column("task_id", sa.String(255), nullable=True, index=True),
        sa.Column("decision_type", sa.String(100), nullable=False),
        sa.Column("input_context", sa.JSON, nullable=True),
        sa.Column("reasoning", sa.Text, nullable=True),
        sa.Column("outcome", sa.JSON, nullable=True),
        sa.Column("confidence", sa.Float, nullable=True),
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
        "agent_observability_events",
        sa.Column("id", sa.UUID(as_uuid=False), primary_key=True),
        sa.Column("project_id", sa.String(255), nullable=False, index=True),
        sa.Column("agent_id", sa.String(255), nullable=True, index=True),
        sa.Column("workflow_id", sa.String(255), nullable=True, index=True),
        sa.Column("task_id", sa.String(255), nullable=True, index=True),
        sa.Column("event_type", sa.String(50), nullable=False, index=True),
        sa.Column("event_name", sa.String(200), nullable=False),
        sa.Column("data", sa.JSON, nullable=True),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("level", sa.String(20), nullable=False, server_default="info"),
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
    op.drop_table("agent_observability_events", schema="memex")
    op.drop_table("agent_decisions", schema="memex")
    op.drop_table("task_executions", schema="memex")
    op.drop_table("agent_workflows", schema="memex")
    op.drop_table("agents", schema="memex")
