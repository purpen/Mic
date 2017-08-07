# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, RadioField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError
from app.constant import PRODUCT_TYPE, PRODUCT_STATUS
from app.models import Product

class ProductForm(Form):
    upc = StringField(lazy_gettext('UPC'))
    ean = StringField(lazy_gettext('EAN'))
    jan = StringField(lazy_gettext('JAN'))
    isbn = StringField(lazy_gettext('ISBN'))
    mpn = StringField(lazy_gettext('MPN'))
    bar_code = StringField(lazy_gettext('Bar Code'))

    location = StringField(lazy_gettext('Location'))
    quantity = StringField(lazy_gettext('Quantity'))

    cover = IntegerField(lazy_gettext('Cover'))
    brand_id = SelectField(lazy_gettext('Brand'), choices=[], coerce=int)

    # 是否配送
    shipping = RadioField(lazy_gettext('Require Shipping'), choices=[
        (1, lazy_gettext('Yes')), (-1, lazy_gettext('No'))
    ], coerce=int, default=1)
    price = FloatField(lazy_gettext('Price'))
    discount_price = FloatField(lazy_gettext('Discount Price'))
    points = IntegerField(lazy_gettext('Points'))

    # 上架日期
    date_available = StringField(lazy_gettext('Date Available'))

    weight = FloatField(lazy_gettext('Weight'), default=0.0)
    length = FloatField(lazy_gettext('Length'), default=0.0)
    width = FloatField(lazy_gettext('Width'), default=0.0)
    height = FloatField(lazy_gettext('Height'), default=0.0)

    mini_cnt = IntegerField(lazy_gettext('Mini Order Quantity'), default=1)

    sort_order = IntegerField(lazy_gettext('Sort Order'), default=1)

    stock = IntegerField(lazy_gettext('Stock'))
    low_stock = IntegerField(lazy_gettext('Lowest Stock'))

    status = SelectField(lazy_gettext('Status'), choices=[(s[0], s[1]) for s in PRODUCT_STATUS], coerce=int)
    type = SelectField(lazy_gettext('Type'), choices=PRODUCT_TYPE, coerce=int)
    # whether recommend
    is_recommend = BooleanField(lazy_gettext('Is Recommended'), default=False)

class ProductSkuForm(Form):
    serial_no = StringField(lazy_gettext('Serial No.'), validators=[DataRequired()])
    sku_cover_id = IntegerField(lazy_gettext('Cover'), default=0)
    sale_price = FloatField(lazy_gettext('Sale Price'), default=0.00)
    s_model = StringField(lazy_gettext('Model'))
    s_weight = FloatField(lazy_gettext('Weight'), default=0.00)
    remark = TextAreaField(lazy_gettext('Remark'))