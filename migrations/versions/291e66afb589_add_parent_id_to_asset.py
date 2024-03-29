"""add parent_id to asset

Revision ID: 291e66afb589
Revises: 1a85f9645db7
Create Date: 2017-05-26 00:13:30.134043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '291e66afb589'
down_revision = '1a85f9645db7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_directory', sa.Column('parent_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fp_directory', 'parent_id')
    # ### end Alembic commands ###
