# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext
from wtforms.fields import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from app.models import Brand

class BrandForm(Form):
    name = StringField(lazy_gettext('Name'), validators=[DataRequired(message=lazy_gettext('Brand name cant empty!')), Length(1, 64)])
    features = StringField(lazy_gettext('Features'))
    logo = IntegerField(lazy_gettext('Logo'), default=0)
    banner = IntegerField(lazy_gettext('Banner'), default=0)
    description = TextAreaField(lazy_gettext('Description'))
    sort_num = IntegerField(lazy_gettext('Sort Number'))


    def validate_name(self, field):
        """validate the name isn't unique."""
        if Brand.query.filter_by(name=field.data).first():
            raise ValidationError(lazy_gettext('Name[%s] has been registered. Change it.' % field.data))


class EditBrandForm(BrandForm):

    def __init__(self, brand, *args, **kwargs):
        super(EditBrandForm, self).__init__(*args, **kwargs)

        self.brand = brand

    def validate_name(self, field):
        """validate the name isn't unique."""
        if field.data != self.brand.name and \
                Brand.query.filter_by(name=field.data).first():
            raise ValidationError(lazy_gettext('Name[%s] has been registered. Change it.' % field.data))