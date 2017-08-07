"""remove create_update_at product table

Revision ID: 4c8dac463381
Revises: 29f7fbdbce76
Create Date: 2017-08-03 23:42:24.407770

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4c8dac463381'
down_revision = '29f7fbdbce76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fp_product', 'published_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_product', sa.Column('published_at', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###