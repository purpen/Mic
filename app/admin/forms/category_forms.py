# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Category

class CategoryForm(Form):
    parent_id = IntegerField(lazy_gettext('Parent'))
    sort_order = IntegerField(lazy_gettext('Sort Order'))
    top = BooleanField(lazy_gettext('Set As Top'), default=False)
    icon = IntegerField(lazy_gettext('Icon image'))
    cover = IntegerField(lazy_gettext('Cover image'))
    status = SelectField(lazy_gettext('Site Status'), choices=[
        (1, lazy_gettext('Enabled')), (-1, lazy_gettext('Disabled'))
    ], coerce=int)
