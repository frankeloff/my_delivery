"""init db

Revision ID: 972ede974775
Revises:
Create Date: 2022-09-01 15:59:51.827165

"""
import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "972ede974775"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "client",
        sa.Column("client_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("name", sa.String()),
        sa.Column("email", sa.String(), unique=True),
        sa.Column("password", sa.String()),
        sa.Column("created_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.Column("updated_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.PrimaryKeyConstraint("client_id"),
    )

    op.create_table(
        "supplier",
        sa.Column("supplier_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("name", sa.String()),
        sa.Column("password", sa.String()),
        sa.Column("busy", sa.Boolean, default=False),
        sa.Column("number_of_orders", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.Column("updated_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.PrimaryKeyConstraint("supplier_id"),
    )

    op.create_table(
        "chef",
        sa.Column("chef_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("name", sa.String()),
        sa.Column("password", sa.String()),
        sa.Column("busy", sa.Boolean, default=False),
        sa.Column("number_of_orders", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.Column("updated_at", sa.DateTime(True), default=datetime.datetime.now),
        sa.PrimaryKeyConstraint("chef_id"),
    )


def downgrade() -> None:
    op.drop_table("client"),
    op.drop_table("supplier"),
    op.drop_table("chef")
