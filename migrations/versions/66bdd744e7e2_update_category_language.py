"""update category language

Revision ID: 66bdd744e7e2
Revises: fd127f34d42f
Create Date: 2017-05-30 21:49:44.800170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '66bdd744e7e2'
down_revision = 'fd127f34d42f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('iso_code_2', sa.String(length=2), nullable=True),
    sa.Column('iso_code_3', sa.String(length=3), nullable=True),
    sa.Column('address_format', sa.String(length=255), nullable=True),
    sa.Column('postcode_required', sa.Boolean(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fp_country_name'), 'fp_country', ['name'], unique=True)
    op.create_table('fp_category_description',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('meta_title', sa.String(length=255), nullable=True),
    sa.Column('meta_description', sa.String(length=255), nullable=True),
    sa.Column('meta_keyword', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['fp_category.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('category_id', 'language_id')
    )
    op.create_index(op.f('ix_fp_category_description_name'), 'fp_category_description', ['name'], unique=True)
    op.drop_index('ix_fp_category_name', table_name='fp_category')
    op.drop_column('fp_category', 'description')
    op.drop_column('fp_category', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_category', sa.Column('name', mysql.VARCHAR(length=64), nullable=True))
    op.add_column('fp_category', sa.Column('description', mysql.VARCHAR(length=140), nullable=True))
    op.create_index('ix_fp_category_name', 'fp_category', ['name'], unique=True)
    op.drop_index(op.f('ix_fp_category_description_name'), table_name='fp_category_description')
    op.drop_table('fp_category_description')
    op.drop_index(op.f('ix_fp_country_name'), table_name='fp_country')
    op.drop_table('fp_country')
    # ### end Alembic commands ###
