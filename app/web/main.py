# -*- coding: utf-8 -*-
from flask import g, current_app, request
from flask_sqlalchemy import get_debug_queries
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

@web.before_app_request
def before_request():
    """
    Such a function is executed before each request, even if outside of a blueprint.
    """
    g.locale = get_locale()

@web.after_app_request
def after_request(response):
    """
    Such a function is executed after each request, even if outside of the blueprint.
    """
    for query in get_debug_queries():
        if query.duration >= current_app.config['DATABASE_QUERY_TIMEOUT']:
            current_app.logger.info("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                                       (query.statement, query.parameters, query.duration, query.context))
    return response