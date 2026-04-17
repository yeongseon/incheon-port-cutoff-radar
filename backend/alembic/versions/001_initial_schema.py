"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-04-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "terminals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("terminal_code", sa.String(50), unique=True, nullable=False),
        sa.Column("terminal_name", sa.String(200), nullable=False),
        sa.Column("aliases", sa.Text(), nullable=True),
        sa.Column("gate_open_time", sa.String(10), nullable=True),
        sa.Column("gate_close_time", sa.String(10), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "source_snapshots_terminal_congestion",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("terminal_code", sa.String(50), nullable=False),
        sa.Column("congestion_status", sa.String(50)),
        sa.Column("congestion_time_minutes", sa.Float()),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("normalized_at", sa.DateTime()),
        sa.Column("freshness_status", sa.String(20)),
        sa.Column("raw_payload_json", postgresql.JSON()),
    )
    op.create_index(
        "ix_congestion_terminal_observed",
        "source_snapshots_terminal_congestion",
        ["terminal_code", "observed_at"],
    )

    op.create_table(
        "source_snapshots_terminal_operation",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("terminal_code", sa.String(50), nullable=False),
        sa.Column("available_time", sa.DateTime()),
        sa.Column("expected_arrival_applied", sa.Boolean()),
        sa.Column("raw_status_note", sa.Text()),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("normalized_at", sa.DateTime()),
        sa.Column("freshness_status", sa.String(20)),
        sa.Column("raw_payload_json", postgresql.JSON()),
    )
    op.create_index(
        "ix_operation_terminal_observed",
        "source_snapshots_terminal_operation",
        ["terminal_code", "observed_at"],
    )

    op.create_table(
        "source_snapshots_gate_entry",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("terminal_name", sa.String(200), nullable=False),
        sa.Column("lane_code", sa.String(50)),
        sa.Column("entry_type", sa.String(50)),
        sa.Column("vehicle_count", sa.Integer()),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("normalized_at", sa.DateTime()),
        sa.Column("freshness_status", sa.String(20)),
        sa.Column("raw_payload_json", postgresql.JSON()),
    )
    op.create_index(
        "ix_gate_terminal_observed",
        "source_snapshots_gate_entry",
        ["terminal_name", "observed_at"],
    )

    op.create_table(
        "source_snapshots_traffic",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("route_key", sa.String(100), nullable=False),
        sa.Column("origin_zone_id", sa.String(50)),
        sa.Column("terminal_code", sa.String(50)),
        sa.Column("average_speed_kph", sa.Float()),
        sa.Column("estimated_travel_minutes", sa.Float()),
        sa.Column("congestion_level", sa.String(20)),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("normalized_at", sa.DateTime()),
        sa.Column("freshness_status", sa.String(20)),
        sa.Column("raw_payload_json", postgresql.JSON()),
    )
    op.create_index(
        "ix_traffic_route_observed",
        "source_snapshots_traffic",
        ["route_key", "observed_at"],
    )

    op.create_table(
        "dispatch_evaluations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("evaluation_id", sa.String(50), unique=True, nullable=False),
        sa.Column("origin_zone_id", sa.String(50), nullable=False),
        sa.Column("terminal_code", sa.String(50), nullable=False),
        sa.Column("cut_off_at", sa.DateTime(), nullable=False),
        sa.Column("conservative_mode", sa.Boolean(), server_default="false"),
        sa.Column("manual_buffer_minutes", sa.Integer()),
        sa.Column("result_status", sa.String(20), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(10), nullable=False),
        sa.Column("on_time_probability", sa.Float(), nullable=False),
        sa.Column("latest_safe_dispatch_at", sa.DateTime()),
        sa.Column("estimated_total_minutes", sa.Integer(), nullable=False),
        sa.Column("verdict", sa.Text(), nullable=False),
        sa.Column("engine_version", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_eval_created", "dispatch_evaluations", ["created_at"])
    op.create_index(
        "ix_eval_terminal_created",
        "dispatch_evaluations",
        ["terminal_code", "created_at"],
    )

    op.create_table(
        "dispatch_reason_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "dispatch_evaluation_id",
            sa.Integer(),
            sa.ForeignKey("dispatch_evaluations.id"),
            nullable=False,
        ),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("contribution_percent", sa.Integer(), nullable=False),
        sa.Column("impact_minutes", sa.Float(), nullable=False),
        sa.Column("direction", sa.String(20), nullable=False),
        sa.Column("display_order", sa.Integer(), server_default="0"),
        sa.Column("summary", sa.Text(), nullable=False),
    )

    op.create_table(
        "dispatch_evaluation_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "dispatch_evaluation_id",
            sa.Integer(),
            sa.ForeignKey("dispatch_evaluations.id"),
            nullable=False,
        ),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("snapshot_id", sa.Integer()),
        sa.Column("freshness_seconds", sa.Integer()),
        sa.Column("used_fallback", sa.Boolean(), server_default="false"),
    )


def downgrade() -> None:
    op.drop_table("dispatch_evaluation_sources")
    op.drop_table("dispatch_reason_items")
    op.drop_table("dispatch_evaluations")
    op.drop_table("source_snapshots_traffic")
    op.drop_table("source_snapshots_gate_entry")
    op.drop_table("source_snapshots_terminal_operation")
    op.drop_table("source_snapshots_terminal_congestion")
    op.drop_table("terminals")
