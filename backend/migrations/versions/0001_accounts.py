"""Account identity, office access and revocable sessions. No runtime identities."""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None


def upgrade():
    op.create_table(
        "accounts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
    )
    op.create_table(
        "memberships",
        sa.Column("account_id", sa.Uuid(), sa.ForeignKey("accounts.id"), primary_key=True),
        sa.Column("active", sa.Boolean(), nullable=False),
    )
    op.create_table(
        "grants",
        sa.Column(
            "account_id", sa.Uuid(), sa.ForeignKey("memberships.account_id"), primary_key=True
        ),
        sa.Column("role", sa.String(32), primary_key=True),
        sa.CheckConstraint("role IN ('administrator', 'menu_maintainer')"),
    )
    op.create_table(
        "installation",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.CheckConstraint("id = 1"),
    )
    op.create_table(
        "login_sessions",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("account_id", sa.Uuid(), sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("csrf_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_login_sessions_account_id", "login_sessions", ["account_id"])


def downgrade():
    for table in ["login_sessions", "installation", "grants", "memberships", "accounts"]:
        op.drop_table(table)
