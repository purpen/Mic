"""remove create_update_at product table

Revision ID: 29f7fbdbce76
Revises: 41d018dace09
Create Date: 2017-08-03 23:41:37.451499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '29f7fbdbce76'
down_revision = '41d018dace09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fp_product', 'updated_at')
    op.drop_column('fp_product', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_product', sa.Column('created_at', mysql.DATETIME(), nullable=True))
    op.add_column('fp_product', sa.Column('updated_at', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
