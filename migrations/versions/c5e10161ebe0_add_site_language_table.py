"""add site_language table

Revision ID: c5e10161ebe0
Revises: 48da0c61e109
Create Date: 2017-08-03 13:52:48.067052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5e10161ebe0'
down_revision = '48da0c61e109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_site_language',
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['fp_site.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fp_site_language')
    # ### end Alembic commands ###
