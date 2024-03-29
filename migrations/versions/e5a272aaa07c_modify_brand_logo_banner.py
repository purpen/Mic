"""modify brand logo/banner

Revision ID: e5a272aaa07c
Revises: 8229f18658d8
Create Date: 2017-05-27 11:31:20.554980

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e5a272aaa07c'
down_revision = '8229f18658d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_brand', sa.Column('banner', sa.Integer(), nullable=True))
    op.drop_constraint('fp_brand_ibfk_2', 'fp_brand', type_='foreignkey')
    op.drop_constraint('fp_brand_ibfk_3', 'fp_brand', type_='foreignkey')
    op.create_foreign_key(None, 'fp_brand', 'fp_asset', ['banner'], ['id'])
    op.drop_column('fp_brand', 'banner_id')
    op.drop_column('fp_brand', 'logo_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_brand', sa.Column('logo_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('fp_brand', sa.Column('banner_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'fp_brand', type_='foreignkey')
    op.create_foreign_key('fp_brand_ibfk_3', 'fp_brand', 'fp_asset', ['banner_id'], ['id'])
    op.create_foreign_key('fp_brand_ibfk_2', 'fp_brand', 'fp_asset', ['logo_id'], ['id'])
    op.drop_column('fp_brand', 'banner')
    # ### end Alembic commands ###
