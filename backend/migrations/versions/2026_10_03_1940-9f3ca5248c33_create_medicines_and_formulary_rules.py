"""create medicines and formulary rules

Revision ID: 9f3ca5248c33
Revises:
Create Date: 2026-10-03 19:40:28.207882

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9f3ca5248c33"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the btree_gist extension for exclusion constraints
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    # Create the new tables
    op.create_table(
        "medicines",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("form", sa.Text(), nullable=False),
        sa.Column("strength_value", sa.Numeric(), nullable=False),
        sa.Column("strength_unit", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_medicines")),
        sa.UniqueConstraint("code", name=op.f("uq_medicines_code")),
        sa.CheckConstraint("code <> ''", name=op.f("ck_medicines_code_not_empty")),
        sa.CheckConstraint("name <> ''", name=op.f("ck_medicines_name_not_empty")),
        sa.CheckConstraint("form <> ''", name=op.f("ck_medicines_form_not_empty")),
        sa.CheckConstraint(
            "strength_unit <> ''", name=op.f("ck_medicines_strength_unit_not_empty")
        ),
        sa.CheckConstraint(
            "strength_value > 0", name=op.f("ck_medicines_strength_value_positive")
        ),
    )
    op.create_table(
        "formulary_rules",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column(
            "medicine_id",
            sa.BigInteger(),
            sa.ForeignKey("medicines.id"),
            nullable=False,
        ),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("max_quantity_per_dispense", sa.Numeric(10, 2), nullable=False),
        sa.Column("max_quantity_per_30_days", sa.Numeric(10, 2), nullable=False),
        sa.Column(
            "requires_authorisation",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_formulary_rules")),
        sa.CheckConstraint(
            "effective_to >= effective_from",
            name=op.f("ck_formulary_rules_period_valid"),
        ),
        sa.CheckConstraint(
            "max_quantity_per_dispense > 0",
            name=op.f("ck_formulary_rules_max_quantity_per_dispense_positive"),
        ),
        sa.CheckConstraint(
            "max_quantity_per_30_days > 0",
            name=op.f("ck_formulary_rules_max_quantity_per_30_days_positive"),
        ),
        sa.CheckConstraint(
            "max_quantity_per_dispense <= max_quantity_per_30_days",
            name=op.f("ck_formulary_rules_max_qty_lte_max_per_30_days"),
        ),
        postgresql.ExcludeConstraint(
            ("medicine_id", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            using="gist",
            name=op.f("ex_formulary_rules_no_overlap"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("formulary_rules")
    op.drop_table("medicines")
    op.execute("DROP EXTENSION IF EXISTS btree_gist")
