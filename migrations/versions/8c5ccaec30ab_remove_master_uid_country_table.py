"""remove master_uid country table

Revision ID: 8c5ccaec30ab
Revises: a7893e4dd6ae
Create Date: 2017-08-04 11:13:20.890072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8c5ccaec30ab'
down_revision = 'a7893e4dd6ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_fp_country_master_uid', table_name='fp_country')
    op.drop_column('fp_country', 'master_uid')
    op.drop_index('ix_fp_currency_master_uid', table_name='fp_currency')
    op.drop_column('fp_currency', 'master_uid')
    op.drop_index('ix_fp_language_master_uid', table_name='fp_language')
    op.drop_column('fp_language', 'master_uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_language', sa.Column('master_uid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_index('ix_fp_language_master_uid', 'fp_language', ['master_uid'], unique=False)
    op.add_column('fp_currency', sa.Column('master_uid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_index('ix_fp_currency_master_uid', 'fp_currency', ['master_uid'], unique=False)
    op.add_column('fp_country', sa.Column('master_uid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_index('ix_fp_country_master_uid', 'fp_country', ['master_uid'], unique=False)
    # ### end Alembic commands ###
