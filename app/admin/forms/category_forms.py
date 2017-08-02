# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import Category


class CategoryForm(Form):
    sort_order = IntegerField(lazy_gettext('Sort Order'))
    parent_id = IntegerField(lazy_gettext('Parent'))
    top = BooleanField(lazy_gettext('Top'))
    icon = IntegerField(lazy_gettext('Icon image'))
    cover = IntegerField(lazy_gettext('Cover image'))
