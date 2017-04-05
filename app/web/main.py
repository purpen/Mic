# -*- coding: utf-8 -*-
from flask import g, request
from app import babel
from config import LANGUAGES
from . import web

@babel.localeselector
def get_locale():
    """
    localeselector装饰器
    在请求之前被调用，当产生响应时，选择使用的语言
    """
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
