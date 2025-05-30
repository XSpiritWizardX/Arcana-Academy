"""create_players_table

Revision ID: 5de10e440756
Revises: ffdc0a98111c
Create Date: 2025-04-24 08:51:28.385847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de10e440756'
down_revision = 'ffdc0a98111c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.Column('magic_class', sa.String(length=20), nullable=False),
    sa.Column('element', sa.String(length=20), nullable=False),
    sa.Column('level', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('xp', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('gold', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('health', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('mana', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('damage', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('speed', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('strength', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('intellect', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('dexterity', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('vitality', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    # ### end Alembic commands ###
