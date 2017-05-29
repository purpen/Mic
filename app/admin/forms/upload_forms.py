# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_babelex import gettext
from wtforms import ValidationError

class UploadForm(FlaskForm):
    file =