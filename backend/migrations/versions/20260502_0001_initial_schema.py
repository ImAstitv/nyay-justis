"""initial schema

Revision ID: 20260502_0001
Revises:
Create Date: 2026-05-02 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260502_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("username", sa.String(), nullable=False, unique=True),
            sa.Column("password_hash", sa.String(), nullable=False),
            sa.Column("role", sa.String(), nullable=False),
            sa.Column("full_name", sa.String(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    if "cases" not in existing_tables:
        op.create_table(
            "cases",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("cnr_number", sa.String(), nullable=True, unique=True),
            sa.Column("status", sa.String(), nullable=False, server_default="Active"),
            sa.Column("case_type", sa.String(), nullable=True, server_default="General"),
            sa.Column("petitioner", sa.String(), nullable=True),
            sa.Column("respondent", sa.String(), nullable=True),
            sa.Column("citizen_username", sa.String(), nullable=True),
            sa.Column("filed_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
            sa.Column("under_acts", sa.String(), nullable=True),
            sa.Column("under_sections", sa.String(), nullable=True),
            sa.Column("filing_date", sa.DateTime(), nullable=False),
            sa.Column("first_hearing_date", sa.DateTime(), nullable=True),
            sa.Column("current_stage", sa.String(), nullable=True, server_default="Pre-Trial"),
            sa.Column("establishment_code", sa.String(), nullable=True, server_default="BRPA20"),
            sa.Column("primary_case_nature", sa.String(), nullable=True, server_default="Civil"),
            sa.Column("custody_status", sa.String(), nullable=True, server_default="None"),
            sa.Column("immediate_risk", sa.String(), nullable=True, server_default="None"),
            sa.Column("financial_stake", sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column("estimated_severity", sa.String(), nullable=True, server_default="Low"),
            sa.Column("is_undertrial", sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column("days_in_custody", sa.Integer(), nullable=True, server_default="0"),
            sa.Column("priority_score", sa.Float(), nullable=True, server_default="0"),
            sa.Column("aging_factor", sa.Float(), nullable=True, server_default="0"),
            sa.Column("friction_index", sa.Integer(), nullable=True, server_default="0"),
            sa.Column("vulnerability", sa.Float(), nullable=True, server_default="1.0"),
            sa.Column("stage_coeff", sa.Float(), nullable=True, server_default="1.0"),
            sa.Column("omega_flag", sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )
    else:
        case_columns = {column["name"] for column in inspector.get_columns("cases")}
        if "status" not in case_columns:
            op.add_column("cases", sa.Column("status", sa.String(), nullable=True, server_default="Active"))
        if "citizen_username" not in case_columns:
            op.add_column("cases", sa.Column("citizen_username", sa.String(), nullable=True))
        if "filed_by_user_id" not in case_columns:
            op.add_column("cases", sa.Column("filed_by_user_id", sa.Integer(), nullable=True))

    if "hearings" not in existing_tables:
        op.create_table(
            "hearings",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=True),
            sa.Column("judge_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
            sa.Column("business_on_date", sa.DateTime(), nullable=True),
            sa.Column("next_hearing_date", sa.DateTime(), nullable=True),
            sa.Column("purpose_of_hearing", sa.String(), nullable=True),
            sa.Column("adjournment_reason", sa.String(), nullable=True),
            sa.Column("adjourned_by", sa.String(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    if "audit_log" not in existing_tables:
        op.create_table(
            "audit_log",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("case_id", sa.Integer(), sa.ForeignKey("cases.id"), nullable=True),
            sa.Column("action", sa.String(), nullable=True),
            sa.Column("performed_by_role", sa.String(), nullable=True),
            sa.Column("old_value", sa.Text(), nullable=True),
            sa.Column("new_value", sa.Text(), nullable=True),
            sa.Column("detail", sa.JSON(), nullable=True),
            sa.Column("timestamp", sa.DateTime(), nullable=True),
        )


def downgrade():
    op.drop_table("audit_log")
    op.drop_table("hearings")
    op.drop_table("cases")
    op.drop_table("users")
