"""create_spell_images_table

Revision ID: a8a58a1af0b1
Revises: d2d13b0bc0f8
Create Date: 2025-04-24 13:05:37.287244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8a58a1af0b1'
down_revision = 'd2d13b0bc0f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spell_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spell_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spell_images')
    # ### end Alembic commands ###
