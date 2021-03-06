"""Initial commit: item user packs action trigger trigger_types trigger_tags trigger_instance sensors

Revision ID: 8eb697bae8bb
Revises:
Create Date: 2019-09-02 14:45:19.500844

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8eb697bae8bb"
down_revision = None
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
    op.create_table(
        "packs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ref", sa.String(), nullable=True),
        sa.Column("uid", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("keywords", sa.String(), nullable=True),
        sa.Column("version", sa.String(), nullable=True),
        sa.Column("python_versions", sa.String(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("contributors", sa.String(), nullable=True),
        sa.Column("files", sa.String(), nullable=True),
        sa.Column("path", sa.String(), nullable=True),
        sa.Column("dependencies", sa.String(), nullable=True),
        sa.Column("system", sa.String(), nullable=True),
        sa.Column("created_at", sa.String(), nullable=True),
        sa.Column("updated_at", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_packs_id"), "packs", ["id"], unique=False)
    op.create_table(
        "trigger_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trigger", sa.String(length=255), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("occurrence_time", sa.String(), nullable=True),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_trigger_events_id"), "trigger_events", ["id"], unique=False
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "user", ["full_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ref", sa.String(length=255), nullable=True),
        sa.Column("uid", sa.String(length=255), nullable=True),
        sa.Column("metadata_file", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("runner_type", sa.String(length=255), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("entry_point", sa.String(length=255), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.String(), nullable=True),
        sa.Column("updated_at", sa.String(), nullable=True),
        sa.Column("packs_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["packs_id"], ["packs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_actions_id"), "actions", ["id"], unique=False)
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
    op.create_table(
        "sensors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("class_name", sa.String(length=255), nullable=True),
        sa.Column("ref", sa.String(length=255), nullable=True),
        sa.Column("uid", sa.String(length=255), nullable=True),
        sa.Column("artifact_uri", sa.String(length=255), nullable=True),
        sa.Column("poll_interval", sa.Integer(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("entry_point", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.String(), nullable=True),
        sa.Column("updated_at", sa.String(), nullable=True),
        sa.Column("packs_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["packs_id"], ["packs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sensors_id"), "sensors", ["id"], unique=False)
    op.create_table(
        "trigger_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("ref", sa.String(length=255), nullable=True),
        sa.Column("uid", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("payload_schema", sa.JSON(), nullable=True),
        sa.Column("parameters_schema", sa.JSON(), nullable=True),
        sa.Column("packs_id", sa.Integer(), nullable=True),
        sa.Column("metadata_file", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["packs_id"], ["packs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trigger_types_id"), "trigger_types", ["id"], unique=False)
    op.create_table(
        "triggers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("ref", sa.String(length=255), nullable=True),
        sa.Column("uid", sa.String(length=255), nullable=True),
        sa.Column("type", sa.String(length=255), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=True),
        sa.Column("ref_count", sa.Integer(), nullable=True),
        sa.Column("packs_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["packs_id"], ["packs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_triggers_id"), "triggers", ["id"], unique=False)
    op.create_table(
        "sensors_trigger_types_association",
        sa.Column("sensors_id", sa.Integer(), nullable=False),
        sa.Column("trigger_types_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["sensors_id"], ["sensors.id"]),
        sa.ForeignKeyConstraint(["trigger_types_id"], ["trigger_types.id"]),
        sa.PrimaryKeyConstraint("sensors_id", "trigger_types_id"),
    )
    op.create_table(
        "trigger_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trigger_type_id", sa.Integer(), nullable=True),
        sa.Column("tag", sa.String(), nullable=True),
        sa.Column("trigger_name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["trigger_type_id"], ["trigger_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trigger_tags_id"), "trigger_tags", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_trigger_tags_id"), table_name="trigger_tags")
    op.drop_table("trigger_tags")
    op.drop_table("sensors_trigger_types_association")
    op.drop_index(op.f("ix_triggers_id"), table_name="triggers")
    op.drop_table("triggers")
    op.drop_index(op.f("ix_trigger_types_id"), table_name="trigger_types")
    op.drop_table("trigger_types")
    op.drop_index(op.f("ix_sensors_id"), table_name="sensors")
    op.drop_table("sensors")
    op.drop_index(op.f("ix_item_title"), table_name="item")
    op.drop_index(op.f("ix_item_id"), table_name="item")
    op.drop_index(op.f("ix_item_description"), table_name="item")
    op.drop_table("item")
    op.drop_index(op.f("ix_actions_id"), table_name="actions")
    op.drop_table("actions")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_full_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_trigger_events_id"), table_name="trigger_events")
    op.drop_table("trigger_events")
    op.drop_index(op.f("ix_packs_id"), table_name="packs")
    op.drop_table("packs")
    op.drop_table("guid_tracker")
    # ### end Alembic commands ###
