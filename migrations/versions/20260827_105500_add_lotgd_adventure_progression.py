"""add LoGD-style adventure progression

Revision ID: 9e4a6c7d1f10
Revises: 5582f238a3b8
Create Date: 2026-08-27 10:55:00

"""
from alembic import op
import sqlalchemy as sa


revision = "9e4a6c7d1f10"
down_revision = "5582f238a3b8"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.add_column(sa.Column("gems", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("specialty_uses", sa.Integer(), nullable=False, server_default="5"))
        batch_op.add_column(sa.Column("game_day", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("alive", sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.add_column(sa.Column("weapon_level", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("armor_level", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("dragon_points", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("dragon_attack", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("dragon_defense", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("dragon_hp", sa.Integer(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("dragon_fights", sa.Integer(), nullable=False, server_default="0"))


def downgrade():
    with op.batch_alter_table("adventure_states", schema=None) as batch_op:
        batch_op.drop_column("dragon_fights")
        batch_op.drop_column("dragon_hp")
        batch_op.drop_column("dragon_defense")
        batch_op.drop_column("dragon_attack")
        batch_op.drop_column("dragon_points")
        batch_op.drop_column("armor_level")
        batch_op.drop_column("weapon_level")
        batch_op.drop_column("alive")
        batch_op.drop_column("game_day")
        batch_op.drop_column("specialty_uses")
        batch_op.drop_column("gems")
