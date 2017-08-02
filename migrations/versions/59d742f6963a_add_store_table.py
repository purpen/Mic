"""add store table

Revision ID: 59d742f6963a
Revises: 29b75ccc0bb5
Create Date: 2017-07-27 16:18:44.608038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59d742f6963a'
down_revision = '29b75ccc0bb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('master_uid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('locale', sa.String(length=4), nullable=True),
    sa.Column('country', sa.String(length=30), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('domain', sa.SmallInteger(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('update_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fp_stores_master_uid'), 'fp_stores', ['master_uid'], unique=False)
    op.create_index(op.f('ix_fp_stores_name'), 'fp_stores', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fp_stores_name'), table_name='fp_stores')
    op.drop_index(op.f('ix_fp_stores_master_uid'), table_name='fp_stores')
    op.drop_table('fp_stores')
    # ### end Alembic commands ###