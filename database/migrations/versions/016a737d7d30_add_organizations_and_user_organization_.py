"""add organizations and user organization relationship

Revision ID: 016a737d7d30
Revises: 94cfce8a1f75
Create Date: 2026-08-25 13:05:16.064860

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "016a737d7d30"
down_revision: Union[str, Sequence[str], None] = "94cfce8a1f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create organizations table.
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_organizations_id"),
        "organizations",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_organizations_name"),
        "organizations",
        ["name"],
        unique=True,
    )

    op.create_index(
        op.f("ix_organizations_slug"),
        "organizations",
        ["slug"],
        unique=True,
    )

    # SQLite requires batch mode for adding a foreign key
    # constraint to an existing table.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "organization_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_index(
            op.f("ix_users_organization_id"),
            ["organization_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_users_organization_id_organizations",
            "organizations",
            ["organization_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_users_organization_id_organizations",
            type_="foreignkey",
        )

        batch_op.drop_index(
            op.f("ix_users_organization_id"),
        )

        batch_op.drop_column(
            "organization_id",
        )

    op.drop_index(
        op.f("ix_organizations_slug"),
        table_name="organizations",
    )

    op.drop_index(
        op.f("ix_organizations_name"),
        table_name="organizations",
    )

    op.drop_index(
        op.f("ix_organizations_id"),
        table_name="organizations",
    )

    op.drop_table("organizations")