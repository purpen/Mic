# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from app.models import Product

class ProductForm(Form):
    sku = StringField(lazy_gettext('Serial No'), validators=[DataRequired(message=lazy_gettext("Product serial no can't empty"))])
    model = StringField(lazy_gettext('Mode'))
    upc = StringField(lazy_gettext('UPC'))
    ean = StringField(lazy_gettext('EAN'))
    jan = StringField(lazy_gettext('JAN'))
    isbn = StringField(lazy_gettext('ISBN'))
    mpn = StringField(lazy_gettext('MPN'))
    bar_code = StringField(lazy_gettext('Bar Code'))

    location = StringField(lazy_gettext('Location'))
    quantity = StringField(lazy_gettext('Quantity'))
    stock_status_id = IntegerField(lazy_gettext('Stock Status'))

    cover = IntegerField(lazy_gettext('Cover'))
    brand_id = IntegerField(lazy_gettext('Brand'))

    # 是否配送
    shipping = IntegerField(lazy_gettext('Shipping'))
    price = FloatField(lazy_gettext('Price'))
    discount_price = FloatField(lazy_gettext('Discount Price'))
    points = IntegerField(lazy_gettext('Points'))

    # 上架日期
    date_available = StringField(lazy_gettext('Date Available'))

    weight = FloatField(lazy_gettext('Weight'))
    length = FloatField(lazy_gettext('Length'))
    width = FloatField(lazy_gettext('Width'))
    height = FloatField(lazy_gettext('Height'))

    mini_cnt = IntegerField(lazy_gettext('Mini Order Quantity'), default=1)

    sort_order = IntegerField(lazy_gettext('Sort Order'))

    stock = IntegerField(lazy_gettext('Stock'))
    low_stock = IntegerField(lazy_gettext('Lowest Stock'))
    # type = SelectField(lazy_gettext('Type'), choices=)
    # whether recommend
    recommend = BooleanField(lazy_gettext('Is Recommended'), default=False)
