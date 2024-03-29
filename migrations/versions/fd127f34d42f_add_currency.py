"""add currency

Revision ID: fd127f34d42f
Revises: 5f92a678689b
Create Date: 2017-05-29 23:54:59.544232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd127f34d42f'
down_revision = '5f92a678689b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('symbol_left', sa.String(length=12), nullable=True),
    sa.Column('symbol_right', sa.String(length=12), nullable=True),
    sa.Column('decimal_place', sa.String(length=1), nullable=False),
    sa.Column('value', sa.Float(precision=15, asdecimal=8), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fp_currency')
    # ### end Alembic commands ###
