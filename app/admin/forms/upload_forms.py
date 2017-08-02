# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError


class UploadForm(Form):
    photo = FileField('Upload file')