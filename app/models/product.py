# -*- coding: utf-8 -*-
from enum import Enum
from flask_babelex import gettext
from app.utils import timestamp
from app import db, uploader
from .asset import Asset
from ..constant import PRODUCT_STATUS

class Product(db.Model):
    __tablename__ = 'fp_product'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('fp_site.id'))

    master_uid = db.Column(db.Integer, index=True, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('fp_user.id'))

    # 所属的品牌
    brand_id = db.Column(db.Integer, db.ForeignKey('fp_brand.id'))

    # product number id
    serial_no = db.Column(db.String(12), unique=True, index=True, nullable=False)
    sku = db.Column(db.String(11), nullable=True)
    upc = db.Column(db.String(12), nullable=True)
    ean = db.Column(db.String(14), nullable=True)
    jan = db.Column(db.String(13), nullable=True)
    isbn = db.Column(db.String(17), nullable=True)
    mpn = db.Column(db.String(64), nullable=True)
    bar_code = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(128), nullable=True)

    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float(15, 4))
    discount_price = db.Column(db.Float(10, 2))
    # 指定封面图，否则默认取第一张
    cover_id = db.Column(db.Integer, db.ForeignKey('fp_asset.id'))
    # 是否配送
    is_shipping = db.Column(db.Boolean, default=True)
    points = db.Column(db.SmallInteger, default=0)
    # 税率
    tax_class_id = db.Column(db.Integer, default=0)
    # 重量
    weight = db.Column(db.Float(15, 8))
    weight_class_id = db.Column(db.Integer)
    # 长x宽x高
    length = db.Column(db.Float(15, 8))
    width = db.Column(db.Float(15, 8))
    height = db.Column(db.Float(15, 8))
    length_class_id = db.Column(db.Integer)
    # 是否减库存
    is_subtract = db.Column(db.Boolean, default=True)
    # 最少采购数量
    mini_quantity = db.Column(db.Integer, default=1)
    # 排序
    sort_order = db.Column(db.SmallInteger, default=0)
    # 上架、下架
    status = db.Column(db.Boolean, default=1)
    # 上架日期
    date_available = db.Column(db.Date())
    # 产品类型
    type = db.Column(db.SmallInteger, default=1)
    # whether recommend
    is_recommend = db.Column(db.Boolean, default=False)
    sale_count = db.Column(db.Integer, default=0)

    # 评价计数
    rate_val = db.Column(db.Float(10, 2))
    rate_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=1)
    comment_count = db.Column(db.Integer, default=0)
    comment_stars = db.Column(db.Integer, default=0)

    stock = db.Column(db.Integer, default=0)
    lowest_stock = db.Column(db.Integer, default=0)

    published_at = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    # 1 => N
    product_descriptions = db.relationship(
        'ProductDescription', backref='product', lazy='dynamic'
    )

    # 1 => N
    images = db.relationship(
        'ProductImage', backref='product', lazy='dynamic'
    )

    # 1 => N
    skus = db.relationship(
        'ProductSku', backref='product', lazy='dynamic'
    )


    def default_description(self, lang_id=0):
        if lang_id:
            return self.product_descriptions.filter_by(language_id=lang_id).first()
        return self.product_descriptions.first()

    @property
    def cover(self):
        """cover asset info"""
        return Asset.query.get(self.cover_id) if self.cover_id else None

    @property
    def status_label(self):
        for status in PRODUCT_STATUS:
            if status[0] == self.status:
                return status

    def image_list(self):
        """获取产品的主图列表"""
        images = []
        for image in self.images:
            asset = Asset.query.get(image.asset_id)
            if asset:
                images.append(asset.to_json())
        return images

    @property
    def category_ids(self):
        """获取所属的分类ID"""
        return [category.id for category in self.categories]

    def add_categories(self, *categories):
        """追加所属分类"""
        self.categories.extend([category for category in categories if category not in self.categories])

    def update_categories(self, *categories):
        """更新所属分类"""
        self.categories = [category for category in categories]

    def remove_categories(self, *categories):
        """删除所属分类"""
        self.categories = [category for category in self.categories if category not in categories]


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

    def __repr__(self):
        return '<ProductDescription {}>'.format(self.product_id)


class ProductSku(db.Model):
    """产品的SKU"""
    __tablename__ = 'fp_product_sku'

    id = db.Column(db.Integer, primary_key=True)
    master_uid = db.Column(db.Integer, index=True, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('fp_product.id'))
    product_serial_no = db.Column(db.String(12), nullable=False)
    # 产品编号sku
    serial_no = db.Column(db.String(12), unique=True, index=True, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('fp_asset.id'))

    s_model = db.Column(db.String(64), nullable=False)
    # 重量
    s_weight = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    sale_price = db.Column(db.Numeric(precision=10, scale=2), default=0.00)
    # 备注
    remark = db.Column(db.String(255), nullable=True)
    # 状态：-1、取消或缺省状态； 1、正常（默认）
    status = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.Integer, index=True, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    # 第三方平台编号
    outside_serial_no = db.Column(db.String(20), index=True, nullable=True)

    @property
    def product_name(self):
        """product name"""
        return self.product.name

    @property
    def cover(self):
        """cover asset info"""
        return Asset.query.get(self.cover_id) if self.cover_id else DEFAULT_IMAGES['cover']

    def to_json(self):
        """资源和JSON的序列化转换"""
        json_asset = {
            'id': self.id,
            'serial_no': self.serial_no,
            's_model': self.s_model,
            'cover': uploader.url(self.cover.filepath),
            'sale_price': str(self.sale_price),
            's_weight': str(self.s_weight)
        }
        return json_asset

    def __repr__(self):
        return '<Product %r>' % self.serial_no


class ProductImage(db.Model):
    __tablename__ = 'fp_product_image'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('fp_product.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('fp_asset.id'))
    sort_order = db.Column(db.SmallInteger, default=1)


    def __repr__(self):
        return '<ProductImage {}>'.format(self.asset_id)


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