# -*- coding: utf-8 -*-
from flask import g, session, current_app, request, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from flask_login import current_user
from app import babel
from app.main import main
from ..constant import SUPPORT_LANGUAGES
from app.models import Language

@main.route('/<string:lang>')
def choose_locale(lang):
    """切换语言"""
    lang = lang.lower()
    if lang not in [lang[1].lower() for lang in SUPPORT_LANGUAGES]:
        # 设置默认语言
        lang = current_app.config['BABEL_DEFAULT_LOCALE']

    session['locale'] = lang

    # remove the locale from the session if it's there
    # session.pop('locale', None)

    return redirect(request.args.get('next') or url_for('web.index'))


@babel.localeselector
def get_locale():
    """
    localeselector装饰器
    在请求之前被调用，当产生响应时，选择使用的语言
    """
    # 优先当前选择语言
    if session.get('locale'):
        current_app.logger.debug('Locale: %s --------|||---------' % session.get('locale'))
        return session['locale']

    # 其次，获取用户设置语言
    user = getattr(g, 'user', None)
    if user is not None and type(user):
        return user.locale

    # 最后，使用默认语言
    return request.accept_languages.best_match([lang[1].lower() for lang in SUPPORT_LANGUAGES])


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


# 针对程序全局请求的钩子，
# 必须使用before_app_request修饰器
@main.before_app_request
def before_request():
    """
    Such a function is executed before each request, even if outside of a blueprint.
    """
    # 设置本地化语言
    g.locale = get_locale()

    g.user = current_user

    # 验证用户
    if current_user.is_authenticated:
        # 每次收到用户的请求时都要调用ping()方法
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@main.after_app_request
def after_request(response):
    """
    Such a function is executed after each request, even if outside of the blueprint.
    """
    for query in get_debug_queries():
        if query.duration >= current_app.config['DATABASE_QUERY_TIMEOUT']:
            current_app.logger.info("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                                       (query.statement, query.parameters, query.duration, query.context))
    return response


@main.app_context_processor
def include_init_data():
    """注入共用的变量"""
    pjax = True if 'X-PJAX' in request.headers else False

    # 获取站点支持的所有语言
    support_languages = Language.query.filter_by(status=1).all()
    return {
        'is_pjax': pjax,
        'support_languages': support_languages
    }
