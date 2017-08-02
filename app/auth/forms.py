# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField()


class RegisterationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm password', validators=[DataRequired()])

	# 中定义了以validate_ 开头且后面跟着字段名的方法，
	# 这个方法就和常规的验证函数一起调用
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

