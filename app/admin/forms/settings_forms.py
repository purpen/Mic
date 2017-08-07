# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm as Form
from flask_babelex import lazy_gettext

from wtforms.fields import StringField, TextAreaField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, optional

from app.models import Language, Country, Currency


class SiteForm(Form):
    name = StringField(lazy_gettext('Site Name'), validators=[DataRequired(message=lazy_gettext("Store name can't empty!")),
                                                          Length(2, 64)])
    domain = IntegerField(lazy_gettext('Domain'))
    unicode = StringField(lazy_gettext('Unicode'))
    copyright = StringField(lazy_gettext('Copyright'))
    description = TextAreaField(lazy_gettext('Description'))
    status = SelectField(lazy_gettext('Site Status'), choices=[
        (1, lazy_gettext('Enabled')), (-1, lazy_gettext('Disabled'))
    ], coerce=int)
    default_country = SelectField(lazy_gettext('Country'), choices=[], coerce=int)
    default_language = SelectField(lazy_gettext('Default Language'), choices=[], coerce=int)
    default_currency = SelectField(lazy_gettext('Default Currency'), choices=[], coerce=int)


class LanguageForm(Form):
    name = StringField(lazy_gettext('Language Name'), validators=[DataRequired(message=lazy_gettext('Language name cant empty!')),
                                                             Length(1, 32)])
    code = StringField(lazy_gettext('Code'), validators=[DataRequired(message=lazy_gettext('Language code cant empty!')),
                                                         Length(2, 5)])

    locale = StringField(lazy_gettext('Locale'))
    icon = IntegerField(lazy_gettext('Icon'), default=0)
    directory = StringField(lazy_gettext('Directory'))
    sort_order = IntegerField(lazy_gettext('Sort Order'), default=1)
    status = SelectField(lazy_gettext('Site Status'), choices=[
        (1, lazy_gettext('Enabled')), (-1, lazy_gettext('Disabled'))
    ], coerce=int)


    def validate_code(self, field):
        if Language.query.filter_by(code=field.data).first():
            return ValidationError(lazy_gettext('The name[%s] already exists.' % field.data))


class EditLanguageForm(LanguageForm):

    def __init__(self, language, *args, **kwargs):
        super(EditLanguageForm, self).__init__(*args, **kwargs)

        self.language = language


    def validate_code(self, field):
        if field.data != self.language.code and \
            Language.query.filter_by(code=field.data).first():
            return ValidationError(lazy_gettext('The name[%s] already exists.' % field.data))


class CountryForm(Form):
    name = StringField(lazy_gettext('Country Name'),
                       validators=[DataRequired(message=lazy_gettext('Country name cant empty!'))])
    iso_code_2 = StringField(lazy_gettext('ISO Code (2)'),
                             validators=[DataRequired(message=lazy_gettext('ISO Code (2) cant empty!'))])
    iso_code_3 = StringField(lazy_gettext('ISO Code (3)'),
                             validators=[DataRequired(message=lazy_gettext('ISO Code (3) cant empty!'))])
    address_format = TextAreaField(lazy_gettext('Address Format'))
    postcode_required = RadioField(lazy_gettext('Postcode required'),
                                   choices=[(True, 'Yes'), (False, 'No')],
                                   validators=[InputRequired()],
                                   coerce=lambda x: x != 'False')
    status = SelectField(lazy_gettext('Status'),
                         choices=[(1, 'Enabled'), (-1, 'Disabled')],
                         coerce=int)


    def validate_name(self, filed):
        if Country.query.filter_by(name=filed.data).first():
            return ValidationError(lazy_gettext('Country name [%s] already exists.' % filed.data))


class EditCountryForm(CountryForm):

    def __init__(self, country, *args, **kwargs):
        super(EditCountryForm, self).__init__(*args, **kwargs)
        self.country = country

    def validate_name(self, filed):
        if filed.data != self.country.name and \
            Country.query.filter_by(name=filed.data).first():
            return ValidationError(lazy_gettext('Country name [%s] already exists.' % filed.data))



class CurrencyForm(Form):
    title = StringField('Currency Title', validators=[DataRequired(message=lazy_gettext('Currency title cant empty!'))])
    code = StringField('Code', validators=[DataRequired(message=lazy_gettext('Currency code cant empty!'))])
    symbol_left = StringField('Symbol Left')
    symbol_right = StringField('Symbol_right')
    # 小数位
    decimal_place = IntegerField('Decimal Place')
    value = FloatField('Value')
    status = SelectField(lazy_gettext('Status'),
                         choices=[(1, lazy_gettext('Enabled')), (-1, lazy_gettext('Disabled'))],
                         coerce=int)





