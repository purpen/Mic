# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import gettext, lazy_gettext
from wtforms.fields import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User, Site

class SetupForm(Form):
    email = StringField(lazy_gettext('Email'), validators=[DataRequired(message=lazy_gettext("Email can't empty!")),
                                                      Email(message=lazy_gettext("Format isn't email!"))])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired(message=lazy_gettext("Password can't empty!")),
                                                              Length(6,message=lazy_gettext("The password is at least 6 characters"))])
    store_name = StringField(lazy_gettext('Store Name'), validators=[DataRequired(message=lazy_gettext("Store name can't empty!"))])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))

    def validate_store_name(self, field):
        if Site.query.filter_by(name=field.data).first():
            raise ValidationError(lazy_gettext('Store name already exist!'))


class EditProfileForm(Form):
    name = StringField(lazy_gettext('User name'), validators=[Length(0, 64)])
    location = StringField(lazy_gettext('Location'), validators=[Length(0, 64)])
    about_me = TextAreaField(lazy_gettext('About me'))
