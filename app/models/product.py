# -*- coding: utf-8 -*-
from enum import Enum
from flask_babelex import gettext
from app.utils import timestamp
from app import db

STATUS_DEFAULT = 1
STATUS_PUBLISHED = 2

class ProductTypeEnum(Enum):
    item = gettext('item')
    free_product = gettext('free_product')
    gift_card = gettext('gift_card')
    software = gettext('software')
    key = gettext('key')


class Product(db.Model):
    __tablename__ = 'fp_product'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('fp_user.id'))

    # product number id
    sku = db.Column(db.String(11), unique=True, index=True, nullable=False)
    model = db.Column(db.String(64), nullable=True)
    upc = db.Column(db.String(12), nullable=True)
    ean = db.Column(db.String(14), nullable=True)
    jan = db.Column(db.String(13), nullable=True)
    isbn = db.Column(db.String(17), nullable=True)
    mpn = db.Column(db.String(64), nullable=True)
    bar_code = db.Column(db.String(64), nullable=True)

    location = db.Column(db.String(128), nullable=True)
    quantity = db.Column(db.Integer, default=0)
    stock_status_id = db.Column(db.Integer, default=0)

    cover_id = db.Column(db.Integer, db.ForeignKey('fp_asset.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('fp_brand.id'))
    # 是否配送
    shipping = db.Column(db.SmallInteger, default=1)
    price = db.Column(db.Float(15, 4))
    discount_price = db.Column(db.Float(10, 2))
    points = db.Column(db.SmallInteger, default=0)
    # 税率
    tax_class_id = db.Column(db.Integer, default=0)
    # 上架日期
    date_available = db.Column(db.Date())

    weight = db.Column(db.Float(15, 8))
    weight_class_id = db.Column(db.Integer)
    length = db.Column(db.Float(15, 8))
    width = db.Column(db.Float(15, 8))
    height = db.Column(db.Float(15, 8))
    length_class_id = db.Column(db.Integer)
    # 是否减库存
    subtract = db.Column(db.SmallInteger, default=1)
    # 最少采购数量
    mini_cnt = db.Column(db.Integer, default=1)

    sort_order = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.Boolean, default=STATUS_DEFAULT)

    rate_val = db.Column(db.Float(10, 2))
    rate_count = db.Column(db.Integer, default=0)
    sale_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=1)
    comment_count = db.Column(db.Integer, default=0)
    comment_stars = db.Column(db.Integer, default=0)


    stock = db.Column(db.Integer, default=0)
    low_stock = db.Column(db.Integer, default=0)
    type = db.Column(db.Enum(ProductTypeEnum), default=ProductTypeEnum.item)
    # whether recommend
    recommend = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    published_at = db.Column(db.Integer)


    def __str__(self):
        return self.sku


    def __repr__(self):
        return '<Product {}>'.format(self.sku)


class ProductDescription(db.Model):
    __tablename__ = 'fp_product_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('product_id', 'language_id'),
    )

    master_uid = db.Column(db.Integer, index=True, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('fp_product.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    tag = db.Column(db.Text())
    meta_title = db.Column(db.String(255), nullable=False)
    meta_description = db.Column(db.String(255), nullable=False)
    meta_keyword = db.Column(db.String(255), nullable=False)


    def __str__(self):
        return self.name



class ProductDiscount(db.Model):
    __tablename__ = 'fp_product_discount'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('fp_product.id'))
    customer_group_id = db.Column(db.Integer, db.ForeignKey('fp_customer_group.id'))
    quantity = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, default=1)
    price = db.Column(db.Float(15, 4))
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)


    def __str__(self):
        return self.product_id


class StockStatus(db.Model):
    __tablename__ = 'fp_stock_status'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    name = db.Column(db.String(32))

    def __str__(self):
        return self.name


class TaxClass(db.Model):
    __tablename__ = 'fp_tax_class'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)


    def __str__(self):
        return self.title


class TaxRate(db.Model):
    __tablename__ = 'fp_tax_rate'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    # 区域
    geo_zone_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(32), nullable=False)
    rate = db.Column(db.Float(15, 4), default=0.0000)
    type = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    def __str__(self):
        return self.name


class WeightClass(db.Model):
    __tablename__ = 'fp_weight_class'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    value = db.Column(db.Float(15, 8), default=0.00000000)

    # 1 => N
    weight_descriptions = db.relationship(
        'WeightClassDescription', backref='weight_class', lazy='dynamic', cascade='delete'
    )

    def language_descriptions(self):
        all_descriptions = {}
        for lang_version in self.weight_descriptions:
            all_descriptions[lang_version.language_id] = lang_version
        return all_descriptions

    def __str__(self):
        return self.id


class WeightClassDescription(db.Model):
    __tablename__ = 'fp_weight_class_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('weight_class_id', 'language_id'),
    )

    weight_class_id = db.Column(db.Integer, db.ForeignKey('fp_weight_class.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    title = db.Column(db.String(32), nullable=False)
    unit = db.Column(db.String(4), nullable=False)

    def __str__(self):
        return self.title


class LengthClass(db.Model):
    __tablename__ = 'fp_length_class'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    value = db.Column(db.Float(15, 8), default=0.00000000)

    # 1 => N
    length_descriptions = db.relationship(
        'LengthClassDescription', backref='length_class', lazy='dynamic', cascade='delete'
    )

    def language_descriptions(self):
        all_descriptions = {}
        for lang_version in self.length_descriptions:
            all_descriptions[lang_version.language_id] = lang_version
        return all_descriptions


    def __str__(self):
        return self.id


class LengthClassDescription(db.Model):
    __tablename__ = 'fp_length_class_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('length_class_id', 'language_id'),
    )

    length_class_id = db.Column(db.Integer, db.ForeignKey('fp_length_class.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    title = db.Column(db.String(32), nullable=False)
    unit = db.Column(db.String(4), nullable=False)

    def __str__(self):
        return self.title


class Attribute(db.Model):
    __tablename__ = 'fp_attribute'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    attribute_group_id = db.Column(db.Integer, db.ForeignKey('fp_attribute_group.id'))
    sort_order = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.id

class AttributeDescription(db.Model):
    __tablename__ = 'fp_attribute_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('attribute_id', 'language_id'),
    )

    attribute_id = db.Column(db.Integer, db.ForeignKey('fp_attribute.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    name = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.name

class AttributeGroup(db.Model):
    __tablename__ = 'fp_attribute_group'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    sort_order = db.Column(db.Integer, default=0)


class AttributeGroupDescription(db.Model):
    __tablename__ = 'fp_attribute_group_description'

    __table_args__ = (
        db.PrimaryKeyConstraint('attribute_group_id', 'language_id'),
    )

    attribute_group_id = db.Column(db.Integer, db.ForeignKey('fp_attribute_group.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('fp_language.id'))
    name = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.name