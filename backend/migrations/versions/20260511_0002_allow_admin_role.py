"""allow admin role in users constraint

Revision ID: 20260511_0002
Revises: 20260502_0001
Create Date: 2026-05-11 00:02:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260511_0002"
down_revision = "20260502_0001"
branch_labels = None
depends_on = None


CONSTRAINT_NAME = "users_role_check"
UPGRADE_ROLES = ("admin", "judge", "lawyer", "citizen")
DOWNGRADE_ROLES = ("judge", "lawyer", "citizen")


def _replace_users_role_constraint(roles: tuple[str, ...]) -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    existing = bind.execute(
        sa.text(
            """
            select 1
            from pg_constraint c
            join pg_class t on t.oid = c.conrelid
            where t.relname = 'users'
              and c.contype = 'c'
              and c.conname = :constraint_name
            """
        ),
        {"constraint_name": CONSTRAINT_NAME},
    ).scalar()

    if existing:
        op.execute(sa.text(f'alter table users drop constraint "{CONSTRAINT_NAME}"'))

    quoted_roles = ", ".join(f"'{role}'" for role in roles)
    op.execute(
        sa.text(
            f"""
            alter table users
            add constraint "{CONSTRAINT_NAME}"
            check (role in ({quoted_roles}))
            """
        )
    )


def upgrade():
    _replace_users_role_constraint(UPGRADE_ROLES)


def downgrade():
    _replace_users_role_constraint(DOWNGRADE_ROLES)
