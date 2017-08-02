# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from app.models import Directory

class FolderForm(Form):
    folder = StringField('Folder', validators=[DataRequired(message=lazy_gettext('Folder name cant empty!'))])

    def validate_folder(self, field):
        if Directory.query.filter_by(name=field.data).first():
            raise ValidationError(lazy_gettext('Name[%s] has been registered. Change it.' % field.data))
