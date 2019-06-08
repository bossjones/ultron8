"""create account table

Revision ID: 2339440ca3c3
Revises: 2e84451f0a1e
Create Date: 2019-06-06 22:21:51.329277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2339440ca3c3"
down_revision = "2e84451f0a1e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "guid_tracker",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("expire", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_guid_tracker_expire"), "guid_tracker", ["expire"], unique=False
    )
    op.create_index(
        op.f("ix_guid_tracker_name"), "guid_tracker", ["name"], unique=False
    )
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_item_description"), "item", ["description"], unique=False)
    op.create_index(op.f("ix_item_id"), "item", ["id"], unique=False)
    op.create_index(op.f("ix_item_title"), "item", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_item_title"), table_name="item")
    op.drop_index(op.f("ix_item_id"), table_name="item")
    op.drop_index(op.f("ix_item_description"), table_name="item")
    op.drop_table("item")
    op.drop_index(op.f("ix_guid_tracker_name"), table_name="guid_tracker")
    op.drop_index(op.f("ix_guid_tracker_expire"), table_name="guid_tracker")
    op.drop_table("guid_tracker")
    # ### end Alembic commands ###