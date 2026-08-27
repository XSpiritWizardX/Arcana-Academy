"""add adventure mana

Revision ID: c7b8a2f4d901
Revises: 9e4a6c7d1f10
Create Date: 2026-08-27 18:35:00

"""
from alembic import op
import sqlalchemy as sa


revision = "c7b8a2f4d901"
down_revision = "9e4a6c7d1f10"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.add_column(sa.Column("mana", sa.Integer(), nullable=False, server_default="10"))
        batch_op.add_column(sa.Column("max_mana", sa.Integer(), nullable=False, server_default="10"))


def downgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.drop_column("max_mana")
        batch_op.drop_column("mana")
