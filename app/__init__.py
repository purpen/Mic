# -*- coding: utf-8 -*-
"""
	__init__.py
	~~~~~~~~~~~~~~

	:copyright: (c) 2017 by purpen.
"""

from flask import Flask
# 脚本化管理
from flask_script import Manager, Shell
# 装载静态文件
from flask_bootstrap import Bootstrap
# 本地化日期和时间
from flask_moment import Moment
# 邮件
from flask_mail import Mail
# 数据库连接
from flask_sqlalchemy import SQLAlchemy
# 管理用户认证系统中的认证状态
from flask_login import LoginManager
# 国际化和本地化
from flask_babelex import Babel

# 导入配置参数
from config import config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
babel = Babel()

# Flask-Login初始化
login_manager = LoginManager()
# 属性可以设为None、'basic' 或'strong'
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # logging setting
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/urk.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Urk startup')

    # attach routes
    from .web import web
    app.register_blueprint(web)

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .blog import blog
    app.register_blueprint(blog)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # API REST
    from .api_1_0 import api as api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/v1.0')

    # 附加路由和自定义的错误页面

    return app