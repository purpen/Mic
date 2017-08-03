"""add site_currency table

Revision ID: 993deebe4fd5
Revises: c5e10161ebe0
Create Date: 2017-08-03 14:55:50.820117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993deebe4fd5'
down_revision = 'c5e10161ebe0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_site_currency',
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['fp_currency.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['fp_site.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fp_site_currency')
    # ### end Alembic commands ###
