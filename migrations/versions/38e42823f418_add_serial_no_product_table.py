"""add serial_no product table

Revision ID: 38e42823f418
Revises: c237dc79f0b4
Create Date: 2017-08-06 20:59:23.431099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e42823f418'
down_revision = 'c237dc79f0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_product', sa.Column('serial_no', sa.String(length=12), nullable=False))
    op.create_index(op.f('ix_fp_product_serial_no'), 'fp_product', ['serial_no'], unique=True)
    op.drop_index('ix_fp_product_sku', table_name='fp_product')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_fp_product_sku', 'fp_product', ['sku'], unique=True)
    op.drop_index(op.f('ix_fp_product_serial_no'), table_name='fp_product')
    op.drop_column('fp_product', 'serial_no')
    # ### end Alembic commands ###
