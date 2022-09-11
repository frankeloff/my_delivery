"""products

Revision ID: 60489bb93019
Revises: be4edb7bdc6c
Create Date: 2022-09-02 18:46:12.000224

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "60489bb93019"
down_revision = "be4edb7bdc6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("product_id", sa.Integer(), autoincrement=True, unique=True),
        sa.Column("name", sa.String()),
        sa.PrimaryKeyConstraint("product_id"),
    )


def downgrade() -> None:
    op.drop_table("products")
