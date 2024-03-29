"""add product relate table

Revision ID: 2b8d132e5aee
Revises: c79be4d02313
Create Date: 2017-06-02 16:19:53.678976

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b8d132e5aee'
down_revision = 'c79be4d02313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fp_attribute_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.String(length=32), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('recurring_id', sa.Integer(), nullable=True),
    sa.Column('option', sa.Text(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_customer_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('approval', sa.Integer(), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_tax_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_tax_rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('geo_zone_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('rate', sa.Float(precision=15, asdecimal=4), nullable=True),
    sa.Column('type', sa.String(length=1), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_weight_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(precision=15, asdecimal=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_attribute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attribute_group_id', sa.Integer(), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attribute_group_id'], ['fp_attribute_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_attribute_group_description',
    sa.Column('attribute_group_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['attribute_group_id'], ['fp_attribute_group.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('attribute_group_id', 'language_id')
    )
    op.create_table('fp_customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_group_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=96), nullable=False),
    sa.Column('password', sa.String(length=40), nullable=False),
    sa.Column('telephone', sa.String(length=32), nullable=True),
    sa.Column('fax', sa.String(length=32), nullable=True),
    sa.Column('salt', sa.String(length=9), nullable=True),
    sa.Column('cart', sa.Text(), nullable=True),
    sa.Column('wishlist', sa.Text(), nullable=True),
    sa.Column('newsletter', sa.SmallInteger(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=40), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('approved', sa.SmallInteger(), nullable=True),
    sa.Column('safe', sa.SmallInteger(), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.Column('code', sa.String(length=40), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_group_id'], ['fp_customer_group.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fp_customer_email'), 'fp_customer', ['email'], unique=True)
    op.create_table('fp_customer_group_description',
    sa.Column('customer_group_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['customer_group_id'], ['fp_customer_group.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('customer_group_id', 'language_id')
    )
    op.create_table('fp_stock_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_weight_class_description',
    sa.Column('weight_class_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=False),
    sa.Column('unit', sa.String(length=4), nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.ForeignKeyConstraint(['weight_class_id'], ['fp_weight_class.id'], ),
    sa.PrimaryKeyConstraint('weight_class_id', 'language_id')
    )
    op.create_table('fp_zone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['fp_country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_attribute_description',
    sa.Column('attribute_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['attribute_id'], ['fp_attribute.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('attribute_id', 'language_id')
    )
    op.create_table('fp_banner_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('banner_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('link', sa.String(length=255), nullable=True),
    sa.Column('image', sa.Integer(), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['banner_id'], ['fp_banner.id'], ),
    sa.ForeignKeyConstraint(['image'], ['fp_asset.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_customer_search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('keyword', sa.String(length=255), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=40), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['fp_customer.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fp_product_description',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tag', sa.Text(), nullable=True),
    sa.Column('meta_title', sa.String(length=255), nullable=False),
    sa.Column('meta_description', sa.String(length=255), nullable=False),
    sa.Column('meta_keyword', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['fp_language.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['fp_product.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'language_id')
    )
    op.create_table('fp_product_discount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('customer_group_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(precision=15, asdecimal=4), nullable=True),
    sa.Column('date_start', sa.Date(), nullable=False),
    sa.Column('date_end', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['customer_group_id'], ['fp_customer_group.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['fp_product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('fp_product', sa.Column('cover_id', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('date_available', sa.Date(), nullable=True))
    op.add_column('fp_product', sa.Column('ean', sa.String(length=14), nullable=True))
    op.add_column('fp_product', sa.Column('height', sa.Float(precision=15, asdecimal=8), nullable=True))
    op.add_column('fp_product', sa.Column('isbn', sa.String(length=17), nullable=True))
    op.add_column('fp_product', sa.Column('jan', sa.String(length=13), nullable=True))
    op.add_column('fp_product', sa.Column('length', sa.Float(precision=15, asdecimal=8), nullable=True))
    op.add_column('fp_product', sa.Column('length_class_id', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('location', sa.String(length=128), nullable=True))
    op.add_column('fp_product', sa.Column('mini_cnt', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('model', sa.String(length=64), nullable=True))
    op.add_column('fp_product', sa.Column('mpn', sa.String(length=64), nullable=True))
    op.add_column('fp_product', sa.Column('points', sa.SmallInteger(), nullable=True))
    op.add_column('fp_product', sa.Column('quantity', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('shipping', sa.SmallInteger(), nullable=True))
    op.add_column('fp_product', sa.Column('sku', sa.String(length=11), nullable=False))
    op.add_column('fp_product', sa.Column('sort_order', sa.SmallInteger(), nullable=True))
    op.add_column('fp_product', sa.Column('stock_status_id', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('subtract', sa.SmallInteger(), nullable=True))
    op.add_column('fp_product', sa.Column('tax_class_id', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('upc', sa.String(length=12), nullable=True))
    op.add_column('fp_product', sa.Column('weight', sa.Float(precision=15, asdecimal=8), nullable=True))
    op.add_column('fp_product', sa.Column('weight_class_id', sa.Integer(), nullable=True))
    op.add_column('fp_product', sa.Column('width', sa.Float(precision=15, asdecimal=8), nullable=True))
    op.create_index(op.f('ix_fp_product_sku'), 'fp_product', ['sku'], unique=True)
    op.drop_index('ix_fp_product_rid', table_name='fp_product')
    op.create_foreign_key(None, 'fp_product', 'fp_asset', ['cover_id'], ['id'])
    op.drop_column('fp_product', 'description')
    op.drop_column('fp_product', 'rid')
    op.drop_column('fp_product', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fp_product', sa.Column('name', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('fp_product', sa.Column('rid', mysql.VARCHAR(length=11), nullable=False))
    op.add_column('fp_product', sa.Column('description', mysql.TEXT(), nullable=True))
    op.drop_constraint(None, 'fp_product', type_='foreignkey')
    op.create_index('ix_fp_product_rid', 'fp_product', ['rid'], unique=True)
    op.drop_index(op.f('ix_fp_product_sku'), table_name='fp_product')
    op.drop_column('fp_product', 'width')
    op.drop_column('fp_product', 'weight_class_id')
    op.drop_column('fp_product', 'weight')
    op.drop_column('fp_product', 'upc')
    op.drop_column('fp_product', 'tax_class_id')
    op.drop_column('fp_product', 'subtract')
    op.drop_column('fp_product', 'stock_status_id')
    op.drop_column('fp_product', 'sort_order')
    op.drop_column('fp_product', 'sku')
    op.drop_column('fp_product', 'shipping')
    op.drop_column('fp_product', 'quantity')
    op.drop_column('fp_product', 'points')
    op.drop_column('fp_product', 'mpn')
    op.drop_column('fp_product', 'model')
    op.drop_column('fp_product', 'mini_cnt')
    op.drop_column('fp_product', 'location')
    op.drop_column('fp_product', 'length_class_id')
    op.drop_column('fp_product', 'length')
    op.drop_column('fp_product', 'jan')
    op.drop_column('fp_product', 'isbn')
    op.drop_column('fp_product', 'height')
    op.drop_column('fp_product', 'ean')
    op.drop_column('fp_product', 'date_available')
    op.drop_column('fp_product', 'cover_id')
    op.drop_table('fp_product_discount')
    op.drop_table('fp_product_description')
    op.drop_table('fp_customer_search')
    op.drop_table('fp_banner_image')
    op.drop_table('fp_attribute_description')
    op.drop_table('fp_zone')
    op.drop_table('fp_weight_class_description')
    op.drop_table('fp_stock_status')
    op.drop_table('fp_customer_group_description')
    op.drop_index(op.f('ix_fp_customer_email'), table_name='fp_customer')
    op.drop_table('fp_customer')
    op.drop_table('fp_attribute_group_description')
    op.drop_table('fp_attribute')
    op.drop_table('fp_weight_class')
    op.drop_table('fp_tax_rate')
    op.drop_table('fp_tax_class')
    op.drop_table('fp_customer_group')
    op.drop_table('fp_cart')
    op.drop_table('fp_banner')
    op.drop_table('fp_attribute_group')
    # ### end Alembic commands ###
