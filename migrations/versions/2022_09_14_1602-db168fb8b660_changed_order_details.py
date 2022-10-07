"""changed order_details

Revision ID: db168fb8b660
Revises: b1d5d2c65fbe
Create Date: 2022-09-14 16:02:36.926494

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "db168fb8b660"
down_revision = "b1d5d2c65fbe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("order_details", sa.Column("quantity", sa.Integer(), nullable=False))
    op.drop_column("order_details", "order_details_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order_details",
        sa.Column("order_details_id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.drop_column("order_details", "quantity")
    # ### end Alembic commands ###