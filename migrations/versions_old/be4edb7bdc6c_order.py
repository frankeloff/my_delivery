"""order

Revision ID: be4edb7bdc6c
Revises: 972ede974775
Create Date: 2022-09-02 18:07:24.449785

"""
from tokenize import String

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be4edb7bdc6c"
down_revision = "972ede974775"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "order",
        sa.Column("order_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("status", sa.String()),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("chef_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["client.client_id"]),
        sa.ForeignKeyConstraint(),
        sa.PrimaryKeyConstraint("order_id"),
    )

    op.create_table(
        "order_details",
        sa.Column("order_details_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["order_id"]),
        sa.PrimaryKeyConstraint("order_details_id"),
    )


def downgrade() -> None:
    op.drop_table("order")
    op.drop_table("order_details")
