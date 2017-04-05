# -*- coding: utf-8 -*-

from flask import g, render_template, session, redirect, url_for, flash, request
from flask_babelex import gettext
from app import babel
from config import LANGUAGES
from . import web

# localeselector装饰器，
# 它被调用在请求之前为了当产生响应的时候给我们机会选择使用的语言
@babel.localeselector
def get_locale():
	user = getattr(g, 'user', None)
	if user is not None:
		return user.locale
	return request.accept_languages.best_match(LANGUAGES.keys())

@babel.timezoneselector
def get_timezone():
	user = getattr(g, 'user', None)
	if user is not None:
		return user.timezone

@web.before_request
def before_request():
	g.locale = get_locale()

@web.route('/')
def index():
	flash(gettext('Invalid login. Please try again.'))
	return render_template('web/index.html')