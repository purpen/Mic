# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User

class PostForm(Form):
	body = TextAreaField("What's on your mind?", validators=[DataRequired()])
	submit = SubmitField('Submit')