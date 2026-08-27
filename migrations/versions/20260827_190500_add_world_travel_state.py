"""add world travel state

Revision ID: a91e5d7c2b44
Revises: c7b8a2f4d901
Create Date: 2026-08-27 19:05:00

"""
from alembic import op
import sqlalchemy as sa


revision = "a91e5d7c2b44"
down_revision = "c7b8a2f4d901"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.add_column(sa.Column("travels", sa.Integer(), nullable=False, server_default="4"))
        batch_op.add_column(sa.Column("town", sa.String(length=50), nullable=False, server_default="academy"))
        batch_op.add_column(sa.Column("mount", sa.String(length=50), nullable=False, server_default=""))
        batch_op.add_column(sa.Column("jewelry", sa.String(length=50), nullable=False, server_default=""))
        batch_op.add_column(sa.Column("mana_runes", sa.Integer(), nullable=False, server_default="0"))


def downgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.drop_column("mana_runes")
        batch_op.drop_column("jewelry")
        batch_op.drop_column("mount")
        batch_op.drop_column("town")
        batch_op.drop_column("travels")
