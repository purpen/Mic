"""add serial_no for store table

Revision ID: 955dcfa369f3
Revises: ea8db3b6c178
Create Date: 2017-08-01 23:30:17.162580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '955dcfa369f3'
down_revision = 'ea8db3b6c178'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_store', sa.Column('serial_no', sa.String(length=32), nullable=False))
    op.create_index(op.f('ix_fp_store_serial_no'), 'fp_store', ['serial_no'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fp_store_serial_no'), table_name='fp_store')
    op.drop_column('fp_store', 'serial_no')
    # ### end Alembic commands ###
